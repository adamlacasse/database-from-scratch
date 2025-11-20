#!/usr/bin/env python3
"""
Test suite for Simple Database

Run with: python3 test_database.py
"""

import unittest
import os
import json
from database import SimpleDatabase


class TestSimpleDatabase(unittest.TestCase):
    """Test cases for SimpleDatabase."""
    
    def setUp(self):
        """Set up test database."""
        self.test_db_file = "test.db"
        # Clean up any existing test database
        if os.path.exists(self.test_db_file):
            os.remove(self.test_db_file)
        self.db = SimpleDatabase(self.test_db_file)
    
    def tearDown(self):
        """Clean up test database."""
        if os.path.exists(self.test_db_file):
            os.remove(self.test_db_file)
    
    def test_set_and_get(self):
        """Test setting and getting values."""
        self.db.set("name", "Alice")
        self.assertEqual(self.db.get("name"), "Alice")
        
        self.db.set("age", 30)
        self.assertEqual(self.db.get("age"), 30)
        
        self.db.set("active", True)
        self.assertEqual(self.db.get("active"), True)
    
    def test_get_default(self):
        """Test getting with default value."""
        result = self.db.get("nonexistent", "default")
        self.assertEqual(result, "default")
    
    def test_set_complex_values(self):
        """Test setting complex JSON-serializable values."""
        data = {"name": "Bob", "scores": [85, 90, 95]}
        self.db.set("user", data)
        self.assertEqual(self.db.get("user"), data)
    
    def test_delete(self):
        """Test deleting keys."""
        self.db.set("temp", "value")
        self.assertTrue(self.db.exists("temp"))
        
        result = self.db.delete("temp")
        self.assertTrue(result)
        self.assertFalse(self.db.exists("temp"))
        
        # Try deleting non-existent key
        result = self.db.delete("nonexistent")
        self.assertFalse(result)
    
    def test_exists(self):
        """Test checking key existence."""
        self.assertFalse(self.db.exists("key"))
        
        self.db.set("key", "value")
        self.assertTrue(self.db.exists("key"))
        
        self.db.delete("key")
        self.assertFalse(self.db.exists("key"))
    
    def test_keys(self):
        """Test getting all keys."""
        self.assertEqual(self.db.keys(), [])
        
        self.db.set("a", 1)
        self.db.set("b", 2)
        self.db.set("c", 3)
        
        keys = self.db.keys()
        self.assertEqual(sorted(keys), ["a", "b", "c"])
    
    def test_values(self):
        """Test getting all values."""
        self.assertEqual(self.db.values(), [])
        
        self.db.set("a", 1)
        self.db.set("b", 2)
        self.db.set("c", 3)
        
        values = self.db.values()
        self.assertEqual(sorted(values), [1, 2, 3])
    
    def test_items(self):
        """Test getting all items."""
        self.assertEqual(self.db.items(), [])
        
        self.db.set("a", 1)
        self.db.set("b", 2)
        
        items = dict(self.db.items())
        self.assertEqual(items, {"a": 1, "b": 2})
    
    def test_size(self):
        """Test getting database size."""
        self.assertEqual(self.db.size(), 0)
        
        self.db.set("a", 1)
        self.assertEqual(self.db.size(), 1)
        
        self.db.set("b", 2)
        self.assertEqual(self.db.size(), 2)
        
        self.db.delete("a")
        self.assertEqual(self.db.size(), 1)
    
    def test_clear(self):
        """Test clearing the database."""
        self.db.set("a", 1)
        self.db.set("b", 2)
        self.assertEqual(self.db.size(), 2)
        
        self.db.clear()
        self.assertEqual(self.db.size(), 0)
        self.assertEqual(self.db.keys(), [])
    
    def test_persistence(self):
        """Test that data persists across instances."""
        self.db.set("persistent", "data")
        self.db.set("number", 42)
        
        # Create new instance with same file
        db2 = SimpleDatabase(self.test_db_file)
        self.assertEqual(db2.get("persistent"), "data")
        self.assertEqual(db2.get("number"), 42)
    
    def test_transaction_commit(self):
        """Test transaction commit."""
        self.db.set("original", "value")
        
        self.db.begin_transaction()
        self.db.set("new", "data")
        self.db.commit()
        
        self.assertTrue(self.db.exists("new"))
        self.assertEqual(self.db.get("new"), "data")
    
    def test_transaction_rollback(self):
        """Test transaction rollback."""
        self.db.set("original", "value")
        
        self.db.begin_transaction()
        self.db.set("temp", "temporary")
        self.assertTrue(self.db.exists("temp"))
        
        self.db.rollback()
        self.assertFalse(self.db.exists("temp"))
        self.assertTrue(self.db.exists("original"))
    
    def test_invalid_key_type(self):
        """Test that non-string keys raise an error."""
        with self.assertRaises(ValueError):
            self.db.set(123, "value")
    
    def test_non_serializable_value(self):
        """Test that non-JSON-serializable values raise an error."""
        with self.assertRaises(ValueError):
            # Lambda functions are not JSON serializable
            self.db.set("func", lambda x: x)
    
    def test_update_existing_key(self):
        """Test updating an existing key."""
        self.db.set("key", "value1")
        self.assertEqual(self.db.get("key"), "value1")
        
        self.db.set("key", "value2")
        self.assertEqual(self.db.get("key"), "value2")


class TestDatabasePersistence(unittest.TestCase):
    """Test database file persistence."""
    
    def setUp(self):
        """Set up test environment."""
        self.test_db_file = "persistence_test.db"
        if os.path.exists(self.test_db_file):
            os.remove(self.test_db_file)
    
    def tearDown(self):
        """Clean up test files."""
        if os.path.exists(self.test_db_file):
            os.remove(self.test_db_file)
    
    def test_file_created_on_first_write(self):
        """Test that database file is created on first write."""
        self.assertFalse(os.path.exists(self.test_db_file))
        
        db = SimpleDatabase(self.test_db_file)
        db.set("key", "value")
        
        self.assertTrue(os.path.exists(self.test_db_file))
    
    def test_file_contains_valid_json(self):
        """Test that database file contains valid JSON."""
        db = SimpleDatabase(self.test_db_file)
        db.set("name", "test")
        db.set("value", 123)
        
        with open(self.test_db_file, 'r') as f:
            data = json.load(f)
        
        self.assertEqual(data["name"], "test")
        self.assertEqual(data["value"], 123)
    
    def test_load_existing_database(self):
        """Test loading an existing database file."""
        # Create a database file manually
        initial_data = {"preloaded": "data", "count": 5}
        with open(self.test_db_file, 'w') as f:
            json.dump(initial_data, f)
        
        # Load it with SimpleDatabase
        db = SimpleDatabase(self.test_db_file)
        self.assertEqual(db.get("preloaded"), "data")
        self.assertEqual(db.get("count"), 5)


def run_tests():
    """Run all tests."""
    # Create a test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test cases
    suite.addTests(loader.loadTestsFromTestCase(TestSimpleDatabase))
    suite.addTests(loader.loadTestsFromTestCase(TestDatabasePersistence))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Return exit code
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    exit(run_tests())
