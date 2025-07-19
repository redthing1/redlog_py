"""
Formatter system for customizable output.
"""

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from .core import Level, level_short_name
from .themes import Color, Theme, get_theme
from .utils import colorize

if TYPE_CHECKING:
    from .core import LogEntry


class Formatter(ABC):
    """Formatter interface for customizable output."""

    @abstractmethod
    def format(self, entry: "LogEntry") -> str:
        """Format a log entry into a string.

        Args:
            entry: The log entry to format

        Returns:
            Formatted string
        """
        pass


class DefaultFormatter(Formatter):
    """Default formatter producing beautiful aligned output.

    Format: [source]      [lvl] message                    key=value key=value
    """

    def __init__(self, theme: Theme = None) -> None:
        self.theme = theme or get_theme()

    def _level_color(self, level: Level) -> Color:
        """Get the color for a specific log level."""
        color_map = {
            Level.CRITICAL: self.theme.critical_color,
            Level.ERROR: self.theme.error_color,
            Level.WARN: self.theme.warn_color,
            Level.INFO: self.theme.info_color,
            Level.VERBOSE: self.theme.verbose_color,
            Level.TRACE: self.theme.trace_color,
            Level.DEBUG: self.theme.debug_color,
            Level.PEDANTIC: self.theme.pedantic_color,
            Level.ANNOYING: self.theme.annoying_color,
        }
        return color_map.get(level, Color.WHITE)

    def _level_bg_color(self, level: Level) -> Color:
        """Get the background color for a specific log level."""
        color_map = {
            Level.CRITICAL: self.theme.critical_bg_color,
            Level.ERROR: self.theme.error_bg_color,
            Level.WARN: self.theme.warn_bg_color,
            Level.INFO: self.theme.info_bg_color,
            Level.VERBOSE: self.theme.verbose_bg_color,
            Level.TRACE: self.theme.trace_bg_color,
            Level.DEBUG: self.theme.debug_bg_color,
            Level.PEDANTIC: self.theme.pedantic_bg_color,
            Level.ANNOYING: self.theme.annoying_bg_color,
        }
        return color_map.get(level, Color.NONE)

    def _get_max_level_text_width(self) -> int:
        """Get the maximum width needed for level text with brackets."""
        max_width = 0
        for level in Level:
            width = len(level_short_name(level)) + 2  # +2 for brackets []
            max_width = max(max_width, width)
        return max_width

    def format(self, entry: "LogEntry") -> str:
        """Format a log entry with beautiful alignment."""
        parts = []

        # Source component with fixed width padding
        if entry.source:
            source_part = f"[{entry.source}]"
            parts.append(colorize(source_part, self.theme.source_color, self.theme.source_bg_color))

            padding = self.theme.source_width - len(source_part)
            if padding > 0:
                parts.append(" " * padding)
            else:
                parts.append(" ")
        else:
            parts.append(" " * self.theme.source_width)

        # Level component with optional padding
        level_text = level_short_name(entry.level)
        level_part = f"[{level_text}]"

        if self.theme.pad_level_text:
            target_width = self._get_max_level_text_width()
            padding = target_width - len(level_part)
            if padding > 0:
                level_part += " " * padding

        parts.append(
            colorize(level_part, self._level_color(entry.level), self._level_bg_color(entry.level))
        )
        parts.append(" ")

        # Message component with fixed width
        message_colored = colorize(entry.message, self.theme.message_color)
        if self.theme.message_fixed_width > 0:
            # Pad message to fixed width (accounting for invisible color codes)
            message_display_len = len(entry.message)
            padding = max(1, self.theme.message_fixed_width - message_display_len)
            parts.append(message_colored + " " * padding)
        else:
            parts.append(message_colored)

        # Fields component
        if not entry.fields.empty():
            field_parts = []
            for field in entry.fields:
                key_colored = colorize(field.key, self.theme.field_key_color)
                value_colored = colorize(field.value, self.theme.field_value_color)
                field_parts.append(f"{key_colored}={value_colored}")

            if field_parts:
                parts.append(" ")
                parts.append(" ".join(field_parts))

        return "".join(parts)


class PlainFormatter(Formatter):
    """Simple plain text formatter without colors."""

    def format(self, entry: "LogEntry") -> str:
        """Format a log entry as plain text."""
        parts = []

        if entry.source:
            parts.append(f"[{entry.source}]")

        parts.append(f"[{level_short_name(entry.level)}]")
        parts.append(entry.message)

        if not entry.fields.empty():
            field_parts = []
            for field in entry.fields:
                field_parts.append(f"{field.key}={field.value}")
            if field_parts:
                parts.append(" ".join(field_parts))

        return " ".join(parts)


class TimestampedFormatter(Formatter):
    """Formatter that adds timestamps to log entries."""

    def __init__(self, theme: Theme = None) -> None:
        self.theme = theme or get_theme()

    def _level_color(self, level: Level) -> Color:
        """Get the color for a specific log level."""
        color_map = {
            Level.CRITICAL: self.theme.critical_color,
            Level.ERROR: self.theme.error_color,
            Level.WARN: self.theme.warn_color,
            Level.INFO: self.theme.info_color,
            Level.VERBOSE: self.theme.verbose_color,
            Level.TRACE: self.theme.trace_color,
            Level.DEBUG: self.theme.debug_color,
            Level.PEDANTIC: self.theme.pedantic_color,
            Level.ANNOYING: self.theme.annoying_color,
        }
        return color_map.get(level, Color.WHITE)

    def format(self, entry: "LogEntry") -> str:
        """Format a log entry with timestamp."""
        parts = []

        # Add timestamp
        timestamp_str = entry.timestamp.strftime("%H:%M:%S")
        parts.append(f"[{timestamp_str}]")

        # Source component
        if entry.source:
            source_colored = colorize(
                entry.source, self.theme.source_color, self.theme.source_bg_color
            )
            parts.append(source_colored)

        # Level component
        level_text = level_short_name(entry.level)
        level_colored = colorize(level_text, self._level_color(entry.level))
        parts.append(f"{level_colored}:")

        # Message
        message_colored = colorize(entry.message, self.theme.message_color)
        parts.append(message_colored)

        # Fields
        if not entry.fields.empty():
            field_parts = []
            for field in entry.fields:
                key_colored = colorize(field.key, self.theme.field_key_color)
                value_colored = colorize(field.value, self.theme.field_value_color)
                field_parts.append(f"{key_colored}={value_colored}")

            if field_parts:
                parts.append(f"[{', '.join(field_parts)}]")

        return " ".join(parts)


class JSONFormatter(Formatter):
    """JSON-style formatter for structured logging."""

    def format(self, entry: "LogEntry") -> str:
        """Format a log entry as JSON."""
        import json

        data = {
            "timestamp": entry.timestamp.isoformat(),
            "level": entry.level.name.lower(),
            "source": entry.source,
            "message": entry.message,
        }

        if not entry.fields.empty():
            fields_dict = {}
            for field in entry.fields:
                fields_dict[field.key] = field.value
            data["fields"] = fields_dict

        return json.dumps(data, separators=(",", ":"))
