"""Base handler class for AbletonMCP Remote Script handlers."""

from typing import Any

from .error_handling import handle_exception, safe_execute
from .logging import RemoteScriptLogger
from .validation import validate_clip_index, validate_track_index


class BaseHandler:
    """Base class for all AbletonMCP Remote Script handlers."""

    def __init__(self, control_surface: Any) -> None:
        """
        Initialize the handler with a control surface.

        Args:
            control_surface: The control surface instance
        """
        self.control_surface = control_surface
        self._song = control_surface._song
        self.logger = RemoteScriptLogger(control_surface)

    def log_message(self, message: str) -> None:
        """
        Log a message using the control surface's logging.

        Args:
            message: The message to log
        """
        self.logger.log_message(message)

    def log_error(self, message: str, exception: Exception | None = None) -> None:
        """
        Log an error message with optional exception details.

        Args:
            message: The error message to log
            exception: Optional exception to include in the log
        """
        self.logger.log_error(message, exception)

    def handle_exception(self, operation_name: str, exception: Exception) -> dict[str, Any]:
        """
        Handle exceptions with consistent logging and error formatting.

        Args:
            operation_name: Name of the operation that failed
            exception: The exception that occurred

        Returns:
            dict: Error response dictionary
        """
        return handle_exception(self.logger, operation_name, exception)

    def safe_execute(self, operation_name: str, func: Any, *args: Any, **kwargs: Any) -> tuple[bool, Any]:
        """
        Safely execute a function with error handling.

        Args:
            operation_name: Name of the operation being performed
            func: Function to execute
            *args: Positional arguments for the function
            **kwargs: Keyword arguments for the function

        Returns:
            tuple: (success: bool, result: any)
        """
        return safe_execute(self.logger, operation_name, func, *args, **kwargs)

    def validate_track_index(self, track_index: int) -> bool:
        """
        Validate that a track index is within the valid range.

        Args:
            track_index: The track index to validate

        Returns:
            bool: True if valid

        Raises:
            IndexError: If track index is out of range
        """
        return validate_track_index(track_index, self._song)

    def validate_clip_index(self, clip_index: int, track: Any) -> bool:
        """
        Validate that a clip index is within the valid range for a track.

        Args:
            clip_index: The clip index to validate
            track: The track object containing clip slots

        Returns:
            bool: True if valid

        Raises:
            IndexError: If clip index is out of range
        """
        return validate_clip_index(clip_index, track)

    def get_track(self, track_index: int) -> Any:
        """
        Get a track by index with validation.

        Args:
            track_index: The index of the track to get

        Returns:
            Track object

        Raises:
            IndexError: If track index is out of range
        """
        self.validate_track_index(track_index)
        return self._song.tracks[track_index]

    def get_clip_slot(self, track_index: int, clip_index: int) -> Any:
        """
        Get a clip slot by track and clip index with validation.

        Args:
            track_index: The index of the track
            clip_index: The index of the clip slot

        Returns:
            ClipSlot object

        Raises:
            IndexError: If track or clip index is out of range
        """
        track = self.get_track(track_index)
        self.validate_clip_index(clip_index, track)
        return track.clip_slots[clip_index]
