# 🐳 PUNTO 6: INSTRUCCIONES DE CÓMO SE HIZO EL DESPLIEGUE EN DOCKER Y QUÉ ARCHIVOS INTERACTÚAN

## 🔗 **NAVEGACIÓN RÁPIDA**

### **📚 DOCUMENTACIÓN PRINCIPAL**
- [🏠 **Volver al índice principal**](README.md)
- [⚙️ **PUNTO 5**: Instalación y configuración](README_PUNTO_5.md)
- [⌨️ **PUNTO 7**: Comandos del proyecto](README_PUNTO_7.md)
- [🚀 **PUNTO 8**: Flujo de ejecución](README_PUNTO_8.md)

### **📊 REPORTES ESPECIALIZADOS**
- [🏗️ **REPORTE**: Análisis de estructura del código](REPORTE_ESTRUCTURA_CODIGO.md)
- [🔄 **REPORTE**: Flujo de interacción del usuario](REPORTE_FLUJO_USUARIO.md)

### **🔗 NAVEGACIÓN INTERNA**
- [🐳 Arquitectura de Docker](#arquitectura-de-docker)
- [📁 Archivos de Docker involucrados](#archivos-de-docker-involucrados)
- [🔄 Flujo de despliegue](#flujo-de-despliegue)
- [⚙️ Configuración de servicios](#configuración-de-servicios)
- [🚀 Scripts de producción](#scripts-de-producción)
- [📊 Monitoreo y mantenimiento](#monitoreo-y-mantenimiento)

---

## 🎯 **OBJETIVO**
Documentar exhaustivamente el proceso de despliegue en Docker del proyecto Backend-Optimizacion, explicando qué archivos interactúan, cómo se configuran los servicios y cuál es el flujo completo de despliegue para producción.

## 📋 **ARQUITECTURA DE DESPLIEGUE DOCKER**

### **🏗️ DIAGRAMA DE SERVICIOS:**
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Nginx (80)    │    │  Django (8000)  │    │   MySQL (3306)  │
│   Proxy Reverso │◄──►│   Web App       │◄──►│   Base Datos    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Static Files  │    │   Celery        │    │   Redis (6379)  │
│   Media Files   │    │   Worker        │    │   Cache/Broker  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │  Celery Beat    │
                       │  Scheduler      │
                       └─────────────────┘
```

---

## 📁 **ARCHIVOS DE DESPLIEGUE DOCKER**

### **🔧 ARCHIVOS PRINCIPALES:**

#### **🐳 `Dockerfile` - Imagen de la Aplicación:**
```dockerfile
# Usar imagen base de Python 3.11
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

# Crear directorios necesarios
RUN mkdir -p /app/staticfiles /app/media /app/logs

# Exponer puerto
EXPOSE 8000

# Comando de inicio
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "settings.wsgi:application"]
```

**🔗 INTERACCIONES:**
- **`requirements.txt`**: Dependencias Python
- **`.`**: Todo el código del proyecto
- **`settings.wsgi:application`**: Punto de entrada Django

#### **🐙 `docker-compose.prod.yml` - Orquestación de Servicios:**
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

**🔗 INTERACCIONES:**
- **`./db/init.sql`**: Script de inicialización de base de datos
- **`./nginx/nginx.prod.conf`**: Configuración principal de Nginx
- **`./nginx/default.prod.conf`**: Configuración de sitio de Nginx
- **Volúmenes nombrados**: Persistencia de datos

#### **📁 `.dockerignore` - Exclusión de Archivos:**
```dockerignore
# Entornos virtuales
venv/
env/
.venv/

# Archivos de desarrollo
*.pyc
__pycache__/
.pytest_cache/
.coverage
htmlcov/

# Archivos de sistema
.DS_Store
Thumbs.db

# Archivos de Git
.git/
.gitignore

# Archivos de IDE
.vscode/
.idea/
*.swp
*.swo

# Archivos de Docker
Dockerfile*
docker-compose*
.dockerignore

# Archivos de configuración local
.env
.env.local
.env.prod

# Archivos de logs
*.log
logs/

# Archivos temporales
tmp/
temp/
```

---

## 🌐 **CONFIGURACIÓN DE NGINX**

### **📁 `nginx/nginx.prod.conf` - Configuración Principal:**
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

**🔗 INTERACCIONES:**
- **`/etc/nginx/mime.types`**: Tipos MIME del sistema
- **`/etc/nginx/conf.d/*.conf`**: Configuraciones de sitios

### **📁 `nginx/default.prod.conf` - Configuración del Sitio:**
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

**🔗 INTERACCIONES:**
- **`upstream django`**: Servidor Django (web:8000)
- **`/app/staticfiles/`**: Archivos estáticos de Django
- **`/app/media/`**: Archivos de media de Django

---

## 🗄️ **CONFIGURACIÓN DE BASE DE DATOS**

### **📁 `db/init.sql` - Inicialización de Base de Datos:**
```sql
-- Crear base de datos si no existe
CREATE DATABASE IF NOT EXISTS backend_optimizacion 
CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Usar la base de datos
USE backend_optimizacion;

-- Crear usuario si no existe
CREATE USER IF NOT EXISTS 'backend_user'@'%' IDENTIFIED BY 'user_password';

-- Asignar permisos
GRANT ALL PRIVILEGES ON backend_optimizacion.* TO 'backend_user'@'%';

-- Crear usuario para conexiones externas
CREATE USER IF NOT EXISTS 'backend_user'@'localhost' IDENTIFIED BY 'user_password';
GRANT ALL PRIVILEGES ON backend_optimizacion.* TO 'backend_user'@'localhost';

-- Aplicar cambios
FLUSH PRIVILEGES;

-- Verificar usuarios creados
SELECT User, Host FROM mysql.user WHERE User = 'backend_user';

-- Verificar base de datos
SHOW DATABASES LIKE 'backend_optimizacion';
```

**🔗 INTERACCIONES:**
- **`docker-compose.prod.yml`**: Montaje como volumen
- **MySQL container**: Ejecución automática al iniciar

---

## 🔐 **CONFIGURACIÓN DE VARIABLES DE ENTORNO**

### **📁 `.env` - Variables de Entorno:**
```bash
# Configuración Django
DEBUG=False
SECRET_KEY=tu_clave_secreta_muy_larga_y_compleja_aqui
ALLOWED_HOSTS=localhost,127.0.0.1,tu-dominio.com

# Base de datos
DATABASE_URL=mysql://backend_user:user_password@db:3306/backend_optimizacion
DB_NAME=backend_optimizacion
DB_USER=backend_user
DB_PASSWORD=user_password
DB_HOST=db
DB_PORT=3306

# Redis
REDIS_URL=redis://:redis_password@redis:6379/0
REDIS_HOST=redis
REDIS_PORT=6379
REDIS_PASSWORD=redis_password

# Celery
CELERY_BROKER_URL=redis://:redis_password@redis:6379/0
CELERY_RESULT_BACKEND=redis://:redis_password@redis:6379/0

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
LOG_FILE=/app/logs/backend.log

# Archivos estáticos
STATIC_ROOT=/app/staticfiles
MEDIA_ROOT=/app/media
```

**🔗 INTERACCIONES:**
- **`docker-compose.prod.yml`**: Referenciado en servicios
- **`settings/settings.py`**: Cargado por python-decouple
- **Contenedores**: Variables de entorno inyectadas

---

## 🚀 **PROCESO COMPLETO DE DESPLIEGUE**

### **📋 PASO A PASO:**

#### **1️⃣ PREPARACIÓN DEL ENTORNO:**
```bash
# Verificar Docker y Docker Compose
docker --version
docker compose version

# Verificar archivos de configuración
ls -la
# Debe mostrar:
# - Dockerfile
# - docker-compose.prod.yml
# - .env
# - nginx/nginx.prod.conf
# - nginx/default.prod.conf
# - db/init.sql
```

#### **2️⃣ CONSTRUCCIÓN DE IMÁGENES:**
```bash
# Construir todas las imágenes
docker compose -f docker-compose.prod.yml build

# Verificar imágenes construidas
docker images
```

#### **3️⃣ INICIO DE SERVICIOS:**
```bash
# Levantar todos los servicios
docker compose -f docker-compose.prod.yml up -d

# Verificar estado de servicios
docker compose -f docker-compose.prod.yml ps
```

#### **4️⃣ VERIFICACIÓN DE SALUD:**
```bash
# Verificar logs de servicios
docker compose -f docker-compose.prod.yml logs

# Verificar salud de servicios
docker compose -f docker-compose.prod.yml exec web python manage.py check
docker compose -f docker-compose.prod.yml exec db mysqladmin ping -h localhost
docker compose -f docker-compose.prod.yml exec redis redis-cli ping
```

#### **5️⃣ MIGRACIONES Y SETUP:**
```bash
# Ejecutar migraciones
docker compose -f docker-compose.prod.yml exec web python manage.py migrate

# Crear superusuario
docker compose -f docker-compose.prod.yml exec web python manage.py createsuperuser

# Recolectar archivos estáticos
docker compose -f docker-compose.prod.yml exec web python manage.py collectstatic --noinput
```

---

## 🔧 **SCRIPTS DE AUTOMATIZACIÓN**

### **📁 `start-prod.ps1` - Script Windows:**
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

### **📁 `start-prod.sh` - Script Linux/macOS:**
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

## 📊 **FLUJO DE INTERACCIÓN DE ARCHIVOS**

### **🔄 DIAGRAMA DE FLUJO:**
```
1. INICIO
   ↓
2. docker-compose.prod.yml
   ↓
3. Construcción de imágenes (Dockerfile)
   ↓
4. Inicio de servicios
   ↓
5. Configuración de volúmenes
   ↓
6. Inyección de variables (.env)
   ↓
7. Configuración de Nginx
   ↓
8. Proxy reverso a Django
   ↓
9. Conexión a MySQL y Redis
   ↓
10. Aplicación funcionando
```

### **🔗 INTERACCIONES DETALLADAS:**

#### **📁 `docker-compose.prod.yml` ↔ Otros archivos:**
- **`Dockerfile`**: Construcción de imagen web
- **`.env`**: Variables de entorno
- **`nginx/*.conf`**: Configuración de Nginx
- **`db/init.sql`**: Inicialización de base de datos

#### **📁 `Dockerfile` ↔ Archivos del proyecto:**
- **`requirements.txt`**: Dependencias Python
- **`.`**: Código fuente completo
- **`settings.wsgi:application`**: Punto de entrada

#### **📁 `nginx/*.conf` ↔ Servicios:**
- **`web:8000`**: Servidor Django
- **`/app/staticfiles`**: Archivos estáticos
- **`/app/media`**: Archivos de media

---

## 🚨 **SOLUCIÓN DE PROBLEMAS COMUNES**

### **❌ ERROR: Build Failed**
```bash
# Verificar Dockerfile
docker build -t test-image .

# Verificar requirements.txt
docker run --rm test-image pip list

# Verificar permisos
ls -la
```

### **❌ ERROR: Service Health Check Failed**
```bash
# Verificar logs del servicio
docker compose -f docker-compose.prod.yml logs [service_name]

# Verificar conectividad entre servicios
docker compose -f docker-compose.prod.yml exec web ping db
docker compose -f docker-compose.prod.yml exec web ping redis
```

### **❌ ERROR: Port Already in Use**
```bash
# Verificar puertos en uso
netstat -tlnp | grep :80
netstat -tlnp | grep :8000
netstat -tlnp | grep :3306
netstat -tlnp | grep :6379

# Detener servicios conflictivos
sudo systemctl stop nginx
sudo systemctl stop apache2
```

### **❌ ERROR: Volume Mount Failed**
```bash
# Verificar permisos de directorios
ls -la nginx/
ls -la db/

# Verificar existencia de archivos
file nginx/nginx.prod.conf
file db/init.sql
```

---

## 🔍 **VERIFICACIÓN DEL DESPLIEGUE**

### **✅ VERIFICAR SERVICIOS:**
```bash
# Estado de todos los servicios
docker compose -f docker-compose.prod.yml ps

# Logs en tiempo real
docker compose -f docker-compose.prod.yml logs -f

# Estadísticas de recursos
docker stats
```

### **✅ VERIFICAR CONECTIVIDAD:**
```bash
# Verificar puertos expuestos
docker compose -f docker-compose.prod.yml port nginx 80
docker compose -f docker-compose.prod.yml port web 8000
docker compose -f docker-compose.prod.yml port db 3306
docker compose -f docker-compose.prod.yml port redis 6379
```

### **✅ VERIFICAR APLICACIÓN:**
```bash
# Health check
curl http://localhost/health/

# API endpoints
curl http://localhost/api/

# Admin interface
curl http://localhost/admin/

# Archivos estáticos
curl http://localhost/static/
```

---

## 📈 **OPTIMIZACIONES DE PRODUCCIÓN**

### **🔧 OPTIMIZACIONES DE DOCKER:**
```dockerfile
# Multi-stage build para reducir tamaño
FROM python:3.11-slim as builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --user -r requirements.txt

FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY . .

ENV PATH=/root/.local/bin:$PATH
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "4", "settings.wsgi:application"]
```

### **🔧 OPTIMIZACIONES DE NGINX:**
```nginx
# Worker processes
worker_processes auto;

# Worker connections
worker_connections 1024;

# Gzip compression
gzip on;
gzip_vary on;
gzip_min_length 1024;
gzip_proxied any;
gzip_comp_level 6;

# Rate limiting
limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
```

---

## 📚 **RECURSOS ADICIONALES**

### **🔗 ENLACES ÚTILES:**
- **Docker Documentation**: https://docs.docker.com/
- **Docker Compose**: https://docs.docker.com/compose/
- **Nginx Documentation**: https://nginx.org/en/docs/
- **MySQL Docker**: https://hub.docker.com/_/mysql
- **Redis Docker**: https://hub.docker.com/_/redis

### **📖 COMANDOS ÚTILES:**
```bash
# Limpiar recursos Docker
docker system prune -a

# Ver logs de un servicio específico
docker compose -f docker-compose.prod.yml logs -f web

# Ejecutar comandos en contenedores
docker compose -f docker-compose.prod.yml exec web python manage.py shell

# Backup de base de datos
docker compose -f docker-compose.prod.yml exec db mysqldump -u root -p backend_optimizacion > backup.sql

# Restaurar base de datos
docker compose -f docker-compose.prod.yml exec -T db mysql -u root -p backend_optimizacion < backup.sql
```

---

## ✅ **ESTADO**
**COMPLETADO** - Instrucciones completas de despliegue en Docker y archivos que interactúan.

---

*README generado para el Punto 6 de la lista de documentación*
*Proyecto: Backend-Optimizacion*
