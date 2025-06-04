"""Core functionality for Ableton MCP Server."""

from .connection import AbletonConnection, get_ableton_connection, disconnect_global_connection

__all__ = ["AbletonConnection", "get_ableton_connection", "disconnect_global_connection"]
