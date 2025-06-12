#!/usr/bin/env python3
"""
Performance testing and benchmarking for redlog.
"""

import time
from redlog import get_logger, set_level, Level, field


class Benchmark:
    """Simple benchmark utility."""
    
    def __init__(self):
        self.start_time = time.time()
    
    def elapsed_ns(self) -> int:
        """Get elapsed time in nanoseconds."""
        return int((time.time() - self.start_time) * 1_000_000_000)
    
    def elapsed_us(self) -> int:
        """Get elapsed time in microseconds."""
        return self.elapsed_ns() // 1000
    
    def elapsed_ms(self) -> int:
        """Get elapsed time in milliseconds."""
        return self.elapsed_us() // 1000


def main():
    log = get_logger("perf")
    log.info("Performance testing started")
    
    iterations = 1_000_000
    
    # Test 1: Disabled level overhead
    print("\n--- Test 1: Disabled Level Overhead ---")
    set_level(Level.WARN)  # Disable info and debug
    bench = Benchmark()
    
    for i in range(iterations):
        log.debug("Disabled message")
    
    log.info(
        "Disabled level test completed",
        field("iterations", iterations),
        field("total_time_us", bench.elapsed_us()),
        field("avg_time_ns", bench.elapsed_ns() // iterations)
    )
    
    # Test 2: Simple message logging
    print("\n--- Test 2: Simple Message Logging ---")
    set_level(Level.INFO)
    bench = Benchmark()
    
    test_iterations = 100  # Much fewer iterations since these actually log
    for i in range(test_iterations):
        log.info("Simple message")
    
    log.info(
        "Simple message test completed",
        field("iterations", test_iterations),
        field("total_time_us", bench.elapsed_us()),
        field("avg_time_ns", bench.elapsed_ns() // test_iterations)
    )
    
    # Test 3: Message with fields
    print("\n--- Test 3: Messages with Fields ---")
    bench = Benchmark()
    
    for i in range(test_iterations):
        log.info("Message with fields", field("id", i), field("name", "test"), field("value", 3.14))
    
    log.info(
        "Fields test completed",
        field("iterations", test_iterations),
        field("total_time_us", bench.elapsed_us()),
        field("avg_time_ns", bench.elapsed_ns() // test_iterations)
    )
    
    # Test 4: Logger creation and scoping
    print("\n--- Test 4: Logger Creation and Scoping ---")
    bench = Benchmark()
    
    for i in range(test_iterations):
        scoped_log = log.with_name("scoped").with_field("iteration", i)
        scoped_log.info("Scoped message")
    
    log.info(
        "Logger scoping test completed",
        field("iterations", test_iterations),
        field("total_time_us", bench.elapsed_us()),
        field("avg_time_ns", bench.elapsed_ns() // test_iterations)
    )
    
    # Test 5: Printf vs structured logging comparison
    print("\n--- Test 5: Printf vs Structured Logging ---")
    printf_iterations = 10
    
    # Printf-style
    bench = Benchmark()
    for i in range(printf_iterations):
        log.info_f("Printf style: %s %s %s", i, "test", 3.14)
    printf_time = bench.elapsed_us()
    
    # Structured logging
    bench = Benchmark()
    for i in range(printf_iterations):
        log.info("Structured style", field("id", i), field("name", "test"), field("value", 3.14))
    struct_time = bench.elapsed_us()
    
    log.info(
        "Printf vs structured comparison",
        field("iterations", printf_iterations),
        field("printf_time_us", printf_time),
        field("struct_time_us", struct_time),
        field("printf_avg_ns", printf_time * 1000 // printf_iterations),
        field("struct_avg_ns", struct_time * 1000 // printf_iterations)
    )
    
    # Test 6: Memory allocation patterns
    print("\n--- Test 6: Memory Allocation Patterns ---")
    bench = Benchmark()
    
    allocation_iterations = 10
    for i in range(allocation_iterations):
        temp_log = (get_logger("temp")
                   .with_field("session", i)
                   .with_field("user", "testuser")
                   .with_name("module")
                   .with_field("operation", "test"))
        temp_log.info("Temporary logger message")
    
    log.info(
        "Memory allocation test completed",
        field("iterations", allocation_iterations),
        field("total_time_us", bench.elapsed_us()),
        field("avg_time_ns", bench.elapsed_ns() // allocation_iterations)
    )
    
    # Test 7: Level filtering performance
    print("\n--- Test 7: Level Filtering Performance ---")
    
    # Test with different levels
    levels_to_test = [Level.CRITICAL, Level.WARN, Level.INFO, Level.DEBUG, Level.ANNOYING]
    
    for test_level in levels_to_test:
        set_level(test_level)
        bench = Benchmark()
        
        for i in range(10):
            # Try logging at different levels
            log.critical("Critical message")
            log.error("Error message") 
            log.warn("Warning message")
            log.info("Info message")
            log.verbose("Verbose message")
            log.debug("Debug message")
            log.pedantic("Pedantic message")
            log.annoying("Annoying message")
        
        elapsed_time = bench.elapsed_us()
        set_level(Level.INFO)  # Reset for logging results
        
        log.info(
            f"Level filtering test at {test_level.name} level",
            field("test_level", test_level.name),
            field("iterations", 10),
            field("total_time_us", elapsed_time),
            field("avg_time_ns", elapsed_time * 1000 // 10)
        )
    
    log.info("Performance testing completed")


if __name__ == "__main__":
    main()