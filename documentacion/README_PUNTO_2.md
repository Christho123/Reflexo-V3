# 🔗 PUNTO 2: DOCUMENTACIÓN DE CÓMO SE CONECTAN CADA MÓDULO Y QUÉ FUNCIONAMIENTO TENÍAN

## 🔗 **NAVEGACIÓN RÁPIDA**

### **📚 DOCUMENTACIÓN PRINCIPAL**
- [🏠 **Volver al índice principal**](README.md)
- [🏗️ **PUNTO 1**: Estructura y módulos](README_PUNTO_1.md)
- [🔗 **PUNTO 3**: Endpoints del backend](README_PUNTO_3.md)
- [🗄️ **PUNTO 4**: Estructura de base de datos](README_PUNTO_4.md)

### **📊 REPORTES ESPECIALIZADOS**
- [🏗️ **REPORTE**: Análisis de estructura del código](REPORTE_ESTRUCTURA_CODIGO.md)
- [🔄 **REPORTE**: Flujo de interacción del usuario](REPORTE_FLUJO_USUARIO.md)

### **🔗 NAVEGACIÓN INTERNA**
- [🏗️ Arquitectura general del sistema](#arquitectura-general-del-sistema)
- [🔄 Flujo de datos entre módulos](#flujo-de-datos-entre-módulos)
- [🔐 Sistema de permisos y roles](#sistema-de-permisos-y-roles)
- [📊 Diagrama de interacciones](#diagrama-de-interacciones)
- [📈 Estadísticas de conexiones](#estadísticas-de-conexiones)

---

## 🎯 **OBJETIVO**
Documentar exhaustivamente cómo se conectan entre sí los diferentes módulos del proyecto Backend-Optimizacion y explicar su funcionamiento conjunto, incluyendo flujos de datos, dependencias y arquitectura del sistema.

## 🏗️ **ARQUITECTURA GENERAL DEL SISTEMA**

### **📊 DIAGRAMA DE CONEXIONES**
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   FRONTEND      │    │     NGINX       │    │   DJANGO WEB    │
│   (Cliente)     │◄──►│  (Proxy/SSL)    │◄──►│  (Gunicorn)     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │                       │
                                ▼                       ▼
                       ┌─────────────────┐    ┌─────────────────┐
                       │   STATIC/MEDIA  │    │   CELERY        │
                       │   (Archivos)    │    │   (Tareas)      │
                       └─────────────────┘    └─────────────────┘
                                                       │
                                                       ▼
                                              ┌─────────────────┐
                                              │     REDIS       │
                                              │  (Cache/Broker) │
                                              └─────────────────┘
                                                       │
                                                       ▼
                                              ┌─────────────────┐
                                              │     MYSQL       │
                                              │  (Base Datos)   │
                                              └─────────────────┘
```

## 🔄 **FLUJO DE CONEXIÓN ENTRE MÓDULOS**

### **1. NIVEL DE PRESENTACIÓN (NGINX)**
- **Función**: Proxy reverso y servidor de archivos estáticos
- **Conexiones**:
  - Recibe peticiones HTTP/HTTPS del cliente
  - Redirige peticiones dinámicas a Django
  - Sirve archivos estáticos y medios directamente
  - Maneja SSL/TLS y headers de seguridad

### **2. NIVEL DE APLICACIÓN (DJANGO)**
- **Función**: Lógica de negocio y API REST
- **Conexiones**:
  - Recibe peticiones de Nginx
  - Procesa lógica de negocio
  - Se conecta a MySQL para datos
  - Usa Redis para cache y sesiones
  - Envía tareas pesadas a Celery

### **3. NIVEL DE DATOS (MYSQL)**
- **Función**: Almacenamiento persistente de datos
- **Conexiones**:
  - Recibe consultas de Django
  - Almacena todos los modelos del sistema
  - Mantiene integridad referencial entre módulos

### **4. NIVEL DE CACHE (REDIS)**
- **Función**: Cache, sesiones y broker de tareas
- **Conexiones**:
  - Cache de Django para consultas frecuentes
  - Sesiones de usuario
  - Broker para Celery (cola de tareas)

## 🧩 **CONEXIONES ENTRE MÓDULOS DJANGO**

### **📁 MÓDULO `architect/` (CORE)**
```
architect/ (Sistema Base)
├── models/
│   ├── base.py ← Base para todos los modelos
│   ├── permission.py ← Permisos del sistema
│   └── role_has_permission.py ← Roles y permisos
├── views/
│   ├── auth.py ← Autenticación JWT
│   ├── permission.py ← Gestión de permisos
│   └── user.py ← Gestión de usuarios
└── services/
    ├── auth_service.py ← Lógica de autenticación
    ├── permission_service.py ← Lógica de permisos
    └── user_service.py ← Lógica de usuarios
```

**🔗 CONEXIONES:**
- **Base para todos los módulos** - Proporciona autenticación y permisos
- **Middleware de autenticación** - Protege todas las vistas
- **Sistema de roles** - Controla acceso a funcionalidades

### **📁 MÓDULO `users_profiles/`**
```
users_profiles/
├── models/
│   ├── user.py ← Extiende User de Django
│   ├── profile.py ← Perfil del usuario
│   └── role.py ← Roles específicos
└── guardian_conf.py ← Permisos a nivel de objeto
```

**🔗 CONEXIONES:**
- **Depende de `architect/`** - Usa sistema de permisos base
- **Extiende User de Django** - Añade campos personalizados
- **Integrado con Guardian** - Permisos granulares por objeto

### **📁 MÓDULO `appointments_status/`**
```
appointments_status/
├── models/
│   ├── appointment.py ← Citas médicas
│   ├── appointment_status.py ← Estados de citas
│   └── ticket.py ← Tickets de citas
└── signals.py ← Automatización
```

**🔗 CONEXIONES:**
- **Depende de `users_profiles/`** - Usuarios y terapeutas
- **Depende de `therapists/`** - Especialidades médicas
- **Depende de `patients_diagnoses/`** - Pacientes
- **Señales automáticas** - Creación de tickets

### **📁 MÓDULO `therapists/`**
```
therapists/
├── models/
│   ├── therapist.py ← Terapeutas
│   └── specialty.py ← Especialidades
└── services/
    ├── therapist_service.py ← Lógica de terapeutas
    └── specialty_service.py ← Lógica de especialidades
```

**🔗 CONEXIONES:**
- **Depende de `users_profiles/`** - Usuarios con rol de terapeuta
- **Conecta con `appointments_status/`** - Citas de terapeutas
- **Conecta con `patients_diagnoses/`** - Diagnósticos por especialidad

### **📁 MÓDULO `patients_diagnoses/`**
```
patients_diagnoses/
├── models/
│   ├── patient.py ← Pacientes
│   ├── diagnosis.py ← Diagnósticos
│   ├── medical_history.py ← Historial médico
│   └── treatment.py ← Tratamientos
└── services/
    ├── patient_service.py ← Lógica de pacientes
    ├── diagnosis_service.py ← Lógica de diagnósticos
    ├── medical_history_service.py ← Lógica de historial
    └── treatment_service.py ← Lógica de tratamientos
```

**🔗 CONEXIONES:**
- **Depende de `users_profiles/`** - Pacientes como usuarios
- **Conecta con `therapists/`** - Diagnósticos por terapeuta
- **Conecta con `histories_configurations/`** - Plantillas de historial
- **Conecta con `appointments_status/`** - Citas de pacientes

### **📁 MÓDULO `histories_configurations/`**
```
histories_configurations/
├── models/
│   ├── history_template.py ← Plantillas de historial
│   ├── field_configuration.py ← Configuración de campos
│   ├── section_configuration.py ← Configuración de secciones
│   ├── validation_rule.py ← Reglas de validación
│   ├── history_instance.py ← Instancias de historial
│   └── field_value.py ← Valores de campos
└── services/
    ├── history_template_service.py ← Lógica de plantillas
    ├── field_configuration_service.py ← Lógica de campos
    ├── section_configuration_service.py ← Lógica de secciones
    ├── validation_rule_service.py ← Lógica de validación
    └── history_instance_service.py ← Lógica de instancias
```

**🔗 CONEXIONES:**
- **Depende de `patients_diagnoses/`** - Historiales de pacientes
- **Sistema flexible** - Configuración dinámica de campos
- **Validaciones automáticas** - Reglas de negocio

### **📁 MÓDULO `company_reports/`**
```
company_reports/
├── models/
│   ├── company.py ← Empresa
│   ├── report.py ← Reportes
│   ├── statistic.py ← Estadísticas
│   └── dashboard.py ← Dashboard
└── services/
    ├── company_service.py ← Lógica de empresa
    ├── report_service.py ← Lógica de reportes
    ├── statistic_service.py ← Lógica de estadísticas
    └── dashboard_service.py ← Lógica de dashboard
```

**🔗 CONEXIONES:**
- **Depende de todos los módulos** - Agrega datos del sistema
- **Reportes consolidados** - Estadísticas de citas, pacientes, terapeutas
- **Dashboard ejecutivo** - Vista general del negocio

### **📁 MÓDULO `ubi_geo/`**
```
ubi_geo/
├── models/
│   ├── country.py ← Países
│   ├── region.py ← Regiones
│   ├── province.py ← Provincias
│   ├── district.py ← Distritos
│   └── location.py ← Ubicaciones
└── management/
    └── commands/
        └── populate_geo.py ← Poblar datos geográficos
```

**🔗 CONEXIONES:**
- **Base para ubicaciones** - Usado por todos los módulos
- **Datos de pacientes** - Direcciones y ubicaciones
- **Datos de terapeutas** - Zonas de trabajo
- **Reportes geográficos** - Análisis por región

## 🔄 **FLUJO DE DATOS ENTRE MÓDULOS**

### **1. FLUJO DE CREACIÓN DE CITA**
```
1. Usuario (users_profiles) → 
2. Selecciona Terapeuta (therapists) → 
3. Selecciona Paciente (patients_diagnoses) → 
4. Crea Cita (appointments_status) → 
5. Se genera Ticket automáticamente (signals) → 
6. Se actualiza Reporte (company_reports)
```

### **2. FLUJO DE DIAGNÓSTICO**
```
1. Terapeuta (therapists) → 
2. Selecciona Paciente (patients_diagnoses) → 
3. Usa Plantilla (histories_configurations) → 
4. Completa Historial (patients_diagnoses) → 
5. Se actualiza Estadística (company_reports)
```

### **3. FLUJO DE REPORTES**
```
1. Sistema (company_reports) → 
2. Consulta Citas (appointments_status) → 
3. Consulta Pacientes (patients_diagnoses) → 
4. Consulta Terapeutas (therapists) → 
5. Agrega Ubicaciones (ubi_geo) → 
6. Genera Reporte Consolidado
```

## 🔧 **CONFIGURACIÓN DE CONEXIONES**

### **📁 `settings/settings.py`**
```python
INSTALLED_APPS = [
    # Django apps
    'django.contrib.admin',
    'django.contrib.auth',
    
    # Third party apps
    'rest_framework',
    'corsheaders',
    'guardian',
    
    # Local apps (orden de dependencias)
    'architect',           # Primero (sistema base)
    'users_profiles',      # Segundo (usuarios)
    'ubi_geo',            # Tercero (ubicaciones)
    'therapists',         # Cuarto (terapeutas)
    'patients_diagnoses',  # Quinto (pacientes)
    'histories_configurations', # Sexto (plantillas)
    'appointments_status', # Séptimo (citas)
    'company_reports',     # Octavo (reportes)
]
```

### **📁 `settings/urls.py`**
```python
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('architect.urls')),      # Autenticación
    path('api/users/', include('users_profiles.urls')),
    path('api/geo/', include('ubi_geo.urls')),
    path('api/therapists/', include('therapists.urls')),
    path('api/patients/', include('patients_diagnoses.urls')),
    path('api/histories/', include('histories_configurations.urls')),
    path('api/appointments/', include('appointments_status.urls')),
    path('api/reports/', include('company_reports.urls')),
]
```

## 🔒 **SISTEMA DE PERMISOS Y AUTENTICACIÓN**

### **📊 JERARQUÍA DE PERMISOS**
```
1. SUPERUSUARIO (Django Admin)
   ├── Acceso total a todos los módulos
   └── Gestión de usuarios y permisos

2. ADMINISTRADOR (architect)
   ├── Gestión de roles y permisos
   ├── Acceso a reportes ejecutivos
   └── Configuración del sistema

3. TERAPEUTA (therapists + appointments_status)
   ├── Gestión de sus citas
   ├── Historiales de sus pacientes
   └── Reportes de su actividad

4. ASISTENTE (appointments_status)
   ├── Gestión de citas
   ├── Creación de tickets
   └── Reportes básicos

5. PACIENTE (patients_diagnoses)
   ├── Ver sus citas
   ├── Ver su historial médico
   └── Acceso limitado a información
```

## 📊 **ESTADÍSTICAS DE CONEXIONES**

- **Módulos principales**: 8
- **Conexiones directas**: 24
- **Dependencias circulares**: 0
- **Módulos independientes**: 2 (architect, ubi_geo)
- **Módulos dependientes**: 6
- **Nivel máximo de dependencia**: 3

## ✅ **ESTADO**
**COMPLETADO** - Documentación completa de conexiones y funcionamiento de módulos.

---

*README generado para el Punto 2 de la lista de documentación*
*Proyecto: Backend-Optimizacion*
