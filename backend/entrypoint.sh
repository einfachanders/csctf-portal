#!/bin/sh
echo "Performing database migrations"
alembic upgrade head
echo

echo "Creating initial data"
python3 initial_data.py
echo

echo "Starting application"
uvicorn app.main:app --host 0.0.0.0 --port 8000
