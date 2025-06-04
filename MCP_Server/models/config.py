"""Configuration models for Ableton MCP Server."""

from dataclasses import dataclass


@dataclass
class ServerConfig:
    """Server configuration data model."""

    host: str = "localhost"
    port: int = 9877
    timeout: float = 10.0
    max_retries: int = 3
    retry_delay: float = 1.0
    buffer_size: int = 8192

    def __post_init__(self) -> None:
        """Validate configuration values."""
        if not (1 <= self.port <= 65535):
            raise ValueError(f"Port must be between 1 and 65535, got {self.port}")
        if self.timeout <= 0:
            raise ValueError(f"Timeout must be positive, got {self.timeout}")
        if self.max_retries < 0:
            raise ValueError(f"Max retries must be non-negative, got {self.max_retries}")
        if self.retry_delay < 0:
            raise ValueError(f"Retry delay must be non-negative, got {self.retry_delay}")
        if self.buffer_size <= 0:
            raise ValueError(f"Buffer size must be positive, got {self.buffer_size}")


@dataclass
class LogConfig:
    """Logging configuration data model."""

    level: str = "INFO"
    format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    enable_file_logging: bool = False
    log_file_path: str | None = None
    max_log_file_size: int = 10 * 1024 * 1024  # 10MB
    backup_count: int = 5


@dataclass
class MCPConfig:
    """MCP Server configuration data model."""

    server_name: str = "AbletonMCP"
    description: str = "Ableton Live integration through the Model Context Protocol"
    version: str = "1.0.0"

    # Connection settings
    server: ServerConfig = None
    logging: LogConfig = None

    def __post_init__(self) -> None:
        if self.server is None:
            self.server = ServerConfig()
        if self.logging is None:
            self.logging = LogConfig()


# Default configuration instance
DEFAULT_CONFIG = MCPConfig()
