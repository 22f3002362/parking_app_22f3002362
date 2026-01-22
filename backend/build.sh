#!/usr/bin/env bash
# Build script for Render.com deployment
# This script runs during the build phase

set -o errexit  # Exit on error

echo "Installing Python dependencies..."
pip install -r requirements.txt

echo "Initializing database..."
python init_db.py

echo "Build completed successfully!"
