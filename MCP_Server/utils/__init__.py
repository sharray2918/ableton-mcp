"""Utility functions for Ableton MCP Server."""

from .logging import get_logger, setup_logging
from .validation import (
    validate_clip_index,
    validate_note_data,
    validate_tempo,
    validate_track_index,
)

__all__ = [
    # Validation utilities
    "validate_note_data",
    "validate_track_index",
    "validate_clip_index",
    "validate_tempo",
    # Logging utilities
    "setup_logging",
    "get_logger",
]
