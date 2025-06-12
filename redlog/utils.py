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


def colorize(text: str, color_code: int) -> str:
    """Apply ANSI color formatting to text."""
    if not should_use_color() or color_code == 0:
        return text
    return f"\033[{color_code}m{text}\033[0m"


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