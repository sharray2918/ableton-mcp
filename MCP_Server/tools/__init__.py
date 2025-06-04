"""Tools module for Ableton MCP Server."""

from .browser_tools import get_browser_items_at_path, get_browser_tree, load_drum_kit, load_instrument_or_effect
from .clip_tools import add_notes_to_clip, create_clip, fire_clip, set_clip_name, stop_clip
from .playback_tools import start_playback, stop_playback
from .session_tools import create_midi_track, get_session_info, get_track_info, set_tempo, set_track_name

__all__ = [
    # Session tools
    "get_session_info",
    "get_track_info",
    "create_midi_track",
    "set_track_name",
    "set_tempo",
    # Clip tools
    "create_clip",
    "add_notes_to_clip",
    "set_clip_name",
    "fire_clip",
    "stop_clip",
    # Playback tools
    "start_playback",
    "stop_playback",
    # Browser tools
    "load_instrument_or_effect",
    "get_browser_tree",
    "get_browser_items_at_path",
    "load_drum_kit",
]
