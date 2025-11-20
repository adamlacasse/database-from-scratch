#!/usr/bin/env python3
"""
Command Line Interface for Simple Database

Provides an interactive shell for database operations.
"""

import sys
import json
from database import SimpleDatabase


def print_help():
    """Print help information."""
    help_text = """
Simple Database CLI - Available Commands:

  SET <key> <value>     - Set a key to a value
  GET <key>             - Get the value of a key
  DELETE <key>          - Delete a key
  EXISTS <key>          - Check if a key exists
  KEYS                  - List all keys
  VALUES                - List all values
  ITEMS                 - List all key-value pairs
  SIZE                  - Show number of items in database
  CLEAR                 - Clear all data (use with caution!)
  BEGIN                 - Begin a transaction
  COMMIT                - Commit the current transaction
  ROLLBACK              - Rollback the current transaction
  HELP                  - Show this help message
  EXIT                  - Exit the database CLI

Examples:
  > SET username alice
  > GET username
  > DELETE username
  > SET config {"theme": "dark", "lang": "en"}
"""
    print(help_text)


def parse_value(value_str: str):
    """Parse a value string, attempting to parse JSON if possible."""
    try:
        # Try to parse as JSON
        return json.loads(value_str)
    except json.JSONDecodeError:
        # Return as string if not valid JSON
        return value_str


def main():
    """Main CLI loop."""
    if len(sys.argv) > 1:
        db_file = sys.argv[1]
    else:
        db_file = "simple.db"
    
    db = SimpleDatabase(db_file)
    print(f"Simple Database CLI - Using file: {db_file}")
    print("Type HELP for available commands, EXIT to quit\n")
    
    while True:
        try:
            # Read command
            command_line = input("> ").strip()
            
            if not command_line:
                continue
            
            # Parse command
            parts = command_line.split(maxsplit=1)
            command = parts[0].upper()
            args = parts[1] if len(parts) > 1 else ""
            
            # Execute command
            if command == "EXIT" or command == "QUIT":
                print("Goodbye!")
                break
            
            elif command == "HELP":
                print_help()
            
            elif command == "SET":
                if not args:
                    print("Error: SET requires <key> <value>")
                    continue
                
                key_value = args.split(maxsplit=1)
                if len(key_value) < 2:
                    print("Error: SET requires both key and value")
                    continue
                
                key, value_str = key_value
                value = parse_value(value_str)
                db.set(key, value)
                print(f"OK - Set '{key}' = {json.dumps(value)}")
            
            elif command == "GET":
                if not args:
                    print("Error: GET requires <key>")
                    continue
                
                key = args.strip()
                value = db.get(key)
                if value is None:
                    print(f"(nil) - Key '{key}' not found")
                else:
                    print(json.dumps(value))
            
            elif command == "DELETE":
                if not args:
                    print("Error: DELETE requires <key>")
                    continue
                
                key = args.strip()
                if db.delete(key):
                    print(f"OK - Deleted '{key}'")
                else:
                    print(f"Error: Key '{key}' not found")
            
            elif command == "EXISTS":
                if not args:
                    print("Error: EXISTS requires <key>")
                    continue
                
                key = args.strip()
                exists = db.exists(key)
                print(f"{'Yes' if exists else 'No'}")
            
            elif command == "KEYS":
                keys = db.keys()
                if keys:
                    for i, key in enumerate(keys, 1):
                        print(f"{i}) {key}")
                else:
                    print("(empty)")
            
            elif command == "VALUES":
                values = db.values()
                if values:
                    for i, value in enumerate(values, 1):
                        print(f"{i}) {json.dumps(value)}")
                else:
                    print("(empty)")
            
            elif command == "ITEMS":
                items = db.items()
                if items:
                    for i, (key, value) in enumerate(items, 1):
                        print(f"{i}) {key} = {json.dumps(value)}")
                else:
                    print("(empty)")
            
            elif command == "SIZE":
                print(f"{db.size()} items")
            
            elif command == "CLEAR":
                confirm = input("Are you sure you want to clear all data? (yes/no): ")
                if confirm.lower() == "yes":
                    db.clear()
                    print("OK - Database cleared")
                else:
                    print("Cancelled")
            
            elif command == "BEGIN":
                db.begin_transaction()
                print("OK - Transaction started")
            
            elif command == "COMMIT":
                db.commit()
                print("OK - Transaction committed")
            
            elif command == "ROLLBACK":
                db.rollback()
                print("OK - Transaction rolled back")
            
            else:
                print(f"Error: Unknown command '{command}'. Type HELP for available commands.")
        
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()
