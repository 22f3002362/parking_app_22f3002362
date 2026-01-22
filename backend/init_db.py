"""
Database initialization script for production deployment.
This script creates all database tables and seeds initial data.
"""
import os
from dotenv import load_dotenv

load_dotenv()

from app import app, db
from models import User

def init_database():
    """Initialize the database with tables and seed data."""
    with app.app_context():
        try:
            # Create all tables
            db.create_all()
            print("Database tables created successfully!")

            # Create admin user if it doesn't exist
            admin = User.query.filter_by(email='admin@parkease.com').first()
            if not admin:
                admin = User(
                    username='admin',
                    email='admin@parkease.com',
                    role='admin',
                    password='Admin@123',  # Change this in production!
                    phone_number='0000000000'
                )
                db.session.add(admin)
                db.session.commit()
                print("Admin user created successfully!")
                print("  Email: admin@parkease.com")
                print("  Password: Admin@123")
                print("  ** IMPORTANT: Change this password after first login! **")
            else:
                print("Admin user already exists.")

        except Exception as e:
            print(f"Database initialization error: {str(e)}")
            db.session.rollback()
            raise e

if __name__ == '__main__':
    init_database()
