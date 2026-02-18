#!/bin/bash
# Stop execution if any command fails
set -e

echo "--- Running Database Migrations ---"
python manage.py migrate --noinput

echo "--- Collecting Static Files ---"
python manage.py collectstatic --noinput

echo "--- Starting Gunicorn Server ---"
exec gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 3