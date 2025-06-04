"""Custom exceptions for Ableton MCP Server."""


class AbletonMCPError(Exception):
    """Base exception for Ableton MCP Server."""


class ConnectionError(AbletonMCPError):
    """Raised when connection to Ableton fails."""


class CommandError(AbletonMCPError):
    """Raised when a command execution fails."""


class ValidationError(AbletonMCPError):
    """Raised when data validation fails."""


class TrackIndexError(ValidationError):
    """Raised when track index is out of range."""


class ClipIndexError(ValidationError):
    """Raised when clip index is out of range."""


class BrowserError(AbletonMCPError):
    """Raised when browser operations fail."""


class DeviceError(AbletonMCPError):
    """Raised when device operations fail."""


class TimeoutError(AbletonMCPError):
    """Raised when operations timeout."""


class InvalidNoteDataError(ValidationError):
    """Raised when note data is invalid."""


class InvalidTempoError(ValidationError):
    """Raised when tempo value is invalid."""
