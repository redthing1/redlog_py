"""
redlog - A modern Python logging library

Features:
- Beautiful aligned output with automatic color detection
- Structured logging with key-value fields
- Immutable scoped loggers for hierarchical context
- Thread-safe by design
- Printf-style formatting support
- Customizable themes and formatters
"""

from .core import Level, Logger, get_logger, set_level, get_level, level_name, level_short_name
from .fields import Field, FieldSet
from .themes import Theme, Color, themes, set_theme, get_theme
from .formatters import Formatter, DefaultFormatter, TimestampedFormatter, JSONFormatter
from .sinks import Sink, ConsoleSink, FileSink, StringSink
from .utils import fmt

__version__ = "0.1.0"
__all__ = [
    # Core API
    "Level",
    "Logger",
    "get_logger",
    "set_level",
    "get_level",
    # Fields
    "Field",
    "FieldSet",
    # Themes
    "Theme",
    "Color",
    "themes",
    "set_theme",
    "get_theme",
    # Formatters
    "Formatter",
    "DefaultFormatter",
    "TimestampedFormatter",
    "JSONFormatter",
    # Sinks
    "Sink",
    "ConsoleSink",
    "FileSink",
    "StringSink",
    # Utilities
    "fmt",
    # Additional exports
    "level_name",
    "level_short_name",
]


def field(key: str, value) -> Field:
    """Create a field for structured logging.

    Args:
        key: Field name
        value: Field value (any type)

    Returns:
        Field instance

    Example:
        log.info("User action", field("user_id", 123), field("action", "login"))
    """
    return Field(key, value)
