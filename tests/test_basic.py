#!/usr/bin/env python3
"""
Basic tests for redlog functionality.
"""

import pytest
from redlog import (
    get_logger, set_level, get_level, Level, field, Field, FieldSet,
    StringSink, DefaultFormatter, TimestampedFormatter, JSONFormatter
)


def test_basic_logging():
    """Test basic logging functionality."""
    # Test that all logging methods exist and can be called
    log = get_logger("test")
    
    # Test full name methods
    log.critical("critical message")
    log.error("error message")
    log.warn("warn message")
    log.info("info message")
    log.verbose("verbose message")
    log.trace("trace message")
    log.debug("debug message")
    log.pedantic("pedantic message")
    log.annoying("annoying message")
    
    # Test short form methods
    log.crt("critical short")
    log.err("error short")
    log.wrn("warn short")
    log.inf("info short")
    log.vrb("verbose short")
    log.trc("trace short")
    log.dbg("debug short")
    log.ped("pedantic short")
    log.ayg("annoying short")


def test_field_system():
    """Test the field system."""
    # Test basic field creation
    f1 = Field("key1", "value1")
    assert f1.key == "key1"
    assert f1.value == "value1"
    
    # Test different value types
    f_int = Field("int", 42)
    f_float = Field("float", 3.14)
    f_bool = Field("bool", True)
    
    assert f_int.value == "42"
    assert "3.14" in f_float.value
    assert f_bool.value in ["1", "True"]
    
    # Test field function
    f = field("test", "value")
    assert isinstance(f, Field)
    assert f.key == "test"
    assert f.value == "value"


def test_field_set():
    """Test FieldSet operations."""
    fs1 = FieldSet()
    assert fs1.empty()
    assert len(fs1) == 0
    
    fs1.add(Field("key1", "value1"))
    assert not fs1.empty()
    assert len(fs1) == 1
    
    fs2 = FieldSet([Field("key2", "value2"), Field("key3", "value3")])
    assert len(fs2) == 2
    
    # Test merge
    fs1.merge(fs2)
    assert len(fs1) == 3
    
    # Test with_field (immutable operation)
    fs3 = fs1.with_field(Field("key4", "value4"))
    assert len(fs1) == 3  # Original unchanged
    assert len(fs3) == 4  # New one has additional field


def test_scoped_loggers():
    """Test scoped logger functionality."""
    base_log = get_logger("base")
    
    # Test with_name
    named_log = base_log.with_name("module")
    assert named_log.name == "base.module"
    
    # Test hierarchical naming
    nested_log = named_log.with_name("submodule")
    assert nested_log.name == "base.module.submodule"
    
    # Test with_field
    field_log = base_log.with_field("session_id", 12345)
    assert len(field_log.fields) == 1
    
    # Test chaining
    chained_log = base_log.with_name("chained").with_field("user", "alice").with_field("action", "login")
    assert chained_log.name == "base.chained"
    assert len(chained_log.fields) == 2


def test_level_filtering():
    """Test level filtering functionality."""
    # Test level setting and getting
    original_level = get_level()
    
    try:
        set_level(Level.WARN)
        assert get_level() == Level.WARN
        
        set_level(Level.DEBUG)
        assert get_level() == Level.DEBUG
        
        set_level(Level.INFO)
        assert get_level() == Level.INFO
    finally:
        # Restore original level
        set_level(original_level)


def test_printf_formatting():
    """Test printf-style formatting."""
    log = get_logger("printf_test")
    
    # Test all level printf methods work (they should not raise exceptions)
    log.critical_f("Critical: %d", 1)
    log.error_f("Error: %d", 2)
    log.warn_f("Warn: %d", 3)
    log.info_f("Info: %d", 4)
    log.verbose_f("Verbose: %d", 5)
    log.trace_f("Trace: %d", 6)
    log.debug_f("Debug: %d", 7)
    log.pedantic_f("Pedantic: %d", 8)
    log.annoying_f("Annoying: %d", 9)
    
    # Test short form printf methods
    log.crt_f("Critical short: %x", 255)
    log.err_f("Error short: %x", 255)
    log.wrn_f("Warn short: %x", 255)
    log.inf_f("Info short: %x", 255)
    log.vrb_f("Verbose short: %x", 255)
    log.trc_f("Trace short: %x", 255)
    log.dbg_f("Debug short: %x", 255)
    log.ped_f("Pedantic short: %x", 255)
    log.ayg_f("Annoying short: %x", 255)


def test_custom_formatters():
    """Test custom formatters."""
    string_sink = StringSink()
    
    # Test default formatter
    default_formatter = DefaultFormatter()
    assert default_formatter is not None
    
    # Test timestamped formatter
    timestamped_formatter = TimestampedFormatter()
    assert timestamped_formatter is not None
    
    # Test JSON formatter
    json_formatter = JSONFormatter()
    assert json_formatter is not None


def test_string_sink():
    """Test StringSink functionality."""
    sink = StringSink()
    
    sink.write("test message 1")
    sink.write("test message 2")
    
    output = sink.get_output()
    assert "test message 1" in output
    assert "test message 2" in output
    
    sink.clear()
    assert sink.get_output() == ""


def test_immutable_logger():
    """Test that loggers are immutable."""
    base_log = get_logger("immutable_test")
    
    # with_name should return new instance
    named_log = base_log.with_name("module")
    assert base_log.name == "immutable_test"
    assert named_log.name == "immutable_test.module"
    assert base_log is not named_log
    
    # with_field should return new instance
    field_log = base_log.with_field("key", "value")
    assert len(base_log.fields) == 0
    assert len(field_log.fields) == 1
    assert base_log is not field_log


if __name__ == "__main__":
    pytest.main([__file__])