"""Playback control handlers for AbletonMCP Remote Script."""

from ..utils import BaseHandler


class PlaybackHandlers(BaseHandler):
    """Handlers for playback-related commands."""

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
