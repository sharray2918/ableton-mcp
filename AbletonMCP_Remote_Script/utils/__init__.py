"""Utility functions for AbletonMCP Remote Script."""

from .base_handler import BaseHandler
from .error_handling import (
    format_error_response,
    format_success_response,
    handle_exception,
    safe_execute,
)
from .logging import RemoteScriptLogger
from .validation import (
    validate_clip_index,
    validate_clip_length,
    validate_note_data,
    validate_tempo,
    validate_track_index,
)

__all__ = [
    # Base handler class
    "BaseHandler",
    # Logging utilities
    "RemoteScriptLogger",
    # Validation utilities
    "validate_track_index",
    "validate_clip_index",
    "validate_tempo",
    "validate_clip_length",
    "validate_note_data",
    # Error handling utilities
    "handle_exception",
    "safe_execute",
    "format_error_response",
    "format_success_response",
]
