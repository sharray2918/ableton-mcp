"""Session and track management handlers for AbletonMCP Remote Script."""

from ..utils import BaseHandler, validate_tempo


class SessionHandlers(BaseHandler):
    """Handlers for session and track-related commands."""

    def get_session_info(self):
        """Get information about the current session"""
        try:
            result = {
                "tempo": self._song.tempo,
                "signature_numerator": self._song.signature_numerator,
                "signature_denominator": self._song.signature_denominator,
                "track_count": len(self._song.tracks),
                "return_track_count": len(self._song.return_tracks),
                "master_track": {
                    "name": "Master",
                    "volume": self._song.master_track.mixer_device.volume.value,
                    "panning": self._song.master_track.mixer_device.panning.value,
                },
            }
            return result
        except Exception as e:
            self.log_message("Error getting session info: " + str(e))
            raise

    def get_track_info(self, track_index):
        """Get information about a track"""
        try:
            track = self.get_track(track_index)

            # Get clip slots
            clip_slots = []
            for slot_index, slot in enumerate(track.clip_slots):
                clip_info = None
                if slot.has_clip:
                    clip = slot.clip
                    clip_info = {
                        "name": clip.name,
                        "length": clip.length,
                        "is_playing": clip.is_playing,
                        "is_recording": clip.is_recording,
                    }

                clip_slots.append({"index": slot_index, "has_clip": slot.has_clip, "clip": clip_info})

            # Get devices
            devices = []
            for device_index, device in enumerate(track.devices):
                devices.append(
                    {
                        "index": device_index,
                        "name": device.name,
                        "type": self._get_device_type(device),
                        "is_enabled": device.is_enabled,
                    }
                )

            result = {
                "index": track_index,
                "name": track.name,
                "is_audio_track": track.has_audio_input,
                "is_midi_track": track.has_midi_input,
                "mute": track.mute,
                "solo": track.solo,
                "arm": track.arm,
                "volume": track.mixer_device.volume.value,
                "panning": track.mixer_device.panning.value,
                "clip_slots": clip_slots,
                "devices": devices,
            }
            return result
        except Exception as e:
            self.log_message("Error getting track info: " + str(e))
            raise

    def create_midi_track(self, index):
        """Create a new MIDI track at the specified index"""
        try:
            # Create the track
            self._song.create_midi_track(index)

            # Get the new track
            new_track_index = len(self._song.tracks) - 1 if index == -1 else index
            new_track = self._song.tracks[new_track_index]

            result = {"index": new_track_index, "name": new_track.name}
            return result
        except Exception as e:
            self.log_message("Error creating MIDI track: " + str(e))
            raise

    def set_track_name(self, track_index, name):
        """Set the name of a track"""
        try:
            track = self.get_track(track_index)
            track.name = name

            result = {"name": track.name}
            return result
        except Exception as e:
            self.log_message("Error setting track name: " + str(e))
            raise

    def set_tempo(self, tempo):
        """Set the tempo of the session"""
        try:
            # Validate tempo value
            validate_tempo(tempo)

            self._song.tempo = tempo

            result = {"tempo": self._song.tempo}
            return result
        except Exception as e:
            self.log_message("Error setting tempo: " + str(e))
            raise

    def _get_device_type(self, device):
        """Get the type of a device"""
        try:
            # Simple heuristic - in a real implementation you'd look at the device class
            if device.can_have_drum_pads:
                return "drum_machine"
            elif device.can_have_chains:
                return "rack"
            elif "instrument" in device.class_display_name.lower():
                return "instrument"
            elif "audio_effect" in device.class_name.lower():
                return "audio_effect"
            elif "midi_effect" in device.class_name.lower():
                return "midi_effect"
            else:
                return "unknown"
        except:
            return "unknown"
