"""
Theme system for visual appearance and layout.
"""

from dataclasses import dataclass
from enum import IntEnum


class Color(IntEnum):
    """ANSI color codes."""
    NONE = 0
    RED = 31
    GREEN = 32
    YELLOW = 33
    BLUE = 34
    MAGENTA = 35
    CYAN = 36
    WHITE = 37
    BRIGHT_RED = 91
    BRIGHT_GREEN = 92
    BRIGHT_YELLOW = 93
    BRIGHT_BLUE = 94
    BRIGHT_MAGENTA = 95
    BRIGHT_CYAN = 96


@dataclass
class Theme:
    """Theme configuration for visual appearance and layout.
    
    Controls colors for different log levels and message components,
    as well as formatting layout parameters.
    """
    # Colors for each log level
    critical_color: Color = Color.BRIGHT_MAGENTA
    error_color: Color = Color.RED
    warn_color: Color = Color.YELLOW
    info_color: Color = Color.GREEN
    verbose_color: Color = Color.BLUE
    trace_color: Color = Color.WHITE
    debug_color: Color = Color.BRIGHT_CYAN
    pedantic_color: Color = Color.BRIGHT_CYAN
    annoying_color: Color = Color.BRIGHT_CYAN
    
    # Colors for message components
    source_color: Color = Color.CYAN
    message_color: Color = Color.WHITE
    field_key_color: Color = Color.BRIGHT_CYAN
    field_value_color: Color = Color.WHITE
    
    # Layout configuration
    source_width: int = 12        # Fixed width for source names
    message_fixed_width: int = 44 # Fixed width for message field
    pad_level_text: bool = True   # Pad level text for consistent alignment


class _Themes:
    """Collection of predefined themes."""
    
    @property
    def DEFAULT(self) -> Theme:
        """Default colorful theme."""
        return Theme()
    
    @property
    def PLAIN(self) -> Theme:
        """Plain theme with no colors."""
        return Theme(
            critical_color=Color.NONE,
            error_color=Color.NONE,
            warn_color=Color.NONE,
            info_color=Color.NONE,
            verbose_color=Color.NONE,
            trace_color=Color.NONE,
            debug_color=Color.NONE,
            pedantic_color=Color.NONE,
            annoying_color=Color.NONE,
            source_color=Color.NONE,
            message_color=Color.NONE,
            field_key_color=Color.NONE,
            field_value_color=Color.NONE,
        )


# Global themes instance
themes = _Themes()


def set_theme(theme: Theme) -> None:
    """Set the global theme."""
    from .core import _config
    _config.set_theme(theme)


def get_theme() -> Theme:
    """Get the current global theme."""
    from .core import _config
    return _config.theme