# Quick Start Guide

Get started with Simple Database in 2 minutes!

## Option 1: Run the Example

```bash
python3 example.py
```

This runs a comprehensive demo showing all features.

## Option 2: Use the Python API

```python
from database import SimpleDatabase

# Create database
db = SimpleDatabase("mydata.db")

# Store data
db.set("greeting", "Hello, World!")

# Retrieve data
print(db.get("greeting"))  # Output: Hello, World!
```

## Option 3: Use the Interactive CLI

```bash
python3 cli.py
```

Then try these commands:
```
> SET name Alice
> GET name
> KEYS
> SIZE
> EXIT
```

## Run Tests

```bash
python3 test_database.py
```

Expected: All 19 tests pass ✓

## What's Next?

- Read the full [README.md](README.md) for complete documentation
- Check [example.py](example.py) for more usage patterns
- Try building something with it!

## Common Use Cases

### Configuration Storage
```python
db.set("config", {"theme": "dark", "lang": "en"})
```

### User Sessions
```python
db.set("session:abc123", {"user_id": 456, "login_time": "..."})
```

### Cache
```python
db.set("cache:user:123", {"name": "Alice", "email": "..."})
```

### Simple Key-Value Store
```python
db.set("counter", 0)
count = db.get("counter") + 1
db.set("counter", count)
```

Happy coding! 🚀
