#!/usr/bin/env python3
"""
Comprehensive themes and formatting demonstration.
"""

import os
from dataclasses import dataclass
from redlog import (
    get_logger,
    set_level,
    set_theme,
    get_theme,
    Level,
    field,
    level_name,
    Theme,
    Color,
    themes,
    DefaultFormatter,
    TimestampedFormatter,
    JSONFormatter,
    StringSink,
    ConsoleSink,
    Logger,
)


@dataclass
class ServerStats:
    connections: int
    cpu_usage: float
    memory_mb: int

    def __str__(self):
        return (
            f"ServerStats{{conn={self.connections}, cpu={self.cpu_usage}%, mem={self.memory_mb}MB}}"
        )


def create_cyberpunk_theme() -> Theme:
    """Cyberpunk-style theme with bright neon colors."""
    return Theme(
        critical_color=Color.BRIGHT_RED,
        error_color=Color.RED,
        warn_color=Color.BRIGHT_YELLOW,
        info_color=Color.BRIGHT_CYAN,
        verbose_color=Color.CYAN,
        trace_color=Color.BRIGHT_BLUE,
        debug_color=Color.BRIGHT_MAGENTA,
        pedantic_color=Color.MAGENTA,
        annoying_color=Color.BRIGHT_GREEN,
        source_color=Color.YELLOW,
        message_color=Color.WHITE,
        field_key_color=Color.BRIGHT_CYAN,
        field_value_color=Color.WHITE,
        source_width=12,
        message_fixed_width=50,
    )


def create_retro_green_theme() -> Theme:
    """Retro green terminal theme."""
    return Theme(
        critical_color=Color.BRIGHT_GREEN,
        error_color=Color.BRIGHT_GREEN,
        warn_color=Color.GREEN,
        info_color=Color.GREEN,
        verbose_color=Color.GREEN,
        trace_color=Color.GREEN,
        debug_color=Color.GREEN,
        pedantic_color=Color.GREEN,
        annoying_color=Color.GREEN,
        source_color=Color.BRIGHT_GREEN,
        message_color=Color.GREEN,
        field_key_color=Color.BRIGHT_GREEN,
        field_value_color=Color.GREEN,
        source_width=16,
        message_fixed_width=40,
    )


def create_high_contrast_theme() -> Theme:
    """High-contrast theme for accessibility."""
    return Theme(
        critical_color=Color.WHITE,
        error_color=Color.WHITE,
        warn_color=Color.WHITE,
        info_color=Color.WHITE,
        verbose_color=Color.WHITE,
        trace_color=Color.WHITE,
        debug_color=Color.WHITE,
        pedantic_color=Color.WHITE,
        annoying_color=Color.WHITE,
        source_color=Color.WHITE,
        message_color=Color.WHITE,
        field_key_color=Color.WHITE,
        field_value_color=Color.WHITE,
        source_width=20,
        message_fixed_width=60,
    )


def demonstrate_default_theme():
    print("\n=== Default Theme ===")

    log = get_logger("default")

    # Set to show all levels
    set_level(Level.ANNOYING)

    log.critical("System failure detected!")
    log.error("Database connection failed")
    log.warn("High memory usage detected")
    log.info("User authentication successful")
    log.verbose("Detailed operation information")
    log.trace("Function entry: authenticate_user()")
    log.debug("Variable state: user_id=12345, session_active=true")
    log.pedantic("Memory allocation: 1024 bytes at address 0x7fff")
    log.annoying("Loop iteration 42 of 10000 completed")

    # With fields
    log.info(
        "Server statistics",
        field("uptime_hours", 72),
        field("active_users", 1543),
        field("memory_usage", "67.3%"),
    )


def demonstrate_plain_theme():
    print("\n=== Plain Theme ===")

    # Switch to plain theme
    original_theme = get_theme()
    set_theme(themes.PLAIN)

    log = get_logger("plain")

    log.critical("System failure detected!")
    log.error("Database connection failed")
    log.warn("High memory usage detected")
    log.info("User authentication successful")
    log.verbose("Detailed operation information")
    log.debug("Variable state: user_id=12345, session_active=true")

    log.info("Server statistics", field("uptime_hours", 72), field("active_users", 1543))

    # Restore original theme
    set_theme(original_theme)


def demonstrate_custom_themes():
    print("\n=== Custom Themes ===")

    # Store original theme
    original_theme = get_theme()

    def generate_theme_samples(theme_name: str):
        log = get_logger(theme_name)
        log.critical("System critical alert")
        log.error("Database connection failed")
        log.warn("High memory usage detected")
        log.info("User login successful", field("user", "alice"), field("ip", "192.168.1.100"))
        log.verbose("Detailed operation trace")
        log.debug("Variable state inspection", field("count", 42), field("active", True))

    # Cyberpunk theme demonstration
    print("\n--- Cyberpunk Theme ---")
    set_theme(create_cyberpunk_theme())
    generate_theme_samples("cyberpunk")

    # Retro green theme demonstration
    print("\n--- Retro Green Theme ---")
    set_theme(create_retro_green_theme())
    generate_theme_samples("retro")

    # High contrast theme demonstration
    print("\n--- High Contrast Theme ---")
    set_theme(create_high_contrast_theme())
    generate_theme_samples("accessible")

    # Restore original theme
    set_theme(original_theme)


def demonstrate_custom_formatters():
    print("\n=== Custom Formatters ===")

    def generate_formatter_samples(logger: Logger, name: str):
        logger.error(
            "Database connection failed",
            field("host", "db.prod.example.com"),
            field("port", 5432),
            field("timeout_ms", 5000),
            field("retry_count", 3),
        )

        logger.info(
            "User session created",
            field("user_id", "user_12345"),
            field("session_token", "abc123..."),
            field("ip_address", "203.0.113.45"),
            field("user_agent", "Chrome/96.0"),
        )

        logger.warn(
            "Rate limit approaching",
            field("current_rate", "450/min"),
            field("limit", "500/min"),
            field("client_id", "api_client_7"),
        )

    # Timestamped formatter demonstration
    print("\n--- Timestamped Formatter ---")
    string_sink = StringSink()
    timestamped_formatter = TimestampedFormatter()
    logger = Logger("timestamps", timestamped_formatter, string_sink)

    generate_formatter_samples(logger, "timestamped")
    print(string_sink.get_output())
    string_sink.clear()

    # JSON formatter demonstration
    print("\n--- JSON Formatter ---")
    json_formatter = JSONFormatter()
    logger = Logger("json", json_formatter, string_sink)

    generate_formatter_samples(logger, "json")
    print(string_sink.get_output())


def demonstrate_environment_variables():
    print("\n=== Environment Variable Configuration ===")
    print("redlog respects environment variables for configuration")

    log = get_logger("env-demo")

    # Check if colors should be disabled
    print("\nColor detection:")
    print(f"- NO_COLOR: {'set (colors disabled)' if os.getenv('NO_COLOR') else 'not set'}")
    print(
        f"- REDLOG_NO_COLOR: {'set (colors disabled)' if os.getenv('REDLOG_NO_COLOR') else 'not set'}"
    )
    print(f"- FORCE_COLOR: {'set (colors forced)' if os.getenv('FORCE_COLOR') else 'not set'}")
    print(
        f"- REDLOG_FORCE_COLOR: {'set (colors forced)' if os.getenv('REDLOG_FORCE_COLOR') else 'not set'}"
    )

    from redlog.utils import should_use_color

    print(f"- TTY detected: {'yes' if should_use_color() else 'no'}")

    log.info("Environment variable demo")
    log.warn("Colors should respect environment settings")

    print("\nTo test environment variables, try:")
    print("  NO_COLOR=1 python examples/themes.py")
    print("  REDLOG_FORCE_COLOR=1 python examples/themes.py")


def demonstrate_printf_formatting():
    print("\n=== Printf Formatting Examples ===")

    log = get_logger("printf-demo")

    # Integer formats
    print("\n--- Integer Formatting ---")
    log.info_f("Decimal: %d, %i", 42, -123)
    log.info_f("Hexadecimal: %x (lower), %X (upper)", 255, 255)
    log.info_f("Octal: %o", 64)

    # Floating point formats
    print("\n--- Floating Point Formatting ---")
    log.info_f("Default float: %f", 3.14159)
    log.info_f("Precision: %.2f, %.5f", 3.14159, 3.14159)
    log.info_f("Scientific: %e, %E", 1234.5, 1234.5)

    # String formats
    print("\n--- String Formatting ---")
    log.info_f("String: %s", "Hello, World!")
    log.info_f("Character: %c", ord("A"))

    # Custom types
    print("\n--- Custom Type Formatting ---")
    stats = ServerStats(42, 67.8, 1024)
    log.info_f("Custom object: %s", stats)

    # Complex mixed formatting
    print("\n--- Complex Mixed Formatting ---")
    log.info_f(
        "Server %s:%d status: %.1f%% CPU, 0x%04X memory pages, %03o permissions",
        "web-server-01",
        8080,
        85.7,
        256,
        0o755,
    )


def main():
    print("=== Themes and Formatting Demonstration ===")

    # Set initial level to show most messages
    set_level(Level.DEBUG)

    # Run demonstrations
    demonstrate_default_theme()
    demonstrate_plain_theme()
    demonstrate_custom_themes()
    demonstrate_custom_formatters()
    demonstrate_printf_formatting()
    demonstrate_environment_variables()


if __name__ == "__main__":
    main()
