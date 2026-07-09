web: gunicorn rexfire.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --timeout 120
release: python manage.py migrate --no-input && python manage.py collectstatic --no-input
