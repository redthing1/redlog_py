#!/usr/bin/env python3
"""
Advanced redlog example demonstrating complex scenarios, threading, performance, and real-world patterns.
"""

import threading
import time
from dataclasses import dataclass
from redlog import get_logger, set_level, get_level, Level, field, level_name, fmt


# Custom type with string representation
@dataclass
class CustomObject:
    id: int
    name: str

    def __str__(self):
        return f"CustomObject{{id={self.id}, name={self.name}}}"


# Simulated database class showing practical usage patterns
class DatabaseManager:
    def __init__(self):
        self.log = get_logger("db")
        self.log.info("Database manager initialized")

    def connect(self, host: str, port: int):
        conn_log = self.log.with_field("host", host).with_field("port", port)

        conn_log.info("Attempting connection")

        # Simulate connection logic with potential failure
        if host == "bad-host":
            conn_log.error("Connection failed", field("reason", "host unreachable"))
            raise RuntimeError("Connection failed")

        time.sleep(0.1)  # Simulate connection time
        conn_log.info("Connected successfully")

    def execute_query(self, sql: str):
        query_id = getattr(self, "_query_id", 0) + 1
        setattr(self, "_query_id", query_id)

        query_log = self.log.with_name("query").with_field("query_id", query_id)

        query_log.trace("Executing query", field("sql", sql))

        start_time = time.time()

        # Simulate query execution
        time.sleep(0.05)

        duration_ms = int((time.time() - start_time) * 1000)

        query_log.debug_f("Query completed in %d ms, affected %d rows", duration_ms, 42)
        query_log.trace(
            "Query performance", field("duration_ms", duration_ms), field("rows_affected", 42)
        )


# HTTP request simulation showing context propagation
@dataclass
class HttpRequest:
    method: str
    path: str
    client_ip: str
    request_id: int


def handle_http_request(req: HttpRequest):
    request_log = (
        get_logger("http")
        .with_field("method", req.method)
        .with_field("path", req.path)
        .with_field("request_id", req.request_id)
        .with_field("client_ip", req.client_ip)
    )

    request_log.info("Request started")

    try:
        # Simulate request processing
        if req.path == "/api/users":
            db_log = request_log.with_name("db")
            db = DatabaseManager()
            db.connect("localhost", 5432)
            db.execute_query("SELECT * FROM users")

            request_log.info_f("Request completed: %d status, %d bytes", 200, 1024)
            request_log.debug(
                "Response details", field("status_code", 200), field("response_size", 1024)
            )

        elif req.path == "/api/error":
            raise RuntimeError("Simulated error")

        else:
            request_log.warn_f("Unknown endpoint: %s (status %d)", req.path, 404)

    except Exception as e:
        request_log.error_f("Request failed with status %d: %s", 500, str(e))
        request_log.debug("Error details", field("error", str(e)), field("status_code", 500))


# Thread safety demonstration
def worker_thread(thread_id: int):
    log = get_logger("worker").with_field("thread_id", thread_id)

    # Different threads demonstrate different verbosity levels
    if thread_id % 4 == 0:
        log.info("Worker thread started (using INFO level)")
    elif thread_id % 4 == 1:
        log.verbose("Worker thread started (using VERBOSE level)")
    elif thread_id % 4 == 2:
        log.debug("Worker thread started (using DEBUG level)")
    else:
        log.trace("Worker thread started (using TRACE level)")

    for i in range(5):
        if thread_id % 4 == 0:
            log.info("Processing item", field("item", i))
        elif thread_id % 4 == 1:
            log.verbose(
                "Processing item with verbose details",
                field("item", i),
                field("memory_mb", 128 + i * 10),
            )
        elif thread_id % 4 == 2:
            log.debug(
                "Processing item with debug info",
                field("item", i),
                field("cpu_percent", 15.5 + i * 2.1),
            )
        else:
            log.trace(
                "Processing item with trace details",
                field("item", i),
                field("timestamp", int(time.time() * 1000)),
            )

        time.sleep(0.01)

    if thread_id % 4 == 0:
        log.info("Worker thread completed")
    elif thread_id % 4 == 1:
        log.verbose("Worker thread completed with all items processed")
    elif thread_id % 4 == 2:
        log.debug("Worker thread completed - releasing resources")
    else:
        log.trace("Worker thread completed - execution trace finished")


def main():
    print("=== redlog Advanced Example ===")
    print("Demonstrating complex scenarios, threading, performance, and real-world patterns")

    log = get_logger("advanced")

    # Start with info level to show basic scenarios
    print(f"\n--- Starting with INFO level ---")
    print(f"Current level: {level_name(get_level())} ({get_level().value})")

    log.info("Advanced example started - demonstrating complex patterns")

    # Custom type logging
    obj = CustomObject(123, "test_object")
    log.info("Custom object logging", field("object", obj))

    # Using the general fmt function for string formatting
    status_msg = fmt("System ready: %d cores, %dMB RAM, %.1f%% disk free", 8, 16384, 67.3)
    log.info("System status", field("status", status_msg))

    # Enable debug level to show detailed internal operations
    print(f"\n--- Enabling DEBUG level for detailed logging ---")
    set_level(Level.DEBUG)
    print(f"Current level: {level_name(get_level())} ({get_level().value})")

    # Now show all relevant log levels with realistic scenarios
    log.critical("System overload detected - immediate intervention required")
    log.error("Database connection lost - attempting reconnection")
    log.warn("High memory usage detected - consider scaling")
    log.info("User session established")
    log.verbose("Detailed request processing information")
    log.trace("Function call trace: process_request() entered")
    log.debug("Variable state: connection_count=42, active_sessions=15")

    # Printf-style formatting demonstrations
    log.info_f("Server stats: %d connections, %.1f%% CPU usage", 42, 85.7)
    log.debug_f("Memory address: 0x%x, hex value: 0x%x", id(obj), 0xDEADBEEF)
    log.verbose_f("Process ID: %d, thread count: %d", 1234, 8)
    log.trace_f("Precision test: %.0f, %.2f, %.5f", 3.14159, 3.14159, 3.14159)

    # Enable maximum verbosity to show extreme debugging levels
    print(f"\n--- Enabling ANNOYING level (maximum verbosity) ---")
    set_level(Level.ANNOYING)
    print(f"Current level: {level_name(get_level())} (shows everything)")

    log.pedantic("Memory allocation details: 1024 bytes allocated at 0x7fff")
    log.annoying("Micro-optimization: loop iteration 573 of 10000")

    # Demonstrate level filtering effects
    print(f"\n--- Demonstrating level filtering effects ---")
    print("Setting to WARN level (restrictive)")
    set_level(Level.WARN)

    log.critical("Critical: Still visible at WARN level")
    log.error("Error: Still visible at WARN level")
    log.warn("Warning: Still visible at WARN level")
    log.info("Info: Should not appear at WARN level")
    log.verbose("Verbose: Should not appear at WARN level")
    log.debug("Debug: Should not appear at WARN level")

    # Reset to verbose for detailed demo
    print(f"\n--- Setting to VERBOSE level for detailed operations ---")
    set_level(Level.VERBOSE)
    print(f"Current level: {level_name(get_level())} ({get_level().value})")

    # HTTP request simulation
    print(f"\n--- HTTP request simulation with scoped logging ---")
    requests = [
        HttpRequest("GET", "/api/users", "192.168.1.100", 1001),
        HttpRequest("POST", "/api/users", "192.168.1.101", 1002),
        HttpRequest("GET", "/api/error", "192.168.1.102", 1003),
        HttpRequest("GET", "/unknown", "192.168.1.103", 1004),
    ]

    for req in requests:
        handle_http_request(req)

    # Thread safety demonstration with different verbosity per thread
    print(f"\n--- Thread safety demonstration ---")
    log.verbose("Starting multi-threaded logging with different verbosity levels")

    threads = []
    for i in range(3):
        thread = threading.Thread(target=worker_thread, args=(i,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    # Performance comparison at different verbosity levels
    print(f"\n--- Performance impact of verbosity levels ---")
    log.verbose("Testing performance impact of level filtering")

    iterations = 1000  # Smaller number for demo purposes

    # Test with very restrictive filtering (only critical/error)
    print("Testing with ERROR level (most restrictive)")
    set_level(Level.ERROR)
    start_time = time.time()

    for i in range(iterations):
        if i < 5:
            log.debug("Filtered debug message", field("iteration", i))
            log.verbose("Filtered verbose message", field("iteration", i))
            log.info("Filtered info message", field("iteration", i))

    restrictive_time = time.time() - start_time

    # Test with moderate filtering (info and above)
    print("Testing with INFO level (moderate filtering)")
    set_level(Level.INFO)
    start_time = time.time()

    for i in range(iterations):
        if i < 5:
            log.debug("Filtered debug message", field("iteration", i))
            log.verbose("Filtered verbose message", field("iteration", i))
            log.info("Enabled info message", field("iteration", i))

    moderate_time = time.time() - start_time

    # Test with maximum verbosity (all messages enabled)
    print("Testing with ANNOYING level (maximum verbosity)")
    set_level(Level.ANNOYING)
    start_time = time.time()

    for i in range(iterations):
        if i < 5:
            log.debug("Enabled debug message", field("iteration", i))
            log.verbose("Enabled verbose message", field("iteration", i))
            log.info("Enabled info message", field("iteration", i))

    verbose_time = time.time() - start_time

    # Reset to info level for final summary
    print(f"\n--- Performance results ---")
    set_level(Level.INFO)
    print(f"Current level: {level_name(get_level())} (for results display)")

    log.info(
        "Performance comparison completed",
        field("iterations", iterations),
        field("restrictive_time_us", int(restrictive_time * 1_000_000)),
        field("moderate_time_us", int(moderate_time * 1_000_000)),
        field("verbose_time_us", int(verbose_time * 1_000_000)),
    )

    log.info("Performance analysis shows significant speedup with level filtering")

    print(f"\n=== Advanced example completed! ===")
    print("Key takeaways:")
    print("- Level filtering provides major performance benefits")
    print("- Scoped loggers enable contextual logging")
    print("- Thread-safe by design for concurrent applications")


if __name__ == "__main__":
    main()
