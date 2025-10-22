FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Dependencias del sistema (mysqlclient, cairo para xhtml2pdf, etc.)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    default-libmysqlclient-dev \
    pkg-config \
    libjpeg-dev \
    zlib1g-dev \
    libfreetype6-dev \
    libffi-dev \
    libcairo2 \
    ghostscript \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app
RUN chmod +x /app/entrypoint.sh

# Usuario sin privilegios
RUN useradd -m appuser

# Crear directorio para estáticos con permisos correctos
RUN mkdir -p /app/staticfiles && chown -R appuser:appuser /app

USER appuser

ENV DJANGO_SETTINGS_MODULE=settings.settings

EXPOSE 8000

CMD ["/bin/bash", "-c", "sleep 10; python manage.py migrate --fake-initial --noinput; python manage.py collectstatic --noinput; exec gunicorn settings.wsgi:application --bind 0.0.0.0:8000 --workers 3 --timeout 120"]


