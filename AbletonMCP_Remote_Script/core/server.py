"""
Socket server for AbletonMCP Remote Script.

This module handles the socket server functionality for accepting and managing
client connections to the Ableton Live Remote Script.
"""

from collections.abc import Callable
import socket
import threading
import time
from typing import Any

# Constants for socket communication
DEFAULT_PORT = 9877
HOST = "localhost"


class SocketServer:
    """Socket server for handling client connections to AbletonMCP."""

    def __init__(
        self,
        logger: Any,
        message_handler: Callable[[str], None],
        port: int = DEFAULT_PORT,
        host: str = HOST,
    ):
        """
        Initialize the socket server.

        Args:
            logger: Logger instance for logging messages
            message_handler: Function to handle showing messages in Ableton
            port: Port number to listen on
            host: Host address to bind to
        """
        self.logger = logger
        self.message_handler = message_handler
        self.port = port
        self.host = host

        # Server state
        self.server: socket.socket | None = None
        self.client_threads: list[threading.Thread] = []
        self.server_thread: threading.Thread | None = None
        self.running = False

        # Client handler callback
        self.client_handler: Callable[[socket.socket], None] | None = None

    def set_client_handler(self, handler: Callable[[socket.socket], None]) -> None:
        """
        Set the client handler callback.

        Args:
            handler: Function to handle client connections
        """
        self.client_handler = handler

    def start(self) -> bool:
        """
        Start the socket server in a separate thread.

        Returns:
            bool: True if server started successfully, False otherwise
        """
        try:
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server.bind((self.host, self.port))
            self.server.listen(5)  # Allow up to 5 pending connections

            self.running = True
            self.server_thread = threading.Thread(target=self._server_thread)
            self.server_thread.daemon = True
            self.server_thread.start()

            self.logger.log_message(f"Server started on port {self.port}")
            return True
        except OSError as e:
            self.logger.log_message(f"Error starting server: {str(e)}")
            error_msg = f"AbletonMCP: Error starting server - {str(e)}"
            self.message_handler(error_msg)
            return False

    def stop(self) -> None:
        """Stop the socket server and clean up resources."""
        self.logger.log_message("Stopping socket server...")
        self.running = False

        # Stop the server
        if self.server:
            try:
                self.server.close()
            except OSError:
                pass

        # Wait for the server thread to exit
        if self.server_thread and self.server_thread.is_alive():
            self.server_thread.join(1.0)

        # Clean up any client threads
        for client_thread in self.client_threads[:]:
            if client_thread.is_alive():
                # We don't join them as they might be stuck
                msg = "Client thread still alive during disconnect"
                self.logger.log_message(msg)

        self.logger.log_message("Socket server stopped")

    def _server_thread(self) -> None:
        """Server thread implementation - handles client connections."""
        try:
            self.logger.log_message("Server thread started")
            # Set a timeout to allow regular checking of running flag
            if self.server:
                self.server.settimeout(1.0)

            while self.running and self.server:
                try:
                    # Accept connections with timeout
                    client, address = self.server.accept()
                    msg = f"Connection accepted from {str(address)}"
                    self.logger.log_message(msg)
                    self.message_handler("AbletonMCP: Client connected")

                    # Handle client in a separate thread if handler is set
                    if self.client_handler:
                        client_thread = threading.Thread(target=self.client_handler, args=(client,))
                        client_thread.daemon = True
                        client_thread.start()

                        # Keep track of client threads
                        self.client_threads.append(client_thread)

                        # Clean up finished client threads
                        self.client_threads = [t for t in self.client_threads if t.is_alive()]

                except TimeoutError:
                    # No connection yet, just continue
                    continue
                except OSError as e:
                    if self.running:  # Only log if still running
                        msg = f"Server accept error: {str(e)}"
                        self.logger.log_message(msg)
                    time.sleep(0.5)

            self.logger.log_message("Server thread stopped")
        except OSError as e:
            self.logger.log_message(f"Server thread error: {str(e)}")

    @property
    def is_running(self) -> bool:
        """Check if the server is currently running."""
        return self.running
