"""
Client handler for AbletonMCP Remote Script.

This module handles individual client connections and message processing
for the Ableton Live Remote Script.
"""

from collections.abc import Callable
import contextlib
import json
import socket
import traceback
from typing import Any

from ..utils import format_error_response


class ClientHandler:
    """Handles individual client connections and message processing."""

    def __init__(
        self,
        logger: Any,
        command_processor: Callable[[dict[str, Any]], dict[str, Any]],
    ):
        """
        Initialize the client handler.

        Args:
            logger: Logger instance for logging messages
            command_processor: Function to process commands and return responses
        """
        self.logger = logger
        self.command_processor = command_processor
        self.running = False

    def set_running(self, running: bool) -> None:
        """
        Set the running state.

        Args:
            running: Whether the handler should continue running
        """
        self.running = running

    def handle_client(self, client: socket.socket) -> None:
        """
        Handle communication with a connected client.

        Args:
            client: The client socket to handle
        """
        self.logger.log_message("Client handler started")
        client.settimeout(None)  # No timeout for client socket
        buffer = ""  # String buffer for Python 2/3 compatibility

        try:
            while self.running:
                try:
                    # Receive data
                    data = client.recv(8192)

                    if not data:
                        # Client disconnected
                        self.logger.log_message("Client disconnected")
                        break

                    # Handle encoding differences between Python 2 and 3
                    try:
                        # Python 3: data is bytes, decode to string
                        buffer += data.decode("utf-8")
                    except (AttributeError, UnicodeDecodeError):
                        # Python 2: data is already string or decode failed
                        buffer += str(data)

                    try:
                        # Try to parse command from buffer
                        command = json.loads(buffer)
                        buffer = ""  # Clear buffer after successful parse

                        command_type = command.get("type", "unknown")
                        msg = f"Received command: {command_type}"
                        self.logger.log_message(msg)

                        # Process the command and get response
                        response = self.command_processor(command)

                        # Send the response with explicit encoding
                        self._send_response(client, response)
                    except ValueError:
                        # Incomplete data, wait for more
                        continue

                except OSError as e:
                    error_msg = f"Error handling client data: {str(e)}"
                    self.logger.log_message(error_msg)
                    self.logger.log_message(traceback.format_exc())

                    # Send error response if possible
                    error_response = format_error_response(str(e))
                    try:
                        self._send_response(client, error_response)
                    except OSError:
                        # If we can't send the error, connection is dead
                        break
                    break
        except OSError as e:
            self.logger.log_message(f"Error in client handler: {str(e)}")
        finally:
            with contextlib.suppress(OSError):
                client.close()
            self.logger.log_message("Client handler stopped")

    def _send_response(self, client: socket.socket, response: dict[str, Any]) -> None:
        """
        Send a JSON response to the client.

        Args:
            client: The client socket to send to
            response: The response dictionary to send

        Raises:
            OSError: If there's an error sending the response
        """
        response_data = json.dumps(response)
        # Handle encoding differences between Python 2 and 3
        if hasattr(response_data, "encode"):
            # Python 3: encode string to bytes
            client.sendall(response_data.encode("utf-8"))
        else:
            # Python 2: string is already bytes-like
            client.sendall(response_data)
