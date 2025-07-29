#!/usr/bin/env python3
"""
System Reset Script - Clears both database and Redis cache
This solves the issue of old cached data being shown after database reset
"""

import os
import sys
import sqlite3
from redis import Redis
from datetime import datetime

def clear_redis():
    """Clear all Redis cache"""
    try:
        redis_client = Redis(
            host='localhost',
            port=6379,
            db=0,
            decode_responses=True,
            socket_connect_timeout=5,
            socket_timeout=5
        )
        
        # Test connection
        redis_client.ping()
        print("✅ Connected to Redis")
        
        # Clear ALL keys in database 0
        redis_client.flushdb()
        print("✅ Cleared all Redis cache")
        
        # Reset basic counters
        redis_client.set('total_api_calls', 0)
        redis_client.set('total_logins', 0)
        redis_client.set('total_logouts', 0)
        redis_client.set('total_registrations', 0)
        redis_client.set('users_created', 0)
        redis_client.set('users_deleted', 0)
        redis_client.set('parking_lots_created', 0)
        redis_client.set('parking_lots_deleted', 0)
        redis_client.set('total_reservations', 0)
        redis_client.set('reservations_cancelled', 0)
        redis_client.set('emails_sent_total', 0)
        redis_client.set('app_name', 'Parking Management System', ex=3600)
        print("✅ Reset Redis counters")
        
        return True
        
    except Exception as e:
        print(f"❌ Redis error: {e}")
        return False

def reset_database():
    """Reset SQLite database"""
    try:
        db_path = 'parking_app.db'
        
        # Check if database exists
        if os.path.exists(db_path):
            # Delete the database file
            os.remove(db_path)
            print("✅ Deleted old database file")
        
        # Create new database and tables by importing from app
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))
        
        from app import app, db, User
        
        with app.app_context():
            # Create all tables
            db.create_all()
            print("✅ Created new database tables")
            
            # Create admin user if doesn't exist
            existing_admin = User.query.filter_by(email='admin@mad2.com').first()
            if not existing_admin:
                admin = User(
                    username='admin',
                    email='admin@mad2.com',
                    role='admin',
                    password='Admin@123',
                    phone_number='8709186793'
                )
                db.session.add(admin)
                db.session.commit()
                print("✅ Created admin user (admin@mad2.com / Admin@123)")
            else:
                print("✅ Admin user already exists (admin@mad2.com / Admin@123)")
        
        return True
        
    except Exception as e:
        print(f"❌ Database error: {e}")
        return False

def main():
    """Main reset function"""
    print("🔄 Starting system reset...")
    print("=" * 50)
    
    # Step 1: Clear Redis
    print("\n1. Clearing Redis cache...")
    redis_success = clear_redis()
    
    # Step 2: Reset Database
    print("\n2. Resetting database...")
    db_success = reset_database()
    
    # Summary
    print("\n" + "=" * 50)
    print("📋 RESET SUMMARY:")
    print(f"Redis Cache: {'✅ Success' if redis_success else '❌ Failed'}")
    print(f"Database: {'✅ Success' if db_success else '❌ Failed'}")
    
    if redis_success and db_success:
        print("\n🎉 System reset completed successfully!")
        print("\nNext steps:")
        print("1. Restart your Flask application")
        print("2. The frontend should now show fresh data")
        print("3. Use admin credentials: admin@mad2.com / Admin@123")
    else:
        print("\n⚠️ Some operations failed. Please check the errors above.")
    
    print("\n" + "=" * 50)

if __name__ == "__main__":
    main()
