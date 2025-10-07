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

# Crear directorio para estáticos
RUN mkdir -p /app/staticfiles

# Usuario sin privilegios
RUN useradd -m appuser
USER appuser

ENV DJANGO_SETTINGS_MODULE=settings.settings

EXPOSE 8000

CMD ["gunicorn", "settings.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3", "--timeout", "120"]


