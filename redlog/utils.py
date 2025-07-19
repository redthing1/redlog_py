"""
Utility functions for redlog.
"""

import os
import sys
from typing import Any


def stringify(value: Any) -> str:
    """Universal type-to-string conversion.
    
    Tries multiple approaches in order:
    1. Direct string types
    2. None handling
    3. Arithmetic types (using str())
    4. Types with __str__ (custom types can implement this)
    5. Fallback for unprintable types
    """
    if value is None:
        return "null"
    elif isinstance(value, str):
        return value
    elif isinstance(value, (int, float, bool)):
        return str(value)
    else:
        try:
            return str(value)
        except Exception:
            return "[unprintable]"


def should_use_color() -> bool:
    """Simple TTY and color detection."""
    # Check environment variables first
    if os.getenv("NO_COLOR") or os.getenv("REDLOG_NO_COLOR"):
        return False
    if os.getenv("FORCE_COLOR") or os.getenv("REDLOG_FORCE_COLOR"):
        return True
    
    # Check if stderr is a TTY
    return hasattr(sys.stderr, 'isatty') and sys.stderr.isatty()


def colorize(text: str, fg_color: int, bg_color: int = 0) -> str:
    """Apply ANSI color formatting to text.
    
    Args:
        text: Text to colorize
        fg_color: Foreground color code (0 for none)
        bg_color: Background color code (0 for none)
        
    Returns:
        Colorized text or original text if colors disabled
    """
    if not should_use_color() or (fg_color == 0 and bg_color == 0):
        return text
    
    escape_seq = "\033["
    codes = []
    
    if fg_color != 0:
        codes.append(str(fg_color))
    
    if bg_color != 0:
        codes.append(str(bg_color))
    
    if not codes:
        return text
    
    escape_seq += ";".join(codes) + "m"
    return f"{escape_seq}{text}\033[0m"


def fmt(format_str: str, *args: Any) -> str:
    """General-purpose string formatting using Python's % operator.
    
    Args:
        format_str: Format string with % placeholders
        *args: Arguments to format
        
    Returns:
        Formatted string
        
    Example:
        msg = fmt("User %s has %d points (%.1f%%)", name, score, percentage)
    """
    try:
        return format_str % args
    except (TypeError, ValueError):
        return "[format_error]"