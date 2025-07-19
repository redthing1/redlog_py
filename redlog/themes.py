"""
Theme system for visual appearance and layout.
"""

from dataclasses import dataclass
from enum import IntEnum


class Color(IntEnum):
    """ANSI color codes."""
    NONE = 0
    # Foreground colors
    RED = 31
    GREEN = 32
    YELLOW = 33
    BLUE = 34
    MAGENTA = 35
    CYAN = 36
    WHITE = 37
    BRIGHT_BLACK = 90
    BRIGHT_RED = 91
    BRIGHT_GREEN = 92
    BRIGHT_YELLOW = 93
    BRIGHT_BLUE = 94
    BRIGHT_MAGENTA = 95
    BRIGHT_CYAN = 96
    BRIGHT_WHITE = 97
    # Background colors
    ON_RED = 41
    ON_GREEN = 42
    ON_YELLOW = 43
    ON_BLUE = 44
    ON_MAGENTA = 45
    ON_CYAN = 46
    ON_WHITE = 47
    ON_GRAY = 100
    ON_BRIGHT_RED = 101
    ON_BRIGHT_GREEN = 102
    ON_BRIGHT_YELLOW = 103
    ON_BRIGHT_BLUE = 104
    ON_BRIGHT_MAGENTA = 105
    ON_BRIGHT_CYAN = 106
    ON_BRIGHT_WHITE = 107


@dataclass
class Theme:
    """Theme configuration for visual appearance and layout.
    
    Controls colors for different log levels and message components,
    as well as formatting layout parameters.
    """
    # Foreground colors for each log level
    critical_color: Color = Color.BRIGHT_MAGENTA
    error_color: Color = Color.RED
    warn_color: Color = Color.YELLOW
    info_color: Color = Color.GREEN
    verbose_color: Color = Color.BLUE
    trace_color: Color = Color.WHITE
    debug_color: Color = Color.BRIGHT_BLACK
    pedantic_color: Color = Color.BRIGHT_BLACK
    annoying_color: Color = Color.BRIGHT_BLACK
    
    # Background colors for each log level
    critical_bg_color: Color = Color.NONE
    error_bg_color: Color = Color.NONE
    warn_bg_color: Color = Color.NONE
    info_bg_color: Color = Color.NONE
    verbose_bg_color: Color = Color.NONE
    trace_bg_color: Color = Color.NONE
    debug_bg_color: Color = Color.NONE
    pedantic_bg_color: Color = Color.NONE
    annoying_bg_color: Color = Color.NONE
    
    # Colors for message components
    source_color: Color = Color.CYAN
    source_bg_color: Color = Color.NONE
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
            critical_bg_color=Color.NONE,
            error_bg_color=Color.NONE,
            warn_bg_color=Color.NONE,
            info_bg_color=Color.NONE,
            verbose_bg_color=Color.NONE,
            trace_bg_color=Color.NONE,
            debug_bg_color=Color.NONE,
            pedantic_bg_color=Color.NONE,
            annoying_bg_color=Color.NONE,
            source_color=Color.NONE,
            source_bg_color=Color.NONE,
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