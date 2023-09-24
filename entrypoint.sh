#!/bin/ash


echo "Running migrations..."

# Run migrations
poetry run alembic upgrade head

echo "Starting server..."
# Run the main application
poetry run python -Xfrozen_modules=off -m debugpy --wait-for-client --listen 0.0.0.0:5678 main.py
