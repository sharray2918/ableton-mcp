"""Playback control handlers for AbletonMCP Remote Script."""

import traceback


class PlaybackHandlers:
    """Handlers for playback-related commands."""

    def __init__(self, control_surface):
        self.control_surface = control_surface
        self._song = control_surface._song

    def log_message(self, message):
        """Log a message using the control surface's logging."""
        self.control_surface.log_message(message)

    def start_playback(self):
        """Start playing the session"""
        try:
            self._song.start_playing()

            result = {"playing": self._song.is_playing}
            return result
        except Exception as e:
            self.log_message("Error starting playback: " + str(e))
            raise

    def stop_playback(self):
        """Stop playing the session"""
        try:
            self._song.stop_playing()

            result = {"playing": self._song.is_playing}
            return result
        except Exception as e:
            self.log_message("Error stopping playback: " + str(e))
            raise
