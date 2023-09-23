#!/bin/ash

# Run migrations
poetry run alembic upgrade head

# Run the main application
poetry run python -Xfrozen_modules=off -m debugpy --wait-for-client --listen 0.0.0.0:5678 main.py
