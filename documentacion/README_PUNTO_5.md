# ⚙️ PUNTO 5: GUÍA DE INSTALACIÓN Y CONFIGURACIONES DE LAS DEPENDENCIAS Y LIBRERÍAS

## 🔗 **NAVEGACIÓN RÁPIDA**

### **📚 DOCUMENTACIÓN PRINCIPAL**
- [🏠 **Volver al índice principal**](README.md)
- [🏗️ **PUNTO 1**: Estructura y módulos](README_PUNTO_1.md)
- [🐳 **PUNTO 6**: Despliegue en Docker](README_PUNTO_6.md)
- [⌨️ **PUNTO 7**: Comandos del proyecto](README_PUNTO_7.md)

### **📊 REPORTES ESPECIALIZADOS**
- [🏗️ **REPORTE**: Análisis de estructura del código](REPORTE_ESTRUCTURA_CODIGO.md)
- [🔄 **REPORTE**: Flujo de interacción del usuario](REPORTE_FLUJO_USUARIO.md)

### **🔗 NAVEGACIÓN INTERNA**
- [💻 Requisitos del sistema](#requisitos-del-sistema)
- [🐍 Instalación de Python](#instalación-de-python)
- [🐳 Instalación de Docker](#instalación-de-docker)
- [🗄️ Instalación de MySQL](#instalación-de-mysql)
- [🔴 Instalación de Redis](#instalación-de-redis)
- [🌐 Instalación de Nginx](#instalación-de-nginx)
- [⚙️ Configuración de variables de entorno](#configuración-de-variables-de-entorno)
- [✅ Verificación de la instalación](#verificación-de-la-instalación)

---

## 🎯 **OBJETIVO**
Proporcionar una guía completa y detallada para la instalación y configuración de todas las dependencias y librerías necesarias para ejecutar el proyecto Backend-Optimizacion, incluyendo requisitos del sistema, instalación paso a paso y verificación de la configuración.

## 📋 **REQUISITOS PREVIOS**

### **💻 SISTEMA OPERATIVO:**
- **Windows 10/11** (64-bit)
- **Ubuntu 20.04+** / **CentOS 8+** / **Debian 11+**
- **macOS 10.15+**

### **🔧 SOFTWARE BASE:**
- **Python 3.8+** (Recomendado: Python 3.11)
- **Git 2.30+**
- **Docker 20.10+** y **Docker Compose 2.0+**
- **Node.js 16+** (para herramientas de desarrollo)

---

## 🐍 **INSTALACIÓN DE PYTHON**

### **🪟 WINDOWS:**
```powershell
# Descargar Python desde python.org
# O usar Chocolatey:
choco install python

# O usar winget:
winget install Python.Python.3.11

# Verificar instalación:
python --version
pip --version
```

### **🐧 LINUX (Ubuntu/Debian):**
```bash
# Actualizar repositorios
sudo apt update

# Instalar Python y pip
sudo apt install python3 python3-pip python3-venv

# Verificar instalación
python3 --version
pip3 --version
```

### **🍎 macOS:**
```bash
# Usar Homebrew
brew install python

# O descargar desde python.org
# Verificar instalación
python3 --version
pip3 --version
```

---

## 🐳 **INSTALACIÓN DE DOCKER**

### **🪟 WINDOWS:**
```powershell
# Descargar Docker Desktop desde docker.com
# O usar Chocolatey:
choco install docker-desktop

# Verificar instalación
docker --version
docker-compose --version
```

### **🐧 LINUX (Ubuntu/Debian):**
```bash
# Instalar dependencias
sudo apt update
sudo apt install apt-transport-https ca-certificates curl gnupg lsb-release

# Agregar GPG key oficial de Docker
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

# Agregar repositorio de Docker
echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Instalar Docker
sudo apt update
sudo apt install docker-ce docker-ce-cli containerd.io docker-compose-plugin

# Agregar usuario al grupo docker
sudo usermod -aG docker $USER

# Verificar instalación
docker --version
docker compose version
```

### **🍎 macOS:**
```bash
# Usar Homebrew
brew install --cask docker

# O descargar Docker Desktop desde docker.com
# Verificar instalación
docker --version
docker compose version
```

---

## 🔧 **CONFIGURACIÓN DEL ENTORNO VIRTUAL**

### **📁 CREAR ENTORNO VIRTUAL:**
```bash
# Navegar al directorio del proyecto
cd Backend-Optimizacion

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual (Windows)
venv\Scripts\activate

# Activar entorno virtual (Linux/macOS)
source venv/bin/activate
```

### **✅ VERIFICAR ACTIVACIÓN:**
```bash
# El prompt debe mostrar (venv)
(venv) C:\Users\Sebaztian\Backend-Optimizacion>

# Verificar Python del entorno
which python  # Linux/macOS
where python  # Windows
```

---

## 📦 **INSTALACIÓN DE DEPENDENCIAS PYTHON**

### **📋 DEPENDENCIAS PRINCIPALES (requirements.txt):**

```bash
# Instalar todas las dependencias
pip install -r requirements.txt
```

### **🔍 DEPENDENCIAS INSTALADAS:**

#### **🏗️ FRAMEWORK WEB:**
```
Django==4.2.7              # Framework web principal
djangorestframework==3.14.0 # API REST
django-cors-headers==4.3.1  # CORS para APIs
```

#### **🔐 AUTENTICACIÓN Y SEGURIDAD:**
```
djangorestframework-simplejwt==5.3.0  # JWT tokens
django-guardian==2.4.0               # Permisos por objeto
django-filter==23.3                  # Filtros avanzados
```

#### **🗄️ BASE DE DATOS:**
```
mysqlclient==2.2.0                   # Cliente MySQL
django-mysql==4.12.0                 # Extensiones MySQL para Django
```

#### **📊 CACHÉ Y TAREAS ASÍNCRONAS:**
```
redis==5.0.1                         # Cliente Redis
celery==5.3.4                        # Cola de tareas
django-celery-beat==2.5.0            # Programador de tareas
django-celery-results==2.5.1         # Almacenamiento de resultados
```

#### **🔧 UTILIDADES:**
```
python-decouple==3.8                 # Variables de entorno
Pillow==10.1.0                       # Procesamiento de imágenes
```

### **📊 DEPENDENCIAS DE DESARROLLO (requirements.dev.txt):**
```bash
# Instalar dependencias de desarrollo
pip install -r requirements.dev.txt
```

#### **🧪 TESTING:**
```
pytest==7.4.3                        # Framework de testing
pytest-django==4.7.0                 # Plugin Django para pytest
factory-boy==3.3.0                   # Generación de datos de prueba
coverage==7.3.2                       # Cobertura de código
```

#### **🔍 LINTING Y FORMATTING:**
```
flake8==6.1.0                        # Linter de código
black==23.11.0                        # Formateador de código
isort==5.12.0                         # Ordenamiento de imports
```

---

## 🗄️ **CONFIGURACIÓN DE BASE DE DATOS**

### **📊 MYSQL:**
```bash
# Instalar MySQL Server (Ubuntu/Debian)
sudo apt install mysql-server

# Iniciar servicio
sudo systemctl start mysql
sudo systemctl enable mysql

# Configurar seguridad
sudo mysql_secure_installation

# Crear base de datos
sudo mysql -u root -p
```

```sql
-- Crear base de datos
CREATE DATABASE backend_optimizacion CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Crear usuario
CREATE USER 'backend_user'@'localhost' IDENTIFIED BY 'tu_password_seguro';

-- Asignar permisos
GRANT ALL PRIVILEGES ON backend_optimizacion.* TO 'backend_user'@'localhost';
FLUSH PRIVILEGES;

-- Verificar
SHOW DATABASES;
SELECT User, Host FROM mysql.user;
```

### **🔧 CONFIGURACIÓN DJANGO:**
```python
# settings/settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'backend_optimizacion',
        'USER': 'backend_user',
        'PASSWORD': 'tu_password_seguro',
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'charset': 'utf8mb4',
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}
```

---

## 🔴 **CONFIGURACIÓN DE REDIS**

### **📦 INSTALACIÓN:**
```bash
# Ubuntu/Debian
sudo apt install redis-server

# CentOS/RHEL
sudo yum install redis

# macOS
brew install redis
```

### **⚙️ CONFIGURACIÓN:**
```bash
# Editar configuración
sudo nano /etc/redis/redis.conf

# Cambiar configuración de seguridad
bind 127.0.0.1
requirepass tu_password_redis

# Reiniciar servicio
sudo systemctl restart redis
sudo systemctl enable redis
```

### **🔧 CONFIGURACIÓN DJANGO:**
```python
# settings/settings.py
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_PASSWORD = 'tu_password_redis'

# Configuración de Celery
CELERY_BROKER_URL = f'redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/0'
CELERY_RESULT_BACKEND = f'redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/0'
```

---

## 🐳 **CONFIGURACIÓN DE DOCKER**

### **📁 ARCHIVOS DOCKER:**

#### **🐳 Dockerfile:**
```dockerfile
# Usar imagen base de Python
FROM python:3.11-slim

# Establecer directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements
COPY requirements.txt .

# Instalar dependencias Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código del proyecto
COPY . .

# Exponer puerto
EXPOSE 8000

# Comando de inicio
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "settings.wsgi:application"]
```

#### **🐙 docker-compose.prod.yml:**
```yaml
version: '3.8'

services:
  db:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: root_password
      MYSQL_DATABASE: backend_optimizacion
      MYSQL_USER: backend_user
      MYSQL_PASSWORD: user_password
    volumes:
      - db_data_prod:/var/lib/mysql
      - ./db/init.sql:/docker-entrypoint-initdb.d/init.sql
    ports:
      - "3306:3306"
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]
      timeout: 20s
      retries: 10

  redis:
    image: redis:7-alpine
    command: redis-server --requirepass redis_password
    volumes:
      - redis_data_prod:/data
    ports:
      - "6379:6379"
    healthcheck:
      test: ["CMD", "redis-cli", "--raw", "incr", "ping"]
      timeout: 3s
      retries: 5

  web:
    build: .
    environment:
      - DEBUG=False
      - DATABASE_URL=mysql://backend_user:user_password@db:3306/backend_optimizacion
      - REDIS_URL=redis://:redis_password@redis:6379/0
    volumes:
      - static_volume_prod:/app/staticfiles
      - media_volume_prod:/app/media
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_healthy
    ports:
      - "8000:8000"

  celery:
    build: .
    command: celery -A settings worker -l info
    environment:
      - DEBUG=False
      - DATABASE_URL=mysql://backend_user:user_password@db:3306/backend_optimizacion
      - REDIS_URL=redis://:redis_password@redis:6379/0
    volumes:
      - static_volume_prod:/app/staticfiles
      - media_volume_prod:/app/media
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_healthy

  celery-beat:
    build: .
    command: celery -A settings beat -l info
    environment:
      - DEBUG=False
      - DATABASE_URL=mysql://backend_user:user_password@db:3306/backend_optimizacion
      - REDIS_URL=redis://:redis_password@redis:6379/0
    volumes:
      - static_volume_prod:/app/staticfiles
      - media_volume_prod:/app/media
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_healthy

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.prod.conf:/etc/nginx/nginx.conf
      - ./nginx/default.prod.conf:/etc/nginx/conf.d/default.conf
      - static_volume_prod:/app/staticfiles
      - media_volume_prod:/app/media
    depends_on:
      web:
        condition: service_healthy

volumes:
  db_data_prod:
  redis_data_prod:
  static_volume_prod:
  media_volume_prod:
```

---

## 🌐 **CONFIGURACIÓN DE NGINX**

### **📁 nginx/nginx.prod.conf:**
```nginx
user nginx;
worker_processes auto;
error_log /var/log/nginx/error.log warn;
pid /var/run/nginx.pid;

events {
    worker_connections 1024;
}

http {
    include /etc/nginx/mime.types;
    default_type application/octet-stream;
    
    log_format main '$remote_addr - $remote_user [$time_local] "$request" '
                    '$status $body_bytes_sent "$http_referer" '
                    '"$http_user_agent" "$http_x_forwarded_for"';
    
    access_log /var/log/nginx/access.log main;
    
    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
    keepalive_timeout 65;
    types_hash_max_size 2048;
    
    # Gzip
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_proxied any;
    gzip_comp_level 6;
    gzip_types
        text/plain
        text/css
        text/xml
        text/javascript
        application/json
        application/javascript
        application/xml+rss
        application/atom+xml
        image/svg+xml;
    
    # Rate limiting
    limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
    
    include /etc/nginx/conf.d/*.conf;
}
```

### **📁 nginx/default.prod.conf:**
```nginx
upstream django {
    server web:8000;
}

server {
    listen 80;
    server_name localhost;
    
    # Rate limiting
    limit_req zone=api burst=20 nodelay;
    
    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header Referrer-Policy "no-referrer-when-downgrade" always;
    add_header Content-Security-Policy "default-src 'self' http: https: data: blob: 'unsafe-inline'" always;
    
    # Static files
    location /static/ {
        alias /app/staticfiles/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
    
    # Media files
    location /media/ {
        alias /app/media/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
    
    # API endpoints
    location /api/ {
        proxy_pass http://django;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Timeouts
        proxy_connect_timeout 30s;
        proxy_send_timeout 30s;
        proxy_read_timeout 30s;
    }
    
    # Admin interface
    location /admin/ {
        proxy_pass http://django;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    # Health check
    location /health/ {
        proxy_pass http://django;
        access_log off;
    }
}
```

---

## 🔧 **CONFIGURACIÓN DE CELERY**

### **📁 settings/celery.py:**
```python
import os
from celery import Celery

# Configurar variables de entorno
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.settings')

# Crear instancia de Celery
app = Celery('backend_optimizacion')

# Configurar Celery
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-descubrir tareas
app.autodiscover_tasks()

# Configuración de tareas
app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,  # 30 minutos
    task_soft_time_limit=25 * 60,  # 25 minutos
    worker_prefetch_multiplier=1,
    worker_max_tasks_per_child=1000,
)

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
```

### **📁 tasks/__init__.py:**
```python
# Importar tareas para que Celery las descubra
from . import email_tasks
from . import report_tasks
from . import maintenance_tasks
```

---

## 🔐 **CONFIGURACIÓN DE VARIABLES DE ENTORNO**

### **📁 .env (PRODUCCIÓN):**
```bash
# Configuración Django
DEBUG=False
SECRET_KEY=tu_clave_secreta_muy_larga_y_compleja_aqui
ALLOWED_HOSTS=localhost,127.0.0.1,tu-dominio.com

# Base de datos
DATABASE_URL=mysql://backend_user:user_password@localhost:3306/backend_optimizacion
DB_NAME=backend_optimizacion
DB_USER=backend_user
DB_PASSWORD=user_password
DB_HOST=localhost
DB_PORT=3306

# Redis
REDIS_URL=redis://:redis_password@localhost:6379/0
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=redis_password

# Celery
CELERY_BROKER_URL=redis://:redis_password@localhost:6379/0
CELERY_RESULT_BACKEND=redis://:redis_password@localhost:6379/0

# Email
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=tu-email@gmail.com
EMAIL_HOST_PASSWORD=tu-app-password

# Seguridad
CSRF_COOKIE_SECURE=True
SESSION_COOKIE_SECURE=True
SECURE_BROWSER_XSS_FILTER=True
SECURE_CONTENT_TYPE_NOSNIFF=True
SECURE_HSTS_SECONDS=31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS=True
SECURE_HSTS_PRELOAD=True

# Logging
LOG_LEVEL=INFO
LOG_FILE=/var/log/django/backend.log

# Archivos estáticos
STATIC_ROOT=/app/staticfiles
MEDIA_ROOT=/app/media
```

---

## 🚀 **SCRIPTS DE INICIO**

### **📁 start-prod.ps1 (Windows):**
```powershell
# Script de inicio para producción en Windows
Write-Host "🚀 Iniciando Backend-Optimizacion en PRODUCCIÓN..." -ForegroundColor Green

# Verificar Docker
if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Docker no está instalado o no está en el PATH" -ForegroundColor Red
    exit 1
}

# Verificar Docker Compose
if (-not (Get-Command docker-compose -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Docker Compose no está instalado o no está en el PATH" -ForegroundColor Red
    exit 1
}

# Construir y levantar servicios
Write-Host "🔨 Construyendo servicios..." -ForegroundColor Yellow
docker-compose -f docker-compose.prod.yml build

Write-Host "📦 Levantando servicios..." -ForegroundColor Yellow
docker-compose -f docker-compose.prod.yml up -d

# Verificar estado
Write-Host "🔍 Verificando estado de servicios..." -ForegroundColor Yellow
Start-Sleep -Seconds 10
docker-compose -f docker-compose.prod.yml ps

Write-Host "✅ Servicios iniciados correctamente!" -ForegroundColor Green
Write-Host "🌐 Aplicación disponible en: http://localhost" -ForegroundColor Cyan
Write-Host "📊 Admin Django en: http://localhost/admin" -ForegroundColor Cyan
```

### **📁 start-prod.sh (Linux/macOS):**
```bash
#!/bin/bash

# Script de inicio para producción en Linux/macOS
echo "🚀 Iniciando Backend-Optimizacion en PRODUCCIÓN..."

# Verificar Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker no está instalado o no está en el PATH"
    exit 1
fi

# Verificar Docker Compose
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose no está instalado o no está en el PATH"
    exit 1
fi

# Construir y levantar servicios
echo "🔨 Construyendo servicios..."
docker-compose -f docker-compose.prod.yml build

echo "📦 Levantando servicios..."
docker-compose -f docker-compose.prod.yml up -d

# Verificar estado
echo "🔍 Verificando estado de servicios..."
sleep 10
docker-compose -f docker-compose.prod.yml ps

echo "✅ Servicios iniciados correctamente!"
echo "🌐 Aplicación disponible en: http://localhost"
echo "📊 Admin Django en: http://localhost/admin"
```

---

## 🧪 **CONFIGURACIÓN DE TESTING**

### **📁 pytest.ini:**
```ini
[tool:pytest]
DJANGO_SETTINGS_MODULE = settings.settings
python_files = tests.py test_*.py *_tests.py
addopts = 
    --strict-markers
    --strict-config
    --verbose
    --tb=short
    --cov=.
    --cov-report=html
    --cov-report=term-missing
    --cov-fail-under=80
markers =
    slow: marks tests as slow (deselect with '-m "not slow"')
    integration: marks tests as integration tests
    unit: marks tests as unit tests
```

### **📁 .coveragerc:**
```ini
[run]
source = .
omit = 
    */tests/*
    */migrations/*
    */venv/*
    manage.py
    settings/*
    */__init__.py

[report]
exclude_lines =
    pragma: no cover
    def __repr__
    if self.debug:
    if settings.DEBUG
    raise AssertionError
    raise NotImplementedError
    if 0:
    if __name__ == .__main__.:
    class .*\bProtocol\):
    @(abc\.)?abstractmethod
```

---

## 🔍 **VERIFICACIÓN DE INSTALACIÓN**

### **✅ VERIFICAR DEPENDENCIAS:**
```bash
# Verificar Python
python --version
pip list

# Verificar Django
python manage.py check

# Verificar base de datos
python manage.py dbshell

# Verificar Redis
redis-cli ping

# Verificar Celery
celery -A settings status
```

### **🔧 VERIFICAR SERVICIOS:**
```bash
# Verificar servicios Docker
docker-compose -f docker-compose.prod.yml ps

# Verificar logs
docker-compose -f docker-compose.prod.yml logs

# Verificar salud de servicios
curl http://localhost/health/
```

---

## 🚨 **SOLUCIÓN DE PROBLEMAS COMUNES**

### **❌ ERROR: MySQL Connection Refused**
```bash
# Verificar servicio MySQL
sudo systemctl status mysql

# Reiniciar servicio
sudo systemctl restart mysql

# Verificar puerto
sudo netstat -tlnp | grep 3306
```

### **❌ ERROR: Redis Connection Refused**
```bash
# Verificar servicio Redis
sudo systemctl status redis

# Reiniciar servicio
sudo systemctl restart redis

# Verificar puerto
sudo netstat -tlnp | grep 6379
```

### **❌ ERROR: Permission Denied en Docker**
```bash
# Agregar usuario al grupo docker
sudo usermod -aG docker $USER

# Reiniciar sesión o ejecutar
newgrp docker
```

### **❌ ERROR: Port Already in Use**
```bash
# Verificar puertos en uso
sudo netstat -tlnp | grep :80
sudo netstat -tlnp | grep :8000

# Detener servicios que usen esos puertos
sudo systemctl stop nginx
sudo systemctl stop apache2
```

---

## 📚 **RECURSOS ADICIONALES**

### **🔗 ENLACES ÚTILES:**
- **Django Documentation**: https://docs.djangoproject.com/
- **Django REST Framework**: https://www.django-rest-framework.org/
- **Celery Documentation**: https://docs.celeryproject.org/
- **Redis Documentation**: https://redis.io/documentation
- **MySQL Documentation**: https://dev.mysql.com/doc/
- **Nginx Documentation**: https://nginx.org/en/docs/

### **📖 LIBROS RECOMENDADOS:**
- "Two Scoops of Django" - Daniel Greenfeld & Audrey Roy
- "Django REST Framework" - Tom Christie
- "Celery in Action" - Ask Solem
- "High Performance MySQL" - Baron Schwartz

---

## ✅ **ESTADO**
**COMPLETADO** - Guía completa de instalación y configuración de dependencias y librerías.

---

*README generado para el Punto 5 de la lista de documentación*
*Proyecto: Backend-Optimizacion*
