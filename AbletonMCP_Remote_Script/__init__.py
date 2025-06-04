# AbletonMCP Remote Script entry point

from typing import Any

from .core.main import AbletonMCP


def create_instance(c_instance: Any) -> AbletonMCP:
    """Create and return the AbletonMCP script instance"""
    return AbletonMCP(c_instance)
