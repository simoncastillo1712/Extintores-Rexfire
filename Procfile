web: gunicorn rexfire.wsgi:application --bind 0.0.0.0:$PORT --workers 1 --threads 4 --timeout 120 --max-requests 500 --max-requests-jitter 50
release: python manage.py migrate --no-input && python manage.py collectstatic --no-input
