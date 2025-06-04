"""
Main controller for AbletonMCP Remote Script.

This module contains the main AbletonMCP class that coordinates between
the socket server, client handler, and Ableton Live handlers.
"""

import traceback
from typing import Any

# Change queue import for Python 2
try:
    import Queue as queue  # Python 2
except ImportError:
    import queue  # Python 3

from _Framework.ControlSurface import ControlSurface

# Import handlers
from ..handlers.browser_handlers import BrowserHandlers
from ..handlers.clip_handlers import ClipHandlers
from ..handlers.playback_handlers import PlaybackHandlers
from ..handlers.session_handlers import SessionHandlers
from ..utils import format_error_response, format_success_response

# Import core components
from .client import ClientHandler
from .server import DEFAULT_PORT, SocketServer


class AbletonMCP(ControlSurface):
    """AbletonMCP Remote Script for Ableton Live."""

    def __init__(self, c_instance: Any) -> None:
        """Initialize the control surface."""
        ControlSurface.__init__(self, c_instance)
        self.log_message("AbletonMCP Remote Script initializing...")

        # Cache the song reference for easier access
        self._song = self.song()

        # Initialize handlers
        self.session_handlers = SessionHandlers(self)
        self.clip_handlers = ClipHandlers(self)
        self.playback_handlers = PlaybackHandlers(self)
        self.browser_handlers = BrowserHandlers(self)

        # Initialize client handler
        self.client_handler = ClientHandler(self, self._process_command)

        # Initialize and start socket server
        self.server = SocketServer(self, self.show_message)
        self.server.set_client_handler(self.client_handler.handle_client)

        # Start the socket server
        if self.server.start():
            self.client_handler.set_running(True)

        self.log_message("AbletonMCP initialized")

        # Show a message in Ableton
        msg = f"AbletonMCP: Listening for commands on port {DEFAULT_PORT}"
        self.show_message(msg)

    def disconnect(self) -> None:
        """Called when Ableton closes or the control surface is removed."""
        self.log_message("AbletonMCP disconnecting...")

        # Stop client handler first
        self.client_handler.set_running(False)

        # Stop the server
        self.server.stop()

        ControlSurface.disconnect(self)
        self.log_message("AbletonMCP disconnected")

    def _process_command(self, command: dict[str, Any]) -> dict[str, Any]:
        """
        Process a command from the client and return a response.

        Args:
            command: Command dictionary containing type and params

        Returns:
            dict: Response dictionary with status and result/error
        """
        command_type = command.get("type", "")
        params = command.get("params", {})

        try:
            # Route the command to the appropriate handler
            if command_type == "get_session_info":
                result = self.session_handlers.get_session_info()
                return format_success_response(result)
            if command_type == "get_track_info":
                track_index = params.get("track_index", 0)
                result = self.session_handlers.get_track_info(track_index)
                return format_success_response(result)
            # Commands that modify Live's state should be scheduled on
            # main thread
            if command_type in [
                "create_midi_track",
                "set_track_name",
                "create_clip",
                "add_notes_to_clip",
                "set_clip_name",
                "set_tempo",
                "fire_clip",
                "stop_clip",
                "start_playback",
                "stop_playback",
                "load_browser_item",
            ]:
                return self._handle_main_thread_command(command_type, params)
            if command_type == "get_browser_item":
                uri = params.get("uri", None)
                path = params.get("path", None)
                result = self.browser_handlers.get_browser_item(uri, path)
                return format_success_response(result)
            if command_type == "get_browser_tree":
                category_type = params.get("category_type", "all")
                result = self.browser_handlers.get_browser_tree(category_type)
                return format_success_response(result)
            if command_type == "get_browser_items_at_path":
                path = params.get("path", "")
                result = self.browser_handlers.get_browser_items_at_path(path)
                return format_success_response(result)
            error_msg = f"Unknown command: {command_type}"
            return format_error_response(error_msg)
        except (OSError, AttributeError, ValueError, TypeError) as e:
            self.log_message(f"Error processing command: {str(e)}")
            self.log_message(traceback.format_exc())
            return format_error_response(str(e))

    def _handle_main_thread_command(self, command_type: str, params: dict[str, Any]) -> dict[str, Any]:
        """
        Handle commands that need to run on the main thread.

        Args:
            command_type: Type of command to execute
            params: Command parameters

        Returns:
            dict: Response dictionary with status and result/error
        """
        # Use a thread-safe approach with a response queue
        response_queue = queue.Queue()

        # Define a function to execute on the main thread
        def main_thread_task() -> None:
            try:
                result = None
                if command_type == "create_midi_track":
                    index = params.get("index", -1)
                    result = self.session_handlers.create_midi_track(index)
                elif command_type == "set_track_name":
                    track_idx = params.get("track_index", 0)
                    name = params.get("name", "")
                    result = self.session_handlers.set_track_name(track_idx, name)
                elif command_type == "create_clip":
                    track_idx = params.get("track_index", 0)
                    clip_idx = params.get("clip_index", 0)
                    length = params.get("length", 4.0)
                    result = self.clip_handlers.create_clip(track_idx, clip_idx, length)
                elif command_type == "add_notes_to_clip":
                    track_idx = params.get("track_index", 0)
                    clip_idx = params.get("clip_index", 0)
                    notes = params.get("notes", [])
                    result = self.clip_handlers.add_notes_to_clip(track_idx, clip_idx, notes)
                elif command_type == "set_clip_name":
                    track_idx = params.get("track_index", 0)
                    clip_idx = params.get("clip_index", 0)
                    name = params.get("name", "")
                    result = self.clip_handlers.set_clip_name(track_idx, clip_idx, name)
                elif command_type == "set_tempo":
                    tempo = params.get("tempo", 120.0)
                    result = self.session_handlers.set_tempo(tempo)
                elif command_type == "fire_clip":
                    track_idx = params.get("track_index", 0)
                    clip_idx = params.get("clip_index", 0)
                    result = self.clip_handlers.fire_clip(track_idx, clip_idx)
                elif command_type == "stop_clip":
                    track_idx = params.get("track_index", 0)
                    clip_idx = params.get("clip_index", 0)
                    result = self.clip_handlers.stop_clip(track_idx, clip_idx)
                elif command_type == "start_playback":
                    result = self.playback_handlers.start_playback()
                elif command_type == "stop_playback":
                    result = self.playback_handlers.stop_playback()
                elif command_type == "load_browser_item":
                    track_idx = params.get("track_index", 0)
                    item_uri = params.get("item_uri", "")
                    result = self.browser_handlers.load_browser_item(track_idx, item_uri)

                # Put the result in the queue
                response_queue.put(format_success_response(result))
            except (OSError, AttributeError, ValueError, TypeError) as e:
                error_msg = f"Error in main thread task: {str(e)}"
                self.log_message(error_msg)
                self.log_message(traceback.format_exc())
                response_queue.put(format_error_response(str(e)))

        # Schedule the task to run on the main thread
        try:
            self.schedule_message(0, main_thread_task)
        except AssertionError:
            # If we're already on the main thread, execute directly
            main_thread_task()

        # Wait for the response with a timeout
        try:
            return response_queue.get(timeout=10.0)
        except queue.Empty:
            error_msg = "Timeout waiting for operation to complete"
            return format_error_response(error_msg)
