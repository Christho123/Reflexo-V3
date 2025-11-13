# 🗄️ PUNTO 4: DOCUMENTACIÓN DE LA BASE DE DATOS COMO SE RELACIONAN LAS TABLAS Y QUÉ MÓDULOS INTERACTÚAN

## 🔗 **NAVEGACIÓN RÁPIDA**

### **📚 DOCUMENTACIÓN PRINCIPAL**
- [🏠 **Volver al índice principal**](README.md)
- [🏗️ **PUNTO 1**: Estructura y módulos](README_PUNTO_1.md)
- [🔗 **PUNTO 2**: Conexiones entre módulos](README_PUNTO_2.md)
- [🔗 **PUNTO 3**: Endpoints del backend](README_PUNTO_3.md)

### **📊 REPORTES ESPECIALIZADOS**
- [🏗️ **REPORTE**: Análisis de estructura del código](REPORTE_ESTRUCTURA_CODIGO.md)
- [🔄 **REPORTE**: Flujo de interacción del usuario](REPORTE_FLUJO_USUARIO.md)

### **🔗 NAVEGACIÓN INTERNA**
- [🗄️ Tablas principales](#tablas-principales)
- [🔗 Relaciones entre entidades](#relaciones-entre-entidades)
- [📊 Diagrama general de relaciones](#diagrama-general-de-relaciones)
- [🔐 Restricciones de integridad](#restricciones-de-integridad)
- [⚡ Optimizaciones recomendadas](#optimizaciones-recomendadas)
- [🔄 Proceso de migración](#proceso-de-migración)

---

## 🎯 **OBJETIVO**
Documentar exhaustivamente la estructura de la base de datos del proyecto Backend-Optimizacion, incluyendo todas las tablas, sus relaciones, y cómo interactúan los diferentes módulos a través de la base de datos.

## 📊 **ESTADÍSTICAS GENERALES DE LA BASE DE DATOS**

- **Total de tablas**: 25+ tablas principales
- **Módulos con modelos**: 8 módulos principales
- **Tipo de base de datos**: MySQL
- **Motor de base de datos**: InnoDB
- **Características**: Transaccional, con integridad referencial

---

## 🔗 **DIAGRAMA GENERAL DE RELACIONES**

```
                    ┌─────────────────┐
                    │   auth_user     │ ← Django User
                    └─────────┬───────┘
                              │
                    ┌─────────▼───────┐
                    │  UserProfile    │ ← users_profiles
                    └─────────┬───────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
┌───────▼────────┐    ┌──────▼──────┐    ┌────────▼────────┐
│   Therapist    │    │   Patient   │    │   Role          │
│                │    │             │    │                 │
└─────┬──────────┘    └─────┬───────┘    └─────┬───────────┘
      │                     │                  │
      │                     │                  │
┌─────▼────────┐    ┌──────▼──────┐    ┌─────▼───────────┐
│ Specialty    │    │  Diagnosis  │    │  Permission    │
│              │    │             │    │                 │
└──────────────┘    └─────┬───────┘    └─────────────────┘
                          │
                          │
                    ┌─────▼────────┐
                    │  Treatment   │
                    │              │
                    └──────────────┘
```

---

## 🏗️ **ARQUITECTURA DE LA BASE DE DATOS**

### **📁 MÓDULO `architect/` - SISTEMA BASE**

#### **🔐 TABLA: `auth_user` (Django Built-in)**
```sql
CREATE TABLE auth_user (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    password VARCHAR(128) NOT NULL,
    last_login DATETIME,
    is_superuser BOOLEAN NOT NULL,
    username VARCHAR(150) UNIQUE NOT NULL,
    first_name VARCHAR(150),
    last_name VARCHAR(150),
    email VARCHAR(254),
    is_staff BOOLEAN NOT NULL,
    is_active BOOLEAN NOT NULL,
    date_joined DATETIME NOT NULL
);
```

**🔗 RELACIONES:**
- **1:1** con `UserProfile` (users_profiles)
- **1:N** con `Therapist` (therapists)
- **1:N** con `Patient` (patients_diagnoses)
- **1:N** con `Diagnosis` (patients_diagnoses)
- **1:N** con `Treatment` (patients_diagnoses)
- **1:N** con `Appointment` (appointments_status)
- **1:N** con `MedicalHistory` (patients_diagnoses)

#### **👤 TABLA: `architect_userprofile`**
```sql
CREATE TABLE architect_userprofile (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    user_id INTEGER UNIQUE NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    phone VARCHAR(20),
    address TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES auth_user(id) ON DELETE CASCADE
);
```

**🔗 RELACIONES:**
- **N:1** con `auth_user` (architect)
- **1:1** con `Therapist` (therapists)
- **1:1** con `Patient` (patients_diagnoses)

#### **🔒 TABLA: `architect_permission`**
```sql
CREATE TABLE architect_permission (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    codename VARCHAR(100) NOT NULL,
    content_type_id INTEGER NOT NULL,
    FOREIGN KEY (content_type_id) REFERENCES django_content_type(id)
);
```

**🔗 RELACIONES:**
- **N:1** con `django_content_type` (Django)
- **N:N** con `Role` a través de `RoleHasPermission`

#### **👑 TABLA: `architect_role`**
```sql
CREATE TABLE architect_role (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) UNIQUE NOT NULL,
    description TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

**🔗 RELACIONES:**
- **N:N** con `Permission` a través de `RoleHasPermission`
- **1:N** con `User` (a través de grupos Django)

#### **🔗 TABLA: `architect_role_has_permission`**
```sql
CREATE TABLE architect_role_has_permission (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    role_id INTEGER NOT NULL,
    permission_id INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (role_id) REFERENCES architect_role(id) ON DELETE CASCADE,
    FOREIGN KEY (permission_id) REFERENCES architect_permission(id) ON DELETE CASCADE,
    UNIQUE KEY unique_role_permission (role_id, permission_id)
);
```

**🔗 RELACIONES:**
- **N:1** con `Role`
- **N:1** con `Permission`

---

## 🏥 **MÓDULO `therapists/` - GESTIÓN DE TERAPEUTAS**

#### **👨‍⚕️ TABLA: `therapists_therapist`**
```sql
CREATE TABLE therapists_therapist (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    user_id INTEGER UNIQUE NOT NULL,
    license_number VARCHAR(50) UNIQUE NOT NULL,
    experience_years INTEGER DEFAULT 0,
    is_available BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES auth_user(id) ON DELETE CASCADE
);
```

**🔗 RELACIONES:**
- **1:1** con `auth_user` (architect)
- **1:N** con `Patient` (patients_diagnoses)
- **1:N** con `Diagnosis` (patients_diagnoses)
- **1:N** con `Treatment` (patients_diagnoses)
- **1:N** con `Appointment` (appointments_status)
- **1:N** con `MedicalHistory` (patients_diagnoses)

#### **🎯 TABLA: `therapists_specialty`**
```sql
CREATE TABLE therapists_specialty (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) UNIQUE NOT NULL,
    description TEXT,
    requirements TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

**🔗 RELACIONES:**
- **1:N** con `Therapist` a través de tabla intermedia
- **1:N** con `MedicalHistoryTemplate` (histories_configurations)

#### **🔗 TABLA: `therapists_therapist_specialty` (Tabla Intermedia)**
```sql
CREATE TABLE therapists_therapist_specialty (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    therapist_id INTEGER NOT NULL,
    specialty_id INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (therapist_id) REFERENCES therapists_therapist(id) ON DELETE CASCADE,
    FOREIGN KEY (specialty_id) REFERENCES therapists_specialty(id) ON DELETE CASCADE,
    UNIQUE KEY unique_therapist_specialty (therapist_id, specialty_id)
);
```

---

## 🧑‍⚕️ **MÓDULO `patients_diagnoses/` - PACIENTES Y DIAGNÓSTICOS**

#### **👥 TABLA: `patients_diagnoses_patient`**
```sql
CREATE TABLE patients_diagnoses_patient (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    user_id INTEGER UNIQUE NOT NULL,
    birth_date DATE NOT NULL,
    gender ENUM('M', 'F', 'O') NOT NULL,
    emergency_contact VARCHAR(100),
    emergency_phone VARCHAR(20),
    blood_type ENUM('A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-'),
    allergies TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES auth_user(id) ON DELETE CASCADE
);
```

**🔗 RELACIONES:**
- **1:1** con `auth_user` (architect)
- **1:N** con `Diagnosis`
- **1:N** con `Treatment`
- **1:N** con `Appointment` (appointments_status)
- **1:N** con `MedicalHistory`

#### **🔍 TABLA: `patients_diagnoses_diagnosis`**
```sql
CREATE TABLE patients_diagnoses_diagnosis (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    patient_id INTEGER NOT NULL,
    therapist_id INTEGER NOT NULL,
    symptoms TEXT NOT NULL,
    diagnosis TEXT NOT NULL,
    treatment_plan TEXT,
    diagnosis_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (patient_id) REFERENCES patients_diagnoses_patient(id) ON DELETE CASCADE,
    FOREIGN KEY (therapist_id) REFERENCES therapists_therapist(id) ON DELETE CASCADE
);
```

**🔗 RELACIONES:**
- **N:1** con `Patient`
- **N:1** con `Therapist` (therapists)
- **1:N** con `Treatment`

#### **💊 TABLA: `patients_diagnoses_treatment`**
```sql
CREATE TABLE patients_diagnoses_treatment (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    patient_id INTEGER NOT NULL,
    therapist_id INTEGER NOT NULL,
    diagnosis_id INTEGER NOT NULL,
    treatment_type ENUM('therapy', 'medication', 'surgery', 'other') NOT NULL,
    description TEXT NOT NULL,
    duration_weeks INTEGER,
    status ENUM('active', 'completed', 'cancelled', 'paused') DEFAULT 'active',
    start_date DATE NOT NULL,
    end_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (patient_id) REFERENCES patients_diagnoses_patient(id) ON DELETE CASCADE,
    FOREIGN KEY (therapist_id) REFERENCES therapists_therapist(id) ON DELETE CASCADE,
    FOREIGN KEY (diagnosis_id) REFERENCES patients_diagnoses_diagnosis(id) ON DELETE CASCADE
);
```

**🔗 RELACIONES:**
- **N:1** con `Patient`
- **N:1** con `Therapist` (therapists)
- **N:1** con `Diagnosis`

#### **📋 TABLA: `patients_diagnoses_medicalhistory`**
```sql
CREATE TABLE patients_diagnoses_medicalhistory (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    patient_id INTEGER NOT NULL,
    therapist_id INTEGER NOT NULL,
    template_id INTEGER NOT NULL,
    fields_data JSON NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (patient_id) REFERENCES patients_diagnoses_patient(id) ON DELETE CASCADE,
    FOREIGN KEY (therapist_id) REFERENCES therapists_therapist(id) ON DELETE CASCADE,
    FOREIGN KEY (template_id) REFERENCES histories_configurations_medicalhistorytemplate(id) ON DELETE CASCADE
);
```

**🔗 RELACIONES:**
- **N:1** con `Patient`
- **N:1** con `Therapist` (therapists)
- **N:1** con `MedicalHistoryTemplate` (histories_configurations)

---

## 📅 **MÓDULO `appointments_status/` - CITAS MÉDICAS**

#### **📅 TABLA: `appointments_status_appointment`**
```sql
CREATE TABLE appointments_status_appointment (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    patient_id INTEGER NOT NULL,
    therapist_id INTEGER NOT NULL,
    date_time DATETIME NOT NULL,
    duration_minutes INTEGER DEFAULT 60,
    notes TEXT,
    status_id INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (patient_id) REFERENCES patients_diagnoses_patient(id) ON DELETE CASCADE,
    FOREIGN KEY (therapist_id) REFERENCES therapists_therapist(id) ON DELETE CASCADE,
    FOREIGN KEY (status_id) REFERENCES appointments_status_appointmentstatus(id) ON DELETE CASCADE
);
```

**🔗 RELACIONES:**
- **N:1** con `Patient` (patients_diagnoses)
- **N:1** con `Therapist` (therapists)
- **N:1** con `AppointmentStatus`
- **1:1** con `Ticket`

#### **🎫 TABLA: `appointments_status_ticket`**
```sql
CREATE TABLE appointments_status_ticket (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    appointment_id INTEGER UNIQUE NOT NULL,
    ticket_number VARCHAR(20) UNIQUE NOT NULL,
    priority ENUM('low', 'medium', 'high', 'urgent') DEFAULT 'medium',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (appointment_id) REFERENCES appointments_status_appointment(id) ON DELETE CASCADE
);
```

**🔗 RELACIONES:**
- **1:1** con `Appointment`

#### **💰 TABLA: `appointments_status_ticket_payment`**
```sql
CREATE TABLE appointments_status_ticket_payment (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    ticket_id INTEGER NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    payment_method ENUM('efectivo', 'tarjeta', 'transferencia', 'cheque', 'otro') NOT NULL,
    status ENUM('pending', 'paid', 'cancelled', 'refunded') DEFAULT 'pending',
    payment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (ticket_id) REFERENCES appointments_status_ticket(id) ON DELETE CASCADE
);
```

**🔗 RELACIONES:**
- **N:1** con `Ticket`
- **1:N** con `PaymentStatus` (histories_configurations)

#### **📊 TABLA: `appointments_status_appointmentstatus`**
```sql
CREATE TABLE appointments_status_appointmentstatus (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50) UNIQUE NOT NULL,
    description TEXT,
    color VARCHAR(7) DEFAULT '#000000',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

**🔗 RELACIONES:**
- **1:N** con `Appointment`

---

## 📋 **MÓDULO `histories_configurations/` - CONFIGURACIÓN DE HISTORIALES**

#### **📄 TABLA: `histories_configurations_medicalhistorytemplate`**
```sql
CREATE TABLE histories_configurations_medicalhistorytemplate (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    specialty_id INTEGER,
    sections JSON NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (specialty_id) REFERENCES therapists_specialty(id) ON DELETE SET NULL
);
```

**🔗 RELACIONES:**
- **N:1** con `Specialty` (therapists)
- **1:N** con `MedicalHistory` (patients_diagnoses)
- **1:N** con `MedicalHistoryField`

#### **⚙️ TABLA: `histories_configurations_medicalhistoryfield`**
```sql
CREATE TABLE histories_configurations_medicalhistoryfield (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    template_id INTEGER NOT NULL,
    name VARCHAR(100) NOT NULL,
    field_type ENUM('text', 'number', 'date', 'select', 'checkbox', 'textarea') NOT NULL,
    validation_rules JSON,
    is_required BOOLEAN DEFAULT FALSE,
    order_index INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (template_id) REFERENCES histories_configurations_medicalhistorytemplate(id) ON DELETE CASCADE
);
```

**🔗 RELACIONES:**
- **N:1** con `MedicalHistoryTemplate`

---

## 📊 **MÓDULO `company_reports/` - REPORTES EMPRESARIALES**

#### **🏢 TABLA: `company_reports_companydata`**
```sql
CREATE TABLE company_reports_companydata (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    company_name VARCHAR(200) NOT NULL,
    legal_name VARCHAR(200),
    tax_id VARCHAR(50),
    address TEXT,
    phone VARCHAR(20),
    email VARCHAR(100),
    website VARCHAR(200),
    company_logo VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

**🔗 RELACIONES:**
- **1:N** con `Report` (implícito)

#### **📈 TABLA: `company_reports_report`**
```sql
CREATE TABLE company_reports_report (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    user_id INTEGER NOT NULL,
    report_type ENUM('appointments', 'patients', 'revenue', 'custom') NOT NULL,
    parameters JSON,
    generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    file_path VARCHAR(255),
    FOREIGN KEY (user_id) REFERENCES auth_user(id) ON DELETE CASCADE
);
```

**🔗 RELACIONES:**
- **N:1** con `auth_user` (architect)

---

## 🌍 **MÓDULO `ubi_geo/` - UBICACIONES GEOGRÁFICAS**

#### **🌍 TABLA: `ubi_geo_country`**
```sql
CREATE TABLE ubi_geo_country (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    code VARCHAR(3) UNIQUE NOT NULL,
    phone_code VARCHAR(10),
    is_active BOOLEAN DEFAULT TRUE
);
```

**🔗 RELACIONES:**
- **1:N** con `Region`

#### **🏞️ TABLA: `ubi_geo_region`**
```sql
CREATE TABLE ubi_geo_region (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    country_id INTEGER NOT NULL,
    name VARCHAR(100) NOT NULL,
    code VARCHAR(10),
    is_active BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (country_id) REFERENCES ubi_geo_country(id) ON DELETE CASCADE
);
```

**🔗 RELACIONES:**
- **N:1** con `Country`
- **1:N** con `Province`

#### **🏙️ TABLA: `ubi_geo_province`**
```sql
CREATE TABLE ubi_geo_province (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    region_id INTEGER NOT NULL,
    name VARCHAR(100) NOT NULL,
    code VARCHAR(10),
    is_active BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (region_id) REFERENCES ubi_geo_region(id) ON DELETE CASCADE
);
```

**🔗 RELACIONES:**
- **N:1** con `Region`
- **1:N** con `District`

#### **🏘️ TABLA: `ubi_geo_district`**
```sql
CREATE TABLE ubi_geo_district (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    province_id INTEGER NOT NULL,
    name VARCHAR(100) NOT NULL,
    code VARCHAR(10),
    is_active BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (province_id) REFERENCES ubi_geo_province(id) ON DELETE CASCADE
);
```

**🔗 RELACIONES:**
- **N:1** con `Province`

---

## 🔄 **FLUJO DE INTERACCIÓN ENTRE MÓDULOS**

### **📊 DIAGRAMA DE FLUJO DE DATOS:**

```
1. AUTENTICACIÓN (architect)
   ↓
2. PERFIL DE USUARIO (users_profiles)
   ↓
3. ROL Y PERMISOS (architect)
   ↓
4. ESPECIALIZACIÓN (therapists)
   ↓
5. GESTIÓN DE PACIENTES (patients_diagnoses)
   ↓
6. CITAS Y TICKETS (appointments_status)
   ↓
7. HISTORIALES MÉDICOS (histories_configurations)
   ↓
8. REPORTES Y ESTADÍSTICAS (company_reports)
```

### **🔗 INTERACCIONES PRINCIPALES:**

#### **🔄 MÓDULO `architect` ↔ `users_profiles`:**
- **Relación**: 1:1 entre `auth_user` y `UserProfile`
- **Propósito**: Extender información básica del usuario
- **Flujo**: Al crear usuario → se crea perfil automáticamente

#### **🔄 MÓDULO `architect` ↔ `therapists`:**
- **Relación**: 1:1 entre `auth_user` y `Therapist`
- **Propósito**: Convertir usuario en terapeuta
- **Flujo**: Usuario con rol terapeuta → se crea registro en `therapists_therapist`

#### **🔄 MÓDULO `architect` ↔ `patients_diagnoses`:**
- **Relación**: 1:1 entre `auth_user` y `Patient`
- **Propósito**: Convertir usuario en paciente
- **Flujo**: Usuario con rol paciente → se crea registro en `patients_diagnoses_patient`

#### **🔄 MÓDULO `therapists` ↔ `patients_diagnoses`:**
- **Relación**: 1:N entre `Therapist` y `Patient`
- **Propósito**: Asignar pacientes a terapeutas
- **Flujo**: Terapeuta puede tener múltiples pacientes

#### **🔄 MÓDULO `patients_diagnoses` ↔ `appointments_status`:**
- **Relación**: 1:N entre `Patient` y `Appointment`
- **Propósito**: Programar citas para pacientes
- **Flujo**: Paciente → Cita → Ticket automático

#### **🔄 MÓDULO `histories_configurations` ↔ `patients_diagnoses`:**
- **Relación**: 1:N entre `MedicalHistoryTemplate` y `MedicalHistory`
- **Propósito**: Crear historiales médicos usando plantillas
- **Flujo**: Template → Historial con datos específicos del paciente

#### **🔄 MÓDULO `company_reports` ↔ Todos los módulos:**
- **Relación**: Agregación de datos de múltiples módulos
- **Propósito**: Generar reportes y estadísticas
- **Flujo**: Consultas a múltiples tablas → Reporte consolidado

#### **🔄 MÓDULO `company_reports` ↔ `appointments_status`:**
- **Relación**: Consulta de citas, tickets y pagos
- **Propósito**: Reportes de caja chica y tickets pagados
- **Flujo**: Filtrado por fecha → Agrupación por método de pago → Resumen consolidado

#### **🔄 MÓDULO `company_reports` ↔ `therapists`:**
- **Relación**: Información de terapeutas en reportes
- **Propósito**: Asociar pagos y tickets con terapeutas
- **Flujo**: Cita → Terapeuta → Reporte de rendimiento

---

## 🗂️ **ESTRUCTURA DE ARCHIVOS DE BASE DE DATOS**

### **📁 DIRECTORIO `db/`:**
```
db/
├── init.sql              # Script de inicialización
├── countries.csv         # Datos de países
├── regions.csv          # Datos de regiones
├── provinces.csv        # Datos de provincias
└── districts.csv        # Datos de distritos
```

### **📊 CONTENIDO DE ARCHIVOS CSV:**
- **`countries.csv`**: Lista de países con códigos ISO
- **`regions.csv`**: Regiones por país
- **`provinces.csv`**: Provincias por región
- **`districts.csv`**: Distritos por provincia

---

## 🔒 **RESTRICCIONES DE INTEGRIDAD**

### **🔑 CLAVES PRIMARIAS:**
- Todas las tablas tienen `id` como clave primaria auto-incremental
- Uso de `INTEGER` para optimización de rendimiento

### **🔗 CLAVES FORÁNEAS:**
- **CASCADE**: Eliminación en cascada para dependencias fuertes
- **SET NULL**: Para relaciones opcionales
- **UNIQUE**: Para relaciones 1:1

### **📋 RESTRICCIONES DE NEGOCIO:**
- **Usuario único**: Un usuario no puede ser terapeuta y paciente simultáneamente
- **Citas únicas**: Un paciente no puede tener citas solapadas con el mismo terapeuta
- **Historiales únicos**: Un paciente tiene un historial por template por fecha

---

## 📈 **OPTIMIZACIONES DE BASE DE DATOS**

### **🔍 ÍNDICES RECOMENDADOS:**
```sql
-- Índices para búsquedas frecuentes
CREATE INDEX idx_patient_therapist ON patients_diagnoses_patient(user_id);
CREATE INDEX idx_diagnosis_patient ON patients_diagnoses_diagnosis(patient_id);
CREATE INDEX idx_appointment_datetime ON appointments_status_appointment(date_time);
CREATE INDEX idx_appointment_patient ON appointments_status_appointment(patient_id);

-- Índices para reportes de pagos
CREATE INDEX idx_ticket_payment_status ON appointments_status_ticket_payment(status);
CREATE INDEX idx_ticket_payment_date ON appointments_status_ticket_payment(payment_date);
CREATE INDEX idx_ticket_payment_method ON appointments_status_ticket_payment(payment_method);
CREATE INDEX idx_appointment_payment ON appointments_status_appointment(payment);
CREATE INDEX idx_appointment_payment_date ON appointments_status_appointment(appointment_date);

-- Índices para relaciones geográficas
CREATE INDEX idx_region_country ON ubi_geo_region(country_id);
CREATE INDEX idx_province_region ON ubi_geo_province(region_id);
CREATE INDEX idx_district_province ON ubi_geo_district(province_id);
```

### **📊 PARTICIONAMIENTO:**
- **Por fecha**: Tablas de citas y diagnósticos
- **Por especialidad**: Tablas de terapeutas y plantillas
- **Por ubicación**: Tablas geográficas

---

## 🚀 **MIGRACIONES Y VERSIONADO**

### **📁 ESTRUCTURA DE MIGRACIONES:**
```
migrations/
├── __init__.py
├── 0001_initial.py          # Migración inicial
├── 0002_alter_*.py          # Modificaciones de campos
└── 0003_alter_*.py          # Cambios estructurales
```

### **🔄 PROCESO DE MIGRACIÓN:**
1. **Desarrollo**: Cambios en modelos
2. **Migración**: `python manage.py makemigrations`
3. **Aplicación**: `python manage.py migrate`
4. **Producción**: Migración controlada con backups

---

## ✅ **ESTADO**
**COMPLETADO** - Documentación exhaustiva de la base de datos, relaciones entre tablas e interacción de módulos.

---

*README generado para el Punto 4 de la lista de documentación*
*Proyecto: Backend-Optimizacion*
