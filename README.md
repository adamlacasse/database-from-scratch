# Simple Database From Scratch

A minimal, educational key-value database implementation built from scratch in Python. This project demonstrates core database concepts including:

- **In-memory storage** with fast access
- **File-based persistence** using JSON
- **CRUD operations** (Create, Read, Update, Delete)
- **Transaction support** (Begin, Commit, Rollback)
- **Interactive CLI** for database operations

## Features

### Core Database Engine (`database.py`)
- Key-value storage with string keys and JSON-serializable values
- Automatic persistence to disk after every write operation
- Transaction support for atomic operations
- Simple API for common database operations

### Command-Line Interface (`cli.py`)
- Interactive shell for database operations
- Support for all CRUD operations
- Transaction commands
- JSON value parsing

### Comprehensive Test Suite (`test_database.py`)
- 19 test cases covering all functionality
- Tests for persistence, transactions, and error handling

## Installation

No external dependencies required! Just Python 3.6+

```bash
# Clone the repository
git clone https://github.com/adamlacasse/database-from-scratch.git
cd database-from-scratch
```

## Usage

### Using the Python API

```python
from database import SimpleDatabase

# Create or open a database
db = SimpleDatabase("mydata.db")

# Set values
db.set("username", "alice")
db.set("age", 30)
db.set("preferences", {"theme": "dark", "notifications": True})

# Get values
username = db.get("username")  # Returns: "alice"
age = db.get("age")            # Returns: 30

# Check if key exists
if db.exists("username"):
    print("User exists!")

# Delete a key
db.delete("age")

# List all keys
all_keys = db.keys()  # Returns: ["username", "preferences"]

# Get database size
count = db.size()  # Returns: 2

# Clear all data
db.clear()

# Transactions
db.begin_transaction()
db.set("temp", "value")
db.rollback()  # Changes are reverted
```

### Using the CLI

```bash
# Start the interactive CLI
python3 cli.py [database_file]

# Example session:
> SET name Alice
OK - Set 'name' = "Alice"

> SET age 30
OK - Set 'age' = 30

> GET name
"Alice"

> KEYS
1) name
2) age

> DELETE age
OK - Deleted 'age'

> SIZE
1 items

> EXIT
Goodbye!
```

### CLI Commands

| Command | Description | Example |
|---------|-------------|---------|
| `SET <key> <value>` | Set a key-value pair | `SET name Alice` |
| `GET <key>` | Retrieve a value | `GET name` |
| `DELETE <key>` | Remove a key | `DELETE name` |
| `EXISTS <key>` | Check if key exists | `EXISTS name` |
| `KEYS` | List all keys | `KEYS` |
| `VALUES` | List all values | `VALUES` |
| `ITEMS` | List all key-value pairs | `ITEMS` |
| `SIZE` | Show number of items | `SIZE` |
| `CLEAR` | Clear all data | `CLEAR` |
| `BEGIN` | Start transaction | `BEGIN` |
| `COMMIT` | Commit transaction | `COMMIT` |
| `ROLLBACK` | Rollback transaction | `ROLLBACK` |
| `HELP` | Show help | `HELP` |
| `EXIT` | Quit the CLI | `EXIT` |

## Running Tests

```bash
python3 test_database.py
```

Expected output:
```
test_clear ... ok
test_delete ... ok
test_exists ... ok
...
----------------------------------------------------------------------
Ran 19 tests in 0.007s

OK
```

## Example: Quick Demo

```bash
# Run the built-in demo
python3 database.py
```

This will demonstrate:
- Setting and getting values
- Listing keys
- Checking existence
- Database size
- Transaction rollback

## How It Works

### Storage Format
The database stores data in a JSON file on disk. For example:

```json
{
  "username": "alice",
  "age": 30,
  "preferences": {
    "theme": "dark",
    "notifications": true
  }
}
```

### Persistence
Every write operation (`set`, `delete`, `clear`) automatically saves data to disk. This ensures data durability but may impact performance for write-heavy workloads.

### Transactions
Transactions work by creating a snapshot of the current data when `begin_transaction()` is called. If `rollback()` is executed, the database restores this snapshot. If `commit()` is called, the snapshot is discarded.

## API Reference

### SimpleDatabase Class

#### `__init__(filepath: str = "data.db")`
Initialize the database with the specified file path.

#### `set(key: str, value: Any) -> None`
Store a key-value pair. Value must be JSON-serializable.

#### `get(key: str, default: Any = None) -> Any`
Retrieve a value by key. Returns `default` if key doesn't exist.

#### `delete(key: str) -> bool`
Delete a key. Returns `True` if deleted, `False` if key didn't exist.

#### `exists(key: str) -> bool`
Check if a key exists in the database.

#### `keys() -> list`
Return a list of all keys.

#### `values() -> list`
Return a list of all values.

#### `items() -> list`
Return a list of (key, value) tuples.

#### `size() -> int`
Return the number of items in the database.

#### `clear() -> None`
Remove all data from the database.

#### `begin_transaction() -> None`
Start a transaction.

#### `commit() -> None`
Commit the current transaction.

#### `rollback() -> None`
Rollback to the state at transaction start.

## Limitations

This is an educational project with intentional simplifications:

- **No concurrent access**: Single-threaded, not safe for multiple processes
- **No indexing**: All operations are O(n) or O(1) on the in-memory dict
- **Full data in memory**: Entire database must fit in RAM
- **No query language**: Only key-value operations supported
- **No data types**: All data must be JSON-serializable
- **No compression**: Data stored as plain JSON text

## Future Enhancements

Possible improvements for learning:

- [ ] Add B-tree indexing for faster lookups
- [ ] Implement a query language (SQL-like)
- [ ] Add support for concurrent access with file locking
- [ ] Implement write-ahead logging (WAL)
- [ ] Add data compression
- [ ] Support for range queries
- [ ] Implement sharding for larger datasets
- [ ] Add replication support

## License

MIT License - Feel free to use this for learning and educational purposes!

## Contributing

This is an educational project, but contributions are welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests
- Use it as a learning resource

---

**Built from scratch to understand database fundamentals!** 🚀