"""Validation utilities for AbletonMCP Remote Script."""


def validate_track_index(track_index, song):
    """
    Validate that a track index is within the valid range.

    Args:
        track_index: The track index to validate
        song: The song object containing tracks

    Returns:
        bool: True if valid, False otherwise

    Raises:
        IndexError: If track index is out of range
    """
    if track_index < 0 or track_index >= len(song.tracks):
        raise IndexError("Track index out of range")
    return True


def validate_clip_index(clip_index, track):
    """
    Validate that a clip index is within the valid range for a track.

    Args:
        clip_index: The clip index to validate
        track: The track object containing clip slots

    Returns:
        bool: True if valid, False otherwise

    Raises:
        IndexError: If clip index is out of range
    """
    if clip_index < 0 or clip_index >= len(track.clip_slots):
        raise IndexError("Clip index out of range")
    return True


def validate_tempo(tempo):
    """
    Validate that a tempo value is within reasonable range.

    Args:
        tempo: The tempo value to validate

    Returns:
        bool: True if valid, False otherwise

    Raises:
        ValueError: If tempo is out of valid range
    """
    if not (20.0 <= tempo <= 999.0):
        raise ValueError(f"Tempo must be between 20.0 and 999.0, got {tempo}")
    return True


def validate_clip_length(length):
    """
    Validate that a clip length is positive.

    Args:
        length: The clip length to validate

    Returns:
        bool: True if valid, False otherwise

    Raises:
        ValueError: If length is not positive
    """
    if length <= 0:
        raise ValueError(f"Clip length must be positive, got {length}")
    return True


def validate_note_data(note):
    """
    Validate note data structure.

    Args:
        note: Dictionary containing note data

    Returns:
        bool: True if valid, False otherwise

    Raises:
        ValueError: If note data is invalid
    """
    required_fields = ["pitch", "start_time", "duration"]
    for field in required_fields:
        if field not in note:
            raise ValueError(f"Note data missing required field: {field}")

    # Validate pitch range
    pitch = note.get("pitch", 60)
    if not (0 <= pitch <= 127):
        raise ValueError(f"MIDI pitch must be between 0 and 127, got {pitch}")

    # Validate velocity range
    velocity = note.get("velocity", 100)
    if not (0 <= velocity <= 127):
        raise ValueError(f"MIDI velocity must be between 0 and 127, got {velocity}")

    # Validate timing values
    start_time = note.get("start_time", 0.0)
    if start_time < 0:
        raise ValueError(f"Start time must be non-negative, got {start_time}")

    duration = note.get("duration", 0.25)
    if duration <= 0:
        raise ValueError(f"Duration must be positive, got {duration}")

    return True
