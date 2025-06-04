"""Clip management handlers for AbletonMCP Remote Script."""

from typing import Any

from ..utils import BaseHandler, validate_note_data


class ClipHandlers(BaseHandler):
    """Handlers for clip-related commands."""

    def create_clip(self, track_index: int, clip_index: int, length: float) -> dict[str, Any]:
        """Create a new MIDI clip in the specified track and clip slot"""
        try:
            clip_slot = self.get_clip_slot(track_index, clip_index)

            # Check if the clip slot already has a clip
            if clip_slot.has_clip:
                raise Exception("Clip slot already has a clip")

            # Create the clip
            clip_slot.create_clip(length)

            result = {"name": clip_slot.clip.name, "length": clip_slot.clip.length}
            return result
        except Exception as e:
            self.log_message("Error creating clip: " + str(e))
            raise

    def add_notes_to_clip(self, track_index: int, clip_index: int, notes: list[dict[str, Any]]) -> dict[str, Any]:
        """Add MIDI notes to a clip"""
        try:
            clip_slot = self.get_clip_slot(track_index, clip_index)

            if not clip_slot.has_clip:
                raise Exception("No clip in slot")

            clip = clip_slot.clip

            # Validate and convert note data to Live's format
            live_notes = []
            for note in notes:
                # Validate note data
                validate_note_data(note)

                pitch = note.get("pitch", 60)
                start_time = note.get("start_time", 0.0)
                duration = note.get("duration", 0.25)
                velocity = note.get("velocity", 100)
                mute = note.get("mute", False)

                live_notes.append((pitch, start_time, duration, velocity, mute))

            # Add the notes
            clip.set_notes(tuple(live_notes))

            result = {"note_count": len(notes)}
            return result
        except Exception as e:
            self.log_message("Error adding notes to clip: " + str(e))
            raise

    def set_clip_name(self, track_index: int, clip_index: int, name: str) -> dict[str, Any]:
        """Set the name of a clip"""
        try:
            clip_slot = self.get_clip_slot(track_index, clip_index)

            if not clip_slot.has_clip:
                raise Exception("No clip in slot")

            clip = clip_slot.clip
            clip.name = name

            result = {"name": clip.name}
            return result
        except Exception as e:
            self.log_message("Error setting clip name: " + str(e))
            raise

    def fire_clip(self, track_index: int, clip_index: int) -> dict[str, Any]:
        """Fire a clip"""
        try:
            clip_slot = self.get_clip_slot(track_index, clip_index)

            if not clip_slot.has_clip:
                raise Exception("No clip in slot")

            # Fire the clip
            clip_slot.fire()

            result = {"fired": True, "name": clip_slot.clip.name}
            return result
        except Exception as e:
            self.log_message("Error firing clip: " + str(e))
            raise

    def stop_clip(self, track_index: int, clip_index: int) -> dict[str, Any]:
        """Stop a clip"""
        try:
            clip_slot = self.get_clip_slot(track_index, clip_index)

            if not clip_slot.has_clip:
                raise Exception("No clip in slot")

            # Stop the clip
            clip_slot.stop()

            result = {"stopped": True, "name": clip_slot.clip.name}
            return result
        except Exception as e:
            self.log_message("Error stopping clip: " + str(e))
            raise
