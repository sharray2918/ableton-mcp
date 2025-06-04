"""Logging utilities for Ableton MCP Server."""

import logging


def setup_logging(
    level: str = "INFO",
    format_string: str | None = None,
    logger_name: str = "AbletonMCPServer",
) -> logging.Logger:
    """
    Set up logging configuration for the MCP server.

    Args:
        level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        format_string: Custom format string for log messages
        logger_name: Name of the logger

    Returns:
        Configured logger instance
    """
    if format_string is None:
        format_string = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    logging.basicConfig(level=getattr(logging, level.upper()), format=format_string)

    return logging.getLogger(logger_name)


def get_logger(name: str = "AbletonMCPServer") -> logging.Logger:
    """
    Get a logger instance with the specified name.

    Args:
        name: Logger name

    Returns:
        Logger instance
    """
    return logging.getLogger(name)
