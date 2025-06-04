# AbletonMCP Remote Script entry point
from __future__ import absolute_import, print_function, unicode_literals

from .core.main import AbletonMCP


def create_instance(c_instance):
    """Create and return the AbletonMCP script instance"""
    return AbletonMCP(c_instance)
