"""Custom exceptions for Ableton MCP Server."""


class AbletonMCPError(Exception):
    """Base exception for Ableton MCP Server."""

    pass


class ConnectionError(AbletonMCPError):
    """Raised when connection to Ableton fails."""

    pass


class CommandError(AbletonMCPError):
    """Raised when a command execution fails."""

    pass


class ValidationError(AbletonMCPError):
    """Raised when data validation fails."""

    pass


class TrackIndexError(ValidationError):
    """Raised when track index is out of range."""

    pass


class ClipIndexError(ValidationError):
    """Raised when clip index is out of range."""

    pass


class BrowserError(AbletonMCPError):
    """Raised when browser operations fail."""

    pass


class DeviceError(AbletonMCPError):
    """Raised when device operations fail."""

    pass


class TimeoutError(AbletonMCPError):
    """Raised when operations timeout."""

    pass


class InvalidNoteDataError(ValidationError):
    """Raised when note data is invalid."""

    pass


class InvalidTempoError(ValidationError):
    """Raised when tempo value is invalid."""

    pass
