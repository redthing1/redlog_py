#!/usr/bin/env python3
"""
Basic redlog example demonstrating core functionality.
"""

import time
from redlog import get_logger, set_level, get_level, Level, field, level_name


def main():
    print("=== redlog Basic Example ===")
    print("Demonstrating different log levels, verbosity filtering, and features")

    # Create our main logger
    log = get_logger("example")

    # Start with default level (info) to show basic usage
    print(f"\n--- Basic logging at INFO level (default) ---")
    print(f"Current level: {level_name(get_level())} ({get_level().value})")

    log.critical("Critical system error - immediate attention required")
    log.error("Error occurred during processing")
    log.warn("Warning: deprecated API usage detected")
    log.info("Application started successfully")
    log.verbose("Verbose - will not appear (filtered out)")
    log.debug("Debug - will not appear (filtered out)")

    # Demonstrate structured logging with fields
    print(f"\n--- Structured logging with fields ---")
    log.info(
        "User login attempt",
        field("username", "alice"),
        field("ip_address", "192.168.1.100"),
        field("success", True),
    )

    log.info(
        "Data types example",
        field("string", "hello world"),
        field("integer", 42),
        field("float", 3.14159),
        field("boolean", False),
    )

    # Demonstrate scoped loggers
    print(f"\n--- Scoped loggers ---")
    db_log = log.with_name("database")
    db_log.info("Database connection established")

    request_log = log.with_field("request_id", 12345).with_field("method", "GET")
    request_log.info("Request started", field("path", "/api/users"))
    request_log.info("Request completed", field("status", 200), field("duration_ms", 150))

    # Demonstrate printf-style formatting
    print(f"\n--- Printf-style formatting ---")
    log.info_f("Server listening on port %d", 8080)
    log.error_f("Failed to connect to %s:%d", "database.example.com", 5432)
    log.info_f("Processing %d items with %.1f%% efficiency", 42, 95.7)

    # Now demonstrate enabling debug level to see more messages
    print(f"\n--- Enabling DEBUG level (shows verbose, trace, debug) ---")
    set_level(Level.DEBUG)
    print(f"Current level: {level_name(get_level())} ({get_level().value})")

    log.critical("Critical still visible")
    log.error("Error still visible")
    log.warn("Warning still visible")
    log.info("Info still visible")
    log.verbose("Verbose now visible!")
    log.trace("Trace now visible!")
    log.debug("Debug now visible!")
    log.pedantic("Pedantic - still filtered (level 7 > 6)")

    # Show short form methods
    print(f"\n--- Short form methods ---")
    log.crt("Critical using short form")
    log.err("Error using short form")
    log.inf("Info using short form")
    log.dbg("Debug using short form")

    # Demonstrate more restrictive filtering
    print(f"\n--- Setting to WARN level (only critical, error, warn) ---")
    set_level(Level.WARN)
    print(f"Current level: {level_name(get_level())} ({get_level().value})")

    log.critical("Critical still visible")
    log.error("Error still visible")
    log.warn("Warning still visible")
    log.info("Info - now filtered out")
    log.debug("Debug - now filtered out")

    # Demonstrate performance of filtered messages
    print(f"\n--- Performance test with filtered messages ---")
    print("Testing 10,000 debug calls (should be very fast since they're filtered)")

    start_time = time.time()
    for i in range(10000):
        log.debug("This debug message is filtered out", field("iteration", i))
    end_time = time.time()

    # Reset to info to show performance results
    set_level(Level.INFO)
    duration_us = int((end_time - start_time) * 1_000_000)
    log.info(
        "Performance test completed",
        field("iterations", 10000),
        field("total_time_us", duration_us),
        field("avg_time_ns", duration_us * 1000 // 10000),
    )

    # Show all levels with printf formatting
    print(f"\n--- All log levels with printf formatting ---")
    set_level(Level.ANNOYING)  # Enable all levels
    print(f"Current level: {level_name(get_level())} (shows all levels)")

    log.critical_f("Critical: System has %d critical errors", 3)
    log.error_f("Error: Failed to process %d/%d items", 5, 100)
    log.warn_f("Warning: Memory usage at %.1f%% capacity", 85.7)
    log.info_f("Info: Processing batch %d of %d", 7, 10)
    log.verbose_f("Verbose: Thread pool has %d active workers", 8)
    log.trace_f("Trace: Function entry with parameter 0x%x", 0xDEADBEEF)
    log.debug_f("Debug: Variable state - counter=%d, flag=%c", 42, ord("Y"))
    log.pedantic_f("Pedantic: Detailed timing - %.3f seconds elapsed", 1.234567)
    log.annoying_f("Annoying: Buffer state - %o octal representation", 0o755)

    print(f"\n=== Example completed! ===")
    print("Try setting NO_COLOR=1 to disable colors")


if __name__ == "__main__":
    main()
