#!/bin/bash
set -e

# Esperar a que la base de datos acepte conexiones TCP (max ~120s)
python - << 'PY'
import os, socket, time
host = os.getenv('DB_HOST', 'db')
port = int(os.getenv('DB_PORT', '3306'))
max_retries = 60
for i in range(max_retries):
    try:
        with socket.create_connection((host, port), timeout=2):
            print('DB listo')
            break
    except OSError:
        print(f'Esperando DB {host}:{port}... intento {i+1}/{max_retries}')
        time.sleep(2)
else:
    raise SystemExit('DB no disponible')
PY

python manage.py migrate --noinput
python manage.py collectstatic --noinput

exec gunicorn settings.wsgi:application --bind 0.0.0.0:8000 --workers ${GUNICORN_WORKERS:-3} --timeout ${GUNICORN_TIMEOUT:-120}