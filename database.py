#!/usr/bin/env python3
"""
Simple Database Implementation

A minimal key-value database with the following features:
- In-memory storage for fast access
- File-based persistence (JSON format)
- CRUD operations (Create, Read, Update, Delete)
- Transaction support (simple commit/rollback)
"""

import json
import os
from typing import Any, Optional, Dict
from pathlib import Path


class SimpleDatabase:
    """A simple key-value database with persistence."""
    
    def __init__(self, filepath: str = "data.db"):
        """
        Initialize the database.
        
        Args:
            filepath: Path to the database file for persistence
        """
        self.filepath = filepath
        self.data: Dict[str, Any] = {}
        self._transaction_data: Optional[Dict[str, Any]] = None
        self._load()
    
    def _load(self) -> None:
        """Load data from disk if the file exists."""
        if os.path.exists(self.filepath):
            try:
                with open(self.filepath, 'r') as f:
                    self.data = json.load(f)
            except (json.JSONDecodeError, IOError) as e:
                print(f"Warning: Could not load database file: {e}")
                self.data = {}
        else:
            self.data = {}
    
    def _save(self) -> None:
        """Save data to disk."""
        try:
            with open(self.filepath, 'w') as f:
                json.dump(self.data, f, indent=2)
        except IOError as e:
            raise IOError(f"Failed to save database: {e}")
    
    def set(self, key: str, value: Any) -> None:
        """
        Set a key-value pair in the database.
        
        Args:
            key: The key to store
            value: The value to store (must be JSON serializable)
        """
        if not isinstance(key, str):
            raise ValueError("Key must be a string")
        
        # Test JSON serializability
        try:
            json.dumps(value)
        except (TypeError, ValueError) as e:
            raise ValueError(f"Value must be JSON serializable: {e}")
        
        self.data[key] = value
        self._save()
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a value from the database.
        
        Args:
            key: The key to retrieve
            default: Default value if key doesn't exist
            
        Returns:
            The value associated with the key, or default if not found
        """
        return self.data.get(key, default)
    
    def delete(self, key: str) -> bool:
        """
        Delete a key from the database.
        
        Args:
            key: The key to delete
            
        Returns:
            True if the key was deleted, False if it didn't exist
        """
        if key in self.data:
            del self.data[key]
            self._save()
            return True
        return False
    
    def exists(self, key: str) -> bool:
        """
        Check if a key exists in the database.
        
        Args:
            key: The key to check
            
        Returns:
            True if the key exists, False otherwise
        """
        return key in self.data
    
    def keys(self) -> list:
        """
        Get all keys in the database.
        
        Returns:
            List of all keys
        """
        return list(self.data.keys())
    
    def values(self) -> list:
        """
        Get all values in the database.
        
        Returns:
            List of all values
        """
        return list(self.data.values())
    
    def items(self) -> list:
        """
        Get all key-value pairs in the database.
        
        Returns:
            List of tuples containing (key, value) pairs
        """
        return list(self.data.items())
    
    def clear(self) -> None:
        """Clear all data from the database."""
        self.data = {}
        self._save()
    
    def size(self) -> int:
        """
        Get the number of key-value pairs in the database.
        
        Returns:
            Number of items in the database
        """
        return len(self.data)
    
    def begin_transaction(self) -> None:
        """Begin a transaction by creating a snapshot of current data."""
        self._transaction_data = self.data.copy()
    
    def commit(self) -> None:
        """Commit the current transaction."""
        if self._transaction_data is not None:
            self._transaction_data = None
            self._save()
    
    def rollback(self) -> None:
        """Rollback to the state at the beginning of the transaction."""
        if self._transaction_data is not None:
            self.data = self._transaction_data
            self._transaction_data = None
            self._save()


if __name__ == "__main__":
    # Example usage
    db = SimpleDatabase("example.db")
    
    # Set some values
    db.set("name", "Simple Database")
    db.set("version", "1.0")
    db.set("author", "Builder")
    
    # Read values
    print(f"Name: {db.get('name')}")
    print(f"Version: {db.get('version')}")
    
    # List all keys
    print(f"All keys: {db.keys()}")
    
    # Check existence
    print(f"Has 'name': {db.exists('name')}")
    print(f"Has 'missing': {db.exists('missing')}")
    
    # Get database size
    print(f"Database size: {db.size()}")
    
    # Transaction example
    db.begin_transaction()
    db.set("temp", "temporary value")
    print(f"Temp value: {db.get('temp')}")
    db.rollback()
    print(f"After rollback, temp exists: {db.exists('temp')}")
    
    print("\nDatabase demo completed!")
