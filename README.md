# redlog

a modern python logging library

## features

- beautiful aligned output with automatic color detection
- structured logging with key-value fields
- immutable scoped loggers for hierarchical context
- thread-safe by design
- printf-style formatting support
- customizable themes and formatters

## quick start

```python
import redlog

log = redlog.get_logger("app")

log.info("hello world")
log.info("user login", 
         redlog.field("username", "alice"),
         redlog.field("success", True))

db_log = log.with_name("database")
db_log.error("connection failed", redlog.field("host", "localhost"))
```

## install

```bash
pip install redlog-py
```

## usage

### basic logging

```python
log = redlog.get_logger("myapp")

log.critical("system failure")
log.error("something went wrong")
log.warn("potential issue")
log.info("general information")
log.debug("debugging details")
```

### short forms

```python
log.crt("critical")  # same as critical()
log.err("error")     # same as error()
log.inf("info")      # same as info()
log.dbg("debug")     # same as debug()
```

### structured fields

```python
log.info("user action",
         redlog.field("user_id", 12345),
         redlog.field("action", "login"),
         redlog.field("ip", "192.168.1.100"))
```

### scoped loggers

```python
request_log = log.with_field("request_id", 12345) \
                 .with_field("method", "POST")

handler_log = request_log.with_name("handler")
handler_log.info("processing request")
```

### printf-style formatting

```python
log.info_f("user %s logged in from %s", username, ip_address)
log.error_f("failed to connect to %s:%d", host, port)
```

### configuration

```python
# set minimum log level
redlog.set_level(redlog.Level.DEBUG)

# use plain theme (no colors)
redlog.set_theme(redlog.themes.PLAIN)
```

## development

```bash
poetry install
poetry run python examples/basic.py
poetry run pytest
```
