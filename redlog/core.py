"""
Core logging functionality - levels, logger class, and configuration.
"""

import sys
import threading
from dataclasses import dataclass
from datetime import datetime
from enum import IntEnum
from typing import Any, List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .fields import Field, FieldSet
    from .formatters import Formatter
    from .sinks import Sink


class Level(IntEnum):
    """Log level enumeration with explicit ordering (lower values = higher priority).

    Provides both full names and 3-character abbreviations for each level.
    Default level is INFO (3).
    """

    CRITICAL = 0  # crt - system-breaking errors
    ERROR = 1  # err - recoverable errors
    WARN = 2  # wrn - warnings and potential issues
    INFO = 3  # inf - general informational messages (default)
    VERBOSE = 4  # vrb - detailed operational information
    TRACE = 5  # trc - detailed execution tracing
    DEBUG = 6  # dbg - debugging information
    PEDANTIC = 7  # ped - extremely detailed debugging
    ANNOYING = 8  # ayg - maximum verbosity


def level_name(level: Level) -> str:
    """Get the full name of a log level."""
    names = {
        Level.CRITICAL: "critical",
        Level.ERROR: "error",
        Level.WARN: "warn",
        Level.INFO: "info",
        Level.VERBOSE: "verbose",
        Level.TRACE: "trace",
        Level.DEBUG: "debug",
        Level.PEDANTIC: "pedantic",
        Level.ANNOYING: "annoying",
    }
    return names.get(level, "unknown")


def level_short_name(level: Level) -> str:
    """Get the 3-character abbreviation of a log level."""
    names = {
        Level.CRITICAL: "crt",
        Level.ERROR: "err",
        Level.WARN: "wrn",
        Level.INFO: "inf",
        Level.VERBOSE: "vrb",
        Level.TRACE: "trc",
        Level.DEBUG: "dbg",
        Level.PEDANTIC: "ped",
        Level.ANNOYING: "ayg",
    }
    return names.get(level, "unk")


@dataclass
class LogEntry:
    """Log entry representing a single log message with metadata."""

    level: Level
    message: str
    source: str
    fields: "FieldSet"
    timestamp: datetime


class Config:
    """Global configuration for redlog."""

    def __init__(self) -> None:
        self._min_level = Level.INFO
        self._theme = None  # Will be set to default theme when themes module loads
        self._lock = threading.Lock()

    @property
    def min_level(self) -> Level:
        """Get the current minimum log level."""
        return self._min_level

    def set_level(self, level: Level) -> None:
        """Set the global minimum log level."""
        with self._lock:
            self._min_level = level

    @property
    def theme(self):
        """Get the current theme."""
        if self._theme is None:
            # Import here to avoid circular imports
            from .themes import themes

            self._theme = themes.DEFAULT
        return self._theme

    def set_theme(self, theme) -> None:
        """Set the global theme."""
        with self._lock:
            self._theme = theme


# Global configuration instance
_config = Config()


class Logger:
    """Main logger class with immutable design for natural thread safety.

    Loggers are immutable - methods like with_name() and with_field() return
    new logger instances rather than modifying the original. This provides
    clean scoping semantics and thread safety.
    """

    def __init__(
        self,
        name: str = "",
        formatter: Optional["Formatter"] = None,
        sink: Optional["Sink"] = None,
        fields: Optional["FieldSet"] = None,
    ) -> None:
        self._name = name
        self._formatter = formatter
        self._sink = sink
        self._fields = fields

    @property
    def name(self) -> str:
        return self._name

    @property
    def formatter(self) -> "Formatter":
        if self._formatter is None:
            from .formatters import DefaultFormatter

            return DefaultFormatter()
        return self._formatter

    @property
    def sink(self) -> "Sink":
        if self._sink is None:
            from .sinks import ConsoleSink

            return ConsoleSink()
        return self._sink

    @property
    def fields(self) -> "FieldSet":
        if self._fields is None:
            from .fields import FieldSet

            return FieldSet()
        return self._fields

    def with_name(self, name: str) -> "Logger":
        """Create a scoped logger with additional name component.

        Example: logger("app").with_name("db") creates logger named "app.db"
        """
        new_name = f"{self._name}.{name}" if self._name else name
        return Logger(new_name, self._formatter, self._sink, self._fields)

    def with_field(self, key: str, value: Any) -> "Logger":
        """Create a logger with additional field.

        Field values are converted to strings using the universal stringify function.
        """
        from .fields import Field

        new_fields = self.fields.with_field(Field(key, value))
        return Logger(self._name, self._formatter, self._sink, new_fields)

    def with_fields(self, *fields: "Field") -> "Logger":
        """Create a logger with multiple additional fields."""
        new_fields = self.fields
        for field in fields:
            new_fields = new_fields.with_field(field)
        return Logger(self._name, self._formatter, self._sink, new_fields)

    def _should_log(self, level: Level) -> bool:
        """Check if level should be logged."""
        return level <= _config.min_level

    def _log(self, level: Level, message: str, *fields: "Field") -> None:
        """Core logging implementation."""
        if not self._should_log(level):
            return

        try:
            # Create merged field set
            entry_fields = self.fields
            for field in fields:
                entry_fields = entry_fields.with_field(field)

            entry = LogEntry(level, message, self._name, entry_fields, datetime.now())
            formatted = self.formatter.format(entry)
            self.sink.write(formatted)
        except Exception:
            # Fallback error handling
            print(f"[redlog-error] Failed to log: {message}", file=sys.stderr)

    # Full name logging methods
    def critical(self, message: str, *fields: "Field") -> None:
        """Log a critical message."""
        self._log(Level.CRITICAL, message, *fields)

    def error(self, message: str, *fields: "Field") -> None:
        """Log an error message."""
        self._log(Level.ERROR, message, *fields)

    def warn(self, message: str, *fields: "Field") -> None:
        """Log a warning message."""
        self._log(Level.WARN, message, *fields)

    def info(self, message: str, *fields: "Field") -> None:
        """Log an info message."""
        self._log(Level.INFO, message, *fields)

    def verbose(self, message: str, *fields: "Field") -> None:
        """Log a verbose message."""
        self._log(Level.VERBOSE, message, *fields)

    def trace(self, message: str, *fields: "Field") -> None:
        """Log a trace message."""
        self._log(Level.TRACE, message, *fields)

    def debug(self, message: str, *fields: "Field") -> None:
        """Log a debug message."""
        self._log(Level.DEBUG, message, *fields)

    def pedantic(self, message: str, *fields: "Field") -> None:
        """Log a pedantic message."""
        self._log(Level.PEDANTIC, message, *fields)

    def annoying(self, message: str, *fields: "Field") -> None:
        """Log an annoying message."""
        self._log(Level.ANNOYING, message, *fields)

    # Short name logging methods
    def crt(self, message: str, *fields: "Field") -> None:
        """Log a critical message (short form)."""
        self.critical(message, *fields)

    def err(self, message: str, *fields: "Field") -> None:
        """Log an error message (short form)."""
        self.error(message, *fields)

    def wrn(self, message: str, *fields: "Field") -> None:
        """Log a warning message (short form)."""
        self.warn(message, *fields)

    def inf(self, message: str, *fields: "Field") -> None:
        """Log an info message (short form)."""
        self.info(message, *fields)

    def vrb(self, message: str, *fields: "Field") -> None:
        """Log a verbose message (short form)."""
        self.verbose(message, *fields)

    def trc(self, message: str, *fields: "Field") -> None:
        """Log a trace message (short form)."""
        self.trace(message, *fields)

    def dbg(self, message: str, *fields: "Field") -> None:
        """Log a debug message (short form)."""
        self.debug(message, *fields)

    def ped(self, message: str, *fields: "Field") -> None:
        """Log a pedantic message (short form)."""
        self.pedantic(message, *fields)

    def ayg(self, message: str, *fields: "Field") -> None:
        """Log an annoying message (short form)."""
        self.annoying(message, *fields)

    # Printf-style formatting methods
    def critical_f(self, format_str: str, *args: Any) -> None:
        """Log a critical message with printf-style formatting."""
        if not self._should_log(Level.CRITICAL):
            return
        message = format_str % args
        self.critical(message)

    def error_f(self, format_str: str, *args: Any) -> None:
        """Log an error message with printf-style formatting."""
        if not self._should_log(Level.ERROR):
            return
        message = format_str % args
        self.error(message)

    def warn_f(self, format_str: str, *args: Any) -> None:
        """Log a warning message with printf-style formatting."""
        if not self._should_log(Level.WARN):
            return
        message = format_str % args
        self.warn(message)

    def info_f(self, format_str: str, *args: Any) -> None:
        """Log an info message with printf-style formatting."""
        if not self._should_log(Level.INFO):
            return
        message = format_str % args
        self.info(message)

    def verbose_f(self, format_str: str, *args: Any) -> None:
        """Log a verbose message with printf-style formatting."""
        if not self._should_log(Level.VERBOSE):
            return
        message = format_str % args
        self.verbose(message)

    def trace_f(self, format_str: str, *args: Any) -> None:
        """Log a trace message with printf-style formatting."""
        if not self._should_log(Level.TRACE):
            return
        message = format_str % args
        self.trace(message)

    def debug_f(self, format_str: str, *args: Any) -> None:
        """Log a debug message with printf-style formatting."""
        if not self._should_log(Level.DEBUG):
            return
        message = format_str % args
        self.debug(message)

    def pedantic_f(self, format_str: str, *args: Any) -> None:
        """Log a pedantic message with printf-style formatting."""
        if not self._should_log(Level.PEDANTIC):
            return
        message = format_str % args
        self.pedantic(message)

    def annoying_f(self, format_str: str, *args: Any) -> None:
        """Log an annoying message with printf-style formatting."""
        if not self._should_log(Level.ANNOYING):
            return
        message = format_str % args
        self.annoying(message)

    # Short form printf methods
    def crt_f(self, format_str: str, *args: Any) -> None:
        """Log a critical message with printf-style formatting (short form)."""
        self.critical_f(format_str, *args)

    def err_f(self, format_str: str, *args: Any) -> None:
        """Log an error message with printf-style formatting (short form)."""
        self.error_f(format_str, *args)

    def wrn_f(self, format_str: str, *args: Any) -> None:
        """Log a warning message with printf-style formatting (short form)."""
        self.warn_f(format_str, *args)

    def inf_f(self, format_str: str, *args: Any) -> None:
        """Log an info message with printf-style formatting (short form)."""
        self.info_f(format_str, *args)

    def vrb_f(self, format_str: str, *args: Any) -> None:
        """Log a verbose message with printf-style formatting (short form)."""
        self.verbose_f(format_str, *args)

    def trc_f(self, format_str: str, *args: Any) -> None:
        """Log a trace message with printf-style formatting (short form)."""
        self.trace_f(format_str, *args)

    def dbg_f(self, format_str: str, *args: Any) -> None:
        """Log a debug message with printf-style formatting (short form)."""
        self.debug_f(format_str, *args)

    def ped_f(self, format_str: str, *args: Any) -> None:
        """Log a pedantic message with printf-style formatting (short form)."""
        self.pedantic_f(format_str, *args)

    def ayg_f(self, format_str: str, *args: Any) -> None:
        """Log an annoying message with printf-style formatting (short form)."""
        self.annoying_f(format_str, *args)


# Global configuration functions
def set_level(level: Level) -> None:
    """Set the global minimum log level.

    Messages below this level will be filtered out.
    """
    _config.set_level(level)


def get_level() -> Level:
    """Get the current global minimum log level."""
    return _config.min_level


def set_theme(theme) -> None:
    """Set the global theme for colors and formatting."""
    _config.set_theme(theme)


def get_theme():
    """Get the current global theme."""
    return _config.theme


def get_logger(name: str = "") -> Logger:
    """Create a logger with the given name.

    This is the main entry point for creating loggers.

    Args:
        name: Logger name (optional)

    Returns:
        Logger instance

    Example:
        log = redlog.get_logger("app")
    """
    return Logger(name)
