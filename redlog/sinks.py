"""
Sink system for output destinations.
"""

import sys
from abc import ABC, abstractmethod
from typing import TextIO


class Sink(ABC):
    """Output sink interface."""

    @abstractmethod
    def write(self, formatted: str) -> None:
        """Write a formatted log message.

        Args:
            formatted: The formatted log message
        """
        pass

    @abstractmethod
    def flush(self) -> None:
        """Flush any buffered output."""
        pass


class ConsoleSink(Sink):
    """Console sink for stderr output."""

    def __init__(self, stream: TextIO = None) -> None:
        self.stream = stream or sys.stderr

    def write(self, formatted: str) -> None:
        """Write to the console stream."""
        print(formatted, file=self.stream)
        self.stream.flush()

    def flush(self) -> None:
        """Flush the console stream."""
        self.stream.flush()


class FileSink(Sink):
    """File sink for logging to a file.

    Falls back to stderr if file cannot be opened.
    """

    def __init__(self, filename: str) -> None:
        self.filename = filename
        self.should_close = False

        try:
            self.file = open(filename, "a")
            self.should_close = True
        except (OSError, IOError):
            # Fallback to stderr if file open fails
            self.file = sys.stderr
            self.should_close = False

    def write(self, formatted: str) -> None:
        """Write to the file."""
        if self.file:
            print(formatted, file=self.file)

    def flush(self) -> None:
        """Flush the file."""
        if self.file:
            self.file.flush()

    def close(self) -> None:
        """Close the file if we opened it."""
        if self.should_close and self.file:
            self.file.close()

    def __del__(self) -> None:
        """Cleanup when the sink is destroyed."""
        self.close()


class StringSink(Sink):
    """String sink for capturing output (useful for testing)."""

    def __init__(self) -> None:
        self.buffer = []

    def write(self, formatted: str) -> None:
        """Write to the internal buffer."""
        self.buffer.append(formatted)

    def flush(self) -> None:
        """No-op for string sink."""
        pass

    def get_output(self) -> str:
        """Get the captured output."""
        return "\n".join(self.buffer)

    def clear(self) -> None:
        """Clear the captured output."""
        self.buffer.clear()


class MultiplexSink(Sink):
    """Sink that writes to multiple other sinks."""

    def __init__(self, *sinks: Sink) -> None:
        self.sinks = list(sinks)

    def add_sink(self, sink: Sink) -> None:
        """Add a sink to the multiplex."""
        self.sinks.append(sink)

    def write(self, formatted: str) -> None:
        """Write to all sinks."""
        for sink in self.sinks:
            try:
                sink.write(formatted)
            except Exception:
                # Continue writing to other sinks even if one fails
                pass

    def flush(self) -> None:
        """Flush all sinks."""
        for sink in self.sinks:
            try:
                sink.flush()
            except Exception:
                # Continue flushing other sinks even if one fails
                pass
