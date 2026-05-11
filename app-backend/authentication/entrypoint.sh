#!/bin/bash
set -e

echo ">>> Running migrations (authentication)..."
uv run python manage.py migrate --noinput

echo ">>> Collecting static files..."
uv run python manage.py collectstatic --noinput --clear 2>/dev/null || true

echo ">>> Starting Daphne on 0.0.0.0:8000..."
exec uv run daphne -b 0.0.0.0 -p 8000 authentication.asgi:application
