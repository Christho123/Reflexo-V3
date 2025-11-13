# ⌨️ PUNTO 7: DOCUMENTACIÓN DE LOS COMANDOS QUE SE UTILIZAN EN TODO EL PROYECTO

## 🔗 **NAVEGACIÓN RÁPIDA**

### **📚 DOCUMENTACIÓN PRINCIPAL**
- [🏠 **Volver al índice principal**](README.md)
- [🐳 **PUNTO 6**: Despliegue en Docker](README_PUNTO_6.md)
- [🚀 **PUNTO 8**: Flujo de ejecución](README_PUNTO_8.md)

### **📊 REPORTES ESPECIALIZADOS**
- [🏗️ **REPORTE**: Análisis de estructura del código](REPORTE_ESTRUCTURA_CODIGO.md)
- [🔄 **REPORTE**: Flujo de interacción del usuario](REPORTE_FLUJO_USUARIO.md)

### **🔗 NAVEGACIÓN INTERNA**
- [🐍 Comandos de Python/Django](#comandos-de-pythondjango)
- [🐳 Comandos de Docker](#comandos-de-docker)
- [📝 Comandos de Git](#comandos-de-git)
- [💻 Comandos de Python/PIP](#comandos-de-pythonpip)
- [🖥️ Comandos del sistema operativo](#comandos-del-sistema-operativo)
- [📊 Comandos de base de datos](#comandos-de-base-de-datos)
- [🔧 Comandos de mantenimiento](#comandos-de-mantenimiento)

---

## 🎯 **OBJETIVO**
Documentar exhaustivamente todos los comandos utilizados en el proyecto Backend-Optimizacion, incluyendo comandos de Django, Docker, Git, Python, y otros comandos del sistema necesarios para el desarrollo, despliegue y mantenimiento del proyecto.

## 📊 **ESTADÍSTICAS GENERALES DE COMANDOS**

- **Total de comandos documentados**: 80+ comandos
- **Categorías principales**: 8 categorías
- **Sistemas operativos**: Windows (PowerShell), Linux/Mac (Bash)
- **Entornos**: Desarrollo, Producción, Testing

---

## 🐍 **COMANDOS DE PYTHON Y DJANGO**

### **🚀 GESTIÓN DEL PROYECTO DJANGO**

#### **📁 CREACIÓN Y CONFIGURACIÓN INICIAL**
```bash
# Crear nuevo proyecto Django
django-admin startproject project_name

# Crear nueva aplicación Django
python manage.py startapp app_name

# Verificar configuración del proyecto
python manage.py check

# Verificar configuración del proyecto (producción)
python manage.py check --deploy
```

#### **🗄️ GESTIÓN DE BASE DE DATOS**
```bash
# Crear migraciones
python manage.py makemigrations

# Crear migraciones para aplicación específica
python manage.py makemigrations app_name

# Aplicar migraciones
python manage.py migrate

# Aplicar migraciones específicas
python manage.py migrate app_name

# Ver estado de migraciones
python manage.py showmigrations

# Ver estado de migraciones de aplicación específica
python manage.py showmigrations app_name

# Revertir migración específica
python manage.py migrate app_name 0001

# Crear superusuario
python manage.py createsuperuser

# Crear superusuario con datos específicos
python manage.py createsuperuser --username admin --email admin@example.com

# Shell de Django
python manage.py shell

# Shell de Django con IPython
python manage.py shell -i ipython

# Dump de datos
python manage.py dumpdata app_name.ModelName > data.json

# Load de datos
python manage.py loaddata data.json

# Flush de base de datos
python manage.py flush

# Reset de base de datos (elimina todas las tablas)
python manage.py reset_db
```

#### **🌐 SERVIDOR DE DESARROLLO**
```bash
# Iniciar servidor de desarrollo
python manage.py runserver

# Iniciar servidor en puerto específico
python manage.py runserver 8000

# Iniciar servidor en IP específica
python manage.py runserver 0.0.0.0:8000

# Iniciar servidor con configuración específica
python manage.py runserver --settings=settings.production
```

#### **🧪 TESTING Y CALIDAD DE CÓDIGO**
```bash
# Ejecutar tests
python manage.py test

# Ejecutar tests de aplicación específica
python manage.py test app_name

# Ejecutar tests con verbosidad
python manage.py test --verbosity=2

# Ejecutar tests específicos
python manage.py test app_name.tests.TestClass.test_method

# Ejecutar tests con coverage
coverage run --source='.' manage.py test
coverage report
coverage html

# Ejecutar tests con pytest
pytest

# Ejecutar tests con pytest y Django
pytest --reuse-db

# Ejecutar tests de integración
pytest tests/integration/

# Ejecutar tests unitarios
pytest tests/unit/
```

#### **🔧 UTILIDADES DJANGO**
```bash
# Validar modelos
python manage.py validate

# Ver comandos disponibles
python manage.py help

# Ver comandos de aplicación específica
python manage.py help app_name

# Collect static files
python manage.py collectstatic

# Collect static files sin confirmación
python manage.py collectstatic --noinput

# Clear cache
python manage.py clearcache

# Change password de usuario
python manage.py changepassword username

# Ver configuración actual
python manage.py diffsettings

# Ver variables de entorno
python manage.py show_urls
```

---

## 🐳 **COMANDOS DE DOCKER**

### **🏗️ CONSTRUCCIÓN DE IMÁGENES**
```bash
# Construir imagen Docker
docker build -t project_name .

# Construir imagen con tag específico
docker build -t project_name:latest .

# Construir imagen sin cache
docker build --no-cache -t project_name .

# Construir imagen con Dockerfile específico
docker build -f Dockerfile.prod -t project_name:prod .

# Construir imagen con argumentos de build
docker build --build-arg VERSION=1.0 -t project_name:1.0 .
```

### **🚀 GESTIÓN DE CONTENEDORES**
```bash
# Ejecutar contenedor
docker run -d --name container_name image_name

# Ejecutar contenedor con puertos
docker run -d -p 8000:8000 --name container_name image_name

# Ejecutar contenedor con variables de entorno
docker run -d -e DEBUG=False -e SECRET_KEY=key --name container_name image_name

# Ejecutar contenedor con volúmenes
docker run -d -v /host/path:/container/path --name container_name image_name

# Ejecutar contenedor interactivo
docker run -it --name container_name image_name /bin/bash

# Ejecutar contenedor en background
docker run -d --name container_name image_name

# Ejecutar comando en contenedor existente
docker exec -it container_name /bin/bash

# Ejecutar comando específico
docker exec container_name python manage.py migrate
```

### **📋 GESTIÓN DE CONTENEDORES**
```bash
# Listar contenedores en ejecución
docker ps

# Listar todos los contenedores
docker ps -a

# Detener contenedor
docker stop container_name

# Iniciar contenedor
docker start container_name

# Reiniciar contenedor
docker restart container_name

# Eliminar contenedor
docker rm container_name

# Eliminar contenedor forzadamente
docker rm -f container_name

# Ver logs de contenedor
docker logs container_name

# Ver logs en tiempo real
docker logs -f container_name

# Ver logs con timestamps
docker logs -t container_name
```

### **🖼️ GESTIÓN DE IMÁGENES**
```bash
# Listar imágenes
docker images

# Eliminar imagen
docker rmi image_name

# Eliminar imagen forzadamente
docker rmi -f image_name

# Eliminar imágenes no utilizadas
docker image prune

# Eliminar todas las imágenes no utilizadas
docker image prune -a

# Ver información de imagen
docker inspect image_name

# Ver historial de imagen
docker history image_name
```

### **🌐 DOCKER COMPOSE**
```bash
# Iniciar servicios
docker-compose up

# Iniciar servicios en background
docker-compose up -d

# Iniciar servicios específicos
docker-compose up web db

# Iniciar servicios con archivo específico
docker-compose -f docker-compose.prod.yml up

# Detener servicios
docker-compose down

# Detener servicios y eliminar volúmenes
docker-compose down -v

# Reconstruir servicios
docker-compose build

# Reconstruir servicio específico
docker-compose build web

# Ver logs de servicios
docker-compose logs

# Ver logs de servicio específico
docker-compose logs web

# Ver logs en tiempo real
docker-compose logs -f

# Ejecutar comando en servicio
docker-compose exec web python manage.py migrate

# Ejecutar comando en servicio con usuario específico
docker-compose exec -u root web python manage.py collectstatic

# Ver estado de servicios
docker-compose ps

# Escalar servicios
docker-compose up --scale web=3
```

---

## 🔧 **COMANDOS DE GIT**

### **📁 GESTIÓN DE REPOSITORIOS**
```bash
# Clonar repositorio
git clone https://github.com/user/repository.git

# Clonar repositorio en directorio específico
git clone https://github.com/user/repository.git project_name

# Clonar repositorio con rama específica
git clone -b branch_name https://github.com/user/repository.git

# Inicializar repositorio Git
git init

# Agregar remote origin
git remote add origin https://github.com/user/repository.git

# Ver remotes configurados
git remote -v

# Cambiar URL del remote
git remote set-url origin https://github.com/user/new_repository.git
```

### **📝 GESTIÓN DE CAMBIOS**
```bash
# Ver estado del repositorio
git status

# Ver cambios en archivos
git diff

# Ver cambios staged
git diff --cached

# Agregar archivos al staging
git add filename

# Agregar todos los archivos
git add .

# Agregar archivos por patrón
git add *.py

# Remover archivos del staging
git reset HEAD filename

# Hacer commit
git commit -m "Mensaje del commit"

# Hacer commit con todos los cambios staged
git commit -am "Mensaje del commit"

# Modificar último commit
git commit --amend -m "Nuevo mensaje"
```

### **🌿 GESTIÓN DE RAMAS**
```bash
# Ver ramas
git branch

# Ver todas las ramas
git branch -a

# Crear nueva rama
git branch branch_name

# Crear y cambiar a nueva rama
git checkout -b branch_name

# Cambiar de rama
git checkout branch_name

# Cambiar de rama (nueva sintaxis)
git switch branch_name

# Eliminar rama
git branch -d branch_name

# Eliminar rama forzadamente
git branch -D branch_name

# Renombrar rama actual
git branch -m new_name

# Ver ramas remotas
git branch -r
```

### **🔄 SINCRONIZACIÓN CON REMOTO**
```bash
# Descargar cambios del remoto
git fetch

# Descargar cambios de rama específica
git fetch origin branch_name

# Ver cambios entre local y remoto
git log HEAD..origin/main

# Hacer pull de cambios
git pull

# Hacer pull de rama específica
git pull origin branch_name

# Hacer push de cambios
git push

# Hacer push de rama específica
git push origin branch_name

# Hacer push de nueva rama
git push -u origin branch_name

# Ver commits no sincronizados
git log origin/main..HEAD
```

### **📋 HISTORIAL Y LOGS**
```bash
# Ver historial de commits
git log

# Ver historial con gráfico
git log --graph --oneline --all

# Ver historial de archivo específico
git log --follow filename

# Ver cambios en commit específico
git show commit_hash

# Ver cambios entre commits
git diff commit1..commit2

# Ver estadísticas de cambios
git log --stat

# Ver commits de autor específico
git log --author="Author Name"
```

---

## 🐍 **COMANDOS DE PYTHON Y PIP**

### **📦 GESTIÓN DE DEPENDENCIAS**
```bash
# Instalar paquete
pip install package_name

# Instalar paquete con versión específica
pip install package_name==1.0.0

# Instalar paquete con versión mínima
pip install package_name>=1.0.0

# Instalar paquetes desde requirements.txt
pip install -r requirements.txt

# Instalar paquetes en modo desarrollo
pip install -e .

# Desinstalar paquete
pip uninstall package_name

# Listar paquetes instalados
pip list

# Listar paquetes con formato
pip list --format=freeze

# Ver información de paquete
pip show package_name

# Ver paquetes obsoletos
pip list --outdated

# Actualizar paquete
pip install --upgrade package_name

# Actualizar pip
pip install --upgrade pip
```

### **🔍 VIRTUAL ENVIRONMENTS**
```bash
# Crear virtual environment
python -m venv venv_name

# Crear virtual environment con Python específico
python3.9 -m venv venv_name

# Activar virtual environment (Windows)
venv_name\Scripts\activate

# Activar virtual environment (Linux/Mac)
source venv_name/bin/activate

# Desactivar virtual environment
deactivate

# Ver virtual environment activo
which python

# Ver paquetes en virtual environment
pip list

# Crear requirements.txt
pip freeze > requirements.txt

# Instalar desde requirements.txt
pip install -r requirements.txt
```

### **🧪 TESTING Y LINTING**
```bash
# Ejecutar tests con pytest
pytest

# Ejecutar tests con coverage
pytest --cov=app_name

# Ejecutar tests específicos
pytest tests/test_file.py::test_function

# Ejecutar tests con verbosidad
pytest -v

# Ejecutar tests y generar reporte HTML
pytest --cov=app_name --cov-report=html

# Ejecutar linting con flake8
flake8 .

# Ejecutar linting con black
black .

# Ejecutar linting con isort
isort .

# Ejecutar linting con mypy
mypy .
```

---

## 🖥️ **COMANDOS DEL SISTEMA OPERATIVO**

### **📁 GESTIÓN DE ARCHIVOS Y DIRECTORIOS**

#### **Windows (PowerShell)**
```powershell
# Listar archivos y directorios
Get-ChildItem
ls
dir

# Listar archivos recursivamente
Get-ChildItem -Recurse
ls -r

# Crear directorio
New-Item -ItemType Directory -Name "nombre_directorio"
mkdir nombre_directorio

# Eliminar directorio
Remove-Item -Recurse -Force "nombre_directorio"
rmdir nombre_directorio

# Copiar archivo
Copy-Item "origen" "destino"
cp origen destino

# Mover archivo
Move-Item "origen" "destino"
mv origen destino

# Eliminar archivo
Remove-Item "archivo"
del archivo

# Ver contenido de archivo
Get-Content "archivo"
cat archivo

# Buscar archivos
Get-ChildItem -Recurse -Filter "*.py"
```

#### **Linux/Mac (Bash)**
```bash
# Listar archivos y directorios
ls
ls -la

# Listar archivos recursivamente
ls -R
find . -type f

# Crear directorio
mkdir nombre_directorio

# Eliminar directorio
rmdir nombre_directorio
rm -rf nombre_directorio

# Copiar archivo
cp origen destino

# Mover archivo
mv origen destino

# Eliminar archivo
rm archivo

# Ver contenido de archivo
cat archivo
less archivo

# Buscar archivos
find . -name "*.py"
find . -type f -name "*.py"
```

### **🔍 BÚSQUEDA Y FILTRADO**

#### **Windows (PowerShell)**
```powershell
# Buscar texto en archivos
Select-String "texto" -Path "*.py" -Recurse

# Buscar archivos por extensión
Get-ChildItem -Recurse -Filter "*.py"

# Buscar archivos por nombre
Get-ChildItem -Recurse -Filter "*nombre*"

# Filtrar por tamaño
Get-ChildItem -Recurse | Where-Object {$_.Length -gt 1MB}
```

#### **Linux/Mac (Bash)**
```bash
# Buscar texto en archivos
grep "texto" *.py
grep -r "texto" .

# Buscar archivos por extensión
find . -name "*.py"

# Buscar archivos por nombre
find . -name "*nombre*"

# Filtrar por tamaño
find . -size +1M
```

### **🌐 RED Y CONECTIVIDAD**

#### **Windows (PowerShell)**
```powershell
# Ver IP del sistema
Get-NetIPAddress
ipconfig

# Ver conexiones de red
Get-NetConnection
netstat -an

# Hacer ping
Test-Connection "hostname"
ping hostname

# Ver DNS
nslookup hostname
```

#### **Linux/Mac (Bash)**
```bash
# Ver IP del sistema
ip addr show
ifconfig

# Ver conexiones de red
netstat -an
ss -tuln

# Hacer ping
ping hostname

# Ver DNS
nslookup hostname
dig hostname
```

---

## 📊 **COMANDOS DE MONITOREO Y MANTENIMIENTO**

### **💾 GESTIÓN DE BASE DE DATOS**
```bash
# Conectar a MySQL
mysql -u username -p database_name

# Conectar a MySQL con host específico
mysql -h hostname -u username -p database_name

# Backup de base de datos
mysqldump -u username -p database_name > backup.sql

# Restore de base de datos
mysql -u username -p database_name < backup.sql

# Ver procesos de MySQL
mysql -u username -p -e "SHOW PROCESSLIST;"

# Ver variables de MySQL
mysql -u username -p -e "SHOW VARIABLES;"
```

### **📈 MONITOREO DE SISTEMA**
```bash
# Ver uso de CPU y memoria
top
htop

# Ver uso de disco
df -h
du -sh *

# Ver procesos
ps aux
ps aux | grep python

# Ver puertos en uso
netstat -tuln
ss -tuln

# Ver logs del sistema
tail -f /var/log/syslog
journalctl -f
```

### **🔧 MANTENIMIENTO DEL SISTEMA**
```bash
# Actualizar paquetes (Ubuntu/Debian)
sudo apt update
sudo apt upgrade

# Actualizar paquetes (CentOS/RHEL)
sudo yum update

# Limpiar cache de paquetes
sudo apt clean
sudo yum clean all

# Ver espacio en disco
df -h
du -sh /*

# Limpiar logs antiguos
sudo find /var/log -type f -name "*.log" -mtime +30 -delete
```

---

## 🚀 **COMANDOS DE DESPLIEGUE Y PRODUCCIÓN**

### **🌐 SERVIDOR WEB (NGINX)**
```bash
# Verificar configuración de Nginx
nginx -t

# Recargar configuración de Nginx
sudo nginx -s reload

# Reiniciar Nginx
sudo systemctl restart nginx

# Ver estado de Nginx
sudo systemctl status nginx

# Ver logs de Nginx
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log

# Ver configuración de Nginx
nginx -T
```

### **🐍 SERVIDOR DE APLICACIÓN (GUNICORN)**
```bash
# Iniciar Gunicorn
gunicorn project.wsgi:application

# Iniciar Gunicorn con configuración
gunicorn --bind 0.0.0.0:8000 --workers 4 project.wsgi:application

# Iniciar Gunicorn con archivo de configuración
gunicorn -c gunicorn.conf.py project.wsgi:application

# Ver procesos de Gunicorn
ps aux | grep gunicorn

# Matar procesos de Gunicorn
pkill gunicorn
```

### **📊 MONITOREO DE PRODUCCIÓN**
```bash
# Ver logs de aplicación
tail -f logs/app.log

# Ver logs de errores
tail -f logs/error.log

# Ver uso de recursos
htop
iotop

# Ver conexiones de red
netstat -tuln | grep :8000

# Ver procesos de Python
ps aux | grep python

# Ver uso de memoria
free -h
```

---

## 📋 **SCRIPTS Y AUTOMATIZACIÓN**

### **🔄 SCRIPTS DE DESPLIEGUE**
```bash
# Script de inicio de producción
./start-prod.sh

# Script de inicio de producción (Windows)
.\start-prod.ps1

# Script de verificación
./verify-prod.sh

# Script de backup
./backup-db.sh

# Script de limpieza
./cleanup.sh
```

### **🔧 SCRIPTS DE MANTENIMIENTO**
```bash
# Script de actualización
./update.sh

# Script de backup automático
./auto-backup.sh

# Script de limpieza de logs
./clean-logs.sh

# Script de monitoreo
./monitor.sh
```

---

## ✅ **ESTADO**
**COMPLETADO** - Documentación exhaustiva de todos los comandos utilizados en el proyecto.

---

*README generado para el Punto 7 de la lista de documentación*
*Proyecto: Backend-Optimizacion*
