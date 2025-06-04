# ableton_mcp_server.py
from mcp.server.fastmcp import FastMCP, Context
import json
import logging
from contextlib import asynccontextmanager
from typing import AsyncIterator, Dict, Any, List, Union

from .core import get_ableton_connection, disconnect_global_connection
from .tools import (
    get_session_info,
    get_track_info,
    create_midi_track,
    set_track_name,
    set_tempo,
    create_clip,
    add_notes_to_clip,
    set_clip_name,
    fire_clip,
    stop_clip,
    start_playback,
    stop_playback,
    load_instrument_or_effect,
    get_browser_tree,
    get_browser_items_at_path,
    load_drum_kit
)

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("AbletonMCPServer")


@asynccontextmanager
async def server_lifespan(server: FastMCP) -> AsyncIterator[Dict[str, Any]]:
    """Manage server startup and shutdown lifecycle"""
    try:
        logger.info("AbletonMCP server starting up")

        try:
            ableton = get_ableton_connection()
            logger.info("Successfully connected to Ableton on startup")
        except Exception as e:
            logger.warning(f"Could not connect to Ableton on startup: {str(e)}")
            logger.warning("Make sure the Ableton Remote Script is running")

        yield {}
    finally:
        disconnect_global_connection()
        logger.info("AbletonMCP server shut down")


# Create the MCP server with lifespan support
mcp = FastMCP(
    "AbletonMCP",
    description="Ableton Live integration through the Model Context Protocol",
    lifespan=server_lifespan
)


# Register all tool functions with MCP decorators
@mcp.tool()
def get_session_info_tool(ctx: Context) -> str:
    """Get detailed information about the current Ableton session"""
    return get_session_info(ctx)


@mcp.tool()
def get_track_info_tool(ctx: Context, track_index: int) -> str:
    """Get detailed information about a specific track in Ableton."""
    return get_track_info(ctx, track_index)


@mcp.tool()
def create_midi_track_tool(ctx: Context, index: int = -1) -> str:
    """Create a new MIDI track in the Ableton session."""
    return create_midi_track(ctx, index)


@mcp.tool()
def set_track_name_tool(ctx: Context, track_index: int, name: str) -> str:
    """Set the name of a track."""
    return set_track_name(ctx, track_index, name)


@mcp.tool()
def set_tempo_tool(ctx: Context, tempo: float) -> str:
    """Set the tempo of the Ableton session."""
    return set_tempo(ctx, tempo)


@mcp.tool()
def create_clip_tool(ctx: Context, track_index: int, clip_index: int, length: float = 4.0) -> str:
    """Create a new MIDI clip in the specified track and clip slot."""
    return create_clip(ctx, track_index, clip_index, length)


@mcp.tool()
def add_notes_to_clip_tool(
    ctx: Context,
    track_index: int,
    clip_index: int,
    notes: List[Dict[str, Union[int, float, bool]]]
) -> str:
    """Add MIDI notes to a clip."""
    return add_notes_to_clip(ctx, track_index, clip_index, notes)


@mcp.tool()
def set_clip_name_tool(ctx: Context, track_index: int, clip_index: int, name: str) -> str:
    """Set the name of a clip."""
    return set_clip_name(ctx, track_index, clip_index, name)


@mcp.tool()
def fire_clip_tool(ctx: Context, track_index: int, clip_index: int) -> str:
    """Start playing a clip."""
    return fire_clip(ctx, track_index, clip_index)


@mcp.tool()
def stop_clip_tool(ctx: Context, track_index: int, clip_index: int) -> str:
    """Stop playing a clip."""
    return stop_clip(ctx, track_index, clip_index)


@mcp.tool()
def start_playback_tool(ctx: Context) -> str:
    """Start playing the Ableton session."""
    return start_playback(ctx)


@mcp.tool()
def stop_playback_tool(ctx: Context) -> str:
    """Stop playing the Ableton session."""
    return stop_playback(ctx)


@mcp.tool()
def load_instrument_or_effect_tool(ctx: Context, track_index: int, uri: str) -> str:
    """Load an instrument or effect onto a track using its URI."""
    return load_instrument_or_effect(ctx, track_index, uri)


@mcp.tool()
def get_browser_tree_tool(ctx: Context, category_type: str = "all") -> str:
    """Get a hierarchical tree of browser categories from Ableton."""
    return get_browser_tree(ctx, category_type)


@mcp.tool()
def get_browser_items_at_path_tool(ctx: Context, path: str) -> str:
    """Get browser items at a specific path in Ableton's browser."""
    return get_browser_items_at_path(ctx, path)


@mcp.tool()
def load_drum_kit_tool(ctx: Context, track_index: int, rack_uri: str, kit_path: str) -> str:
    """Load a drum rack and then load a specific drum kit into it."""
    return load_drum_kit(ctx, track_index, rack_uri, kit_path)


# Main execution
def main():
    """Run the MCP server"""
    mcp.run()


if __name__ == "__main__":
    main()
