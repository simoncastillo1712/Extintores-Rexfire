#!/bin/bash
set -e
python manage.py collectstatic --no-input
exec gunicorn rexfire.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --timeout 120
