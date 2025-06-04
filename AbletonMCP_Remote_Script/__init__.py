# AbletonMCP Remote Script entry point

from .core.main import AbletonMCP


def create_instance(c_instance):
    """Create and return the AbletonMCP script instance"""
    return AbletonMCP(c_instance)
