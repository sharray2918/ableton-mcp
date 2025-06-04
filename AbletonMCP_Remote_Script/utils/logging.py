"""Logging utilities for AbletonMCP Remote Script."""

from typing import Any


class RemoteScriptLogger:
    """Shared logging functionality for AbletonMCP Remote Script handlers."""

    def __init__(self, control_surface: Any) -> None:
        """
        Initialize the logger with a control surface.

        Args:
            control_surface: The control surface instance for logging
        """
        self.control_surface = control_surface

    def log_message(self, message: str) -> None:
        """
        Log a message using the control surface's logging.

        Args:
            message: The message to log
        """
        self.control_surface.log_message(message)

    def log_error(self, message: str, exception: Exception | None = None) -> None:
        """
        Log an error message with optional exception details.

        Args:
            message: The error message to log
            exception: Optional exception to include in the log
        """
        if exception:
            self.log_message(f"Error: {message} - {str(exception)}")
        else:
            self.log_message(f"Error: {message}")

    def log_debug(self, message: str) -> None:
        """
        Log a debug message.

        Args:
            message: The debug message to log
        """
        self.log_message(f"Debug: {message}")

    def log_info(self, message: str) -> None:
        """
        Log an info message.

        Args:
            message: The info message to log
        """
        self.log_message(f"Info: {message}")
