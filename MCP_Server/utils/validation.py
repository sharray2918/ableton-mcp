"""Data validation utilities for Ableton MCP Server."""

from typing import Any


def validate_note_data(note_data: dict[str, Any]) -> bool:
    """Validate note data structure."""
    required_fields = ["pitch", "start_time", "duration"]
    return all(field in note_data for field in required_fields)


def validate_track_index(track_index: int, max_tracks: int) -> bool:
    """Validate track index is within bounds."""
    return 0 <= track_index < max_tracks


def validate_clip_index(clip_index: int, max_clips: int) -> bool:
    """Validate clip index is within bounds."""
    return 0 <= clip_index < max_clips


def validate_tempo(tempo: float) -> bool:
    """Validate tempo is within reasonable range."""
    return 20.0 <= tempo <= 999.0
