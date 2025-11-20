#!/usr/bin/env python3
"""
Example demonstrating various database operations.

This script shows how to use the SimpleDatabase for common tasks.
"""

from database import SimpleDatabase
import json


def main():
    print("=" * 60)
    print("Simple Database - Example Usage")
    print("=" * 60)
    print()
    
    # Initialize database
    db = SimpleDatabase("demo.db")
    db.clear()  # Start fresh
    
    # Example 1: Basic CRUD operations
    print("1. Basic CRUD Operations")
    print("-" * 60)
    
    # Create
    db.set("user:1:name", "Alice")
    db.set("user:1:email", "alice@example.com")
    db.set("user:1:age", 28)
    print("✓ Created user record")
    
    # Read
    name = db.get("user:1:name")
    email = db.get("user:1:email")
    print(f"✓ Read: {name} ({email})")
    
    # Update
    db.set("user:1:age", 29)
    print(f"✓ Updated age to {db.get('user:1:age')}")
    
    # Delete
    db.delete("user:1:age")
    print("✓ Deleted age field")
    print()
    
    # Example 2: Complex data structures
    print("2. Storing Complex Data")
    print("-" * 60)
    
    user_profile = {
        "id": 123,
        "name": "Bob Smith",
        "preferences": {
            "theme": "dark",
            "language": "en",
            "notifications": True
        },
        "tags": ["developer", "python", "database"]
    }
    
    db.set("user:123:profile", user_profile)
    stored = db.get("user:123:profile")
    print(f"✓ Stored complex object:")
    print(f"  Name: {stored['name']}")
    print(f"  Theme: {stored['preferences']['theme']}")
    print(f"  Tags: {', '.join(stored['tags'])}")
    print()
    
    # Example 3: Listing and counting
    print("3. Database Inspection")
    print("-" * 60)
    
    db.set("setting:max_users", 100)
    db.set("setting:timeout", 30)
    
    print(f"✓ Total items in database: {db.size()}")
    print(f"✓ All keys:")
    for key in sorted(db.keys()):
        print(f"  - {key}")
    print()
    
    # Example 4: Transactions
    print("4. Transaction Example")
    print("-" * 60)
    
    print(f"Current database size: {db.size()}")
    
    # Start a transaction
    db.begin_transaction()
    print("✓ Transaction started")
    
    # Make some changes
    db.set("temp:1", "temporary data 1")
    db.set("temp:2", "temporary data 2")
    db.set("temp:3", "temporary data 3")
    print(f"✓ Added temporary data (size: {db.size()})")
    
    # Rollback
    db.rollback()
    print(f"✓ Transaction rolled back (size: {db.size()})")
    print()
    
    # Example 5: Search pattern (using key prefixes)
    print("5. Key Patterns")
    print("-" * 60)
    
    # Store some data with prefixes
    db.set("product:1:name", "Laptop")
    db.set("product:1:price", 999.99)
    db.set("product:2:name", "Mouse")
    db.set("product:2:price", 29.99)
    
    # Find all product keys
    product_keys = [k for k in db.keys() if k.startswith("product:")]
    print(f"✓ Found {len(product_keys)} product-related keys:")
    for key in sorted(product_keys):
        print(f"  - {key}: {db.get(key)}")
    print()
    
    # Example 6: Session data
    print("6. Session Management Example")
    print("-" * 60)
    
    session = {
        "session_id": "abc123",
        "user_id": 456,
        "login_time": "2024-11-20T19:00:00Z",
        "ip_address": "192.168.1.100"
    }
    
    db.set("session:abc123", session)
    
    # Retrieve session
    active_session = db.get("session:abc123")
    if active_session:
        print(f"✓ Active session for user {active_session['user_id']}")
        print(f"  Login time: {active_session['login_time']}")
        print(f"  IP: {active_session['ip_address']}")
    
    # Cleanup session
    db.delete("session:abc123")
    print("✓ Session cleaned up")
    print()
    
    # Summary
    print("=" * 60)
    print(f"Final database state: {db.size()} items")
    print("=" * 60)
    print()
    print("Example completed successfully! ✓")
    print(f"Database persisted to: demo.db")


if __name__ == "__main__":
    main()
