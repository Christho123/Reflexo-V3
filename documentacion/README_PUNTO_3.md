# 🔗 PUNTO 3: DOCUMENTACIÓN DE TODOS LOS ENDPOINTS QUE MANEJA EL BACKEND

## 🔗 **NAVEGACIÓN RÁPIDA**

### **📚 DOCUMENTACIÓN PRINCIPAL**
- [🏠 **Volver al índice principal**](README.md)
- [🏗️ **PUNTO 1**: Estructura y módulos](README_PUNTO_1.md)
- [🔗 **PUNTO 2**: Conexiones entre módulos](README_PUNTO_2.md)
- [🗄️ **PUNTO 4**: Estructura de base de datos](README_PUNTO_4.md)

### **📊 REPORTES ESPECIALIZADOS**
- [🏗️ **REPORTE**: Análisis de estructura del código](REPORTE_ESTRUCTURA_CODIGO.md)
- [🔄 **REPORTE**: Flujo de interacción del usuario](REPORTE_FLUJO_USUARIO.md)

### **🔗 NAVEGACIÓN INTERNA**
- [🔐 Endpoints de autenticación](#endpoints-de-autenticación)
- [👥 Endpoints de gestión de usuarios](#endpoints-de-gestión-de-usuarios)
- [🏥 Endpoints de gestión de citas](#endpoints-de-gestión-de-citas)
- [👨‍⚕️ Endpoints de gestión de terapeutas](#endpoints-de-gestión-de-terapeutas)
- [📊 Endpoints de reportes](#endpoints-de-reportes)
- [📤 Endpoints de exportación](#endpoints-de-exportación)
- [🗄️ Endpoints de gestión de base de datos](#endpoints-de-gestión-de-base-de-datos)

---

## 🎯 **OBJETIVO**
Documentar exhaustivamente todos los endpoints de la API REST que maneja el backend del proyecto Backend-Optimizacion, incluyendo métodos HTTP, parámetros, respuestas, permisos y sistema de autenticación.

## 📊 **ESTADÍSTICAS GENERALES DE LA API**

- **Total de endpoints**: ~40 endpoints
- **Módulos con API**: 8 módulos principales
- **Métodos HTTP**: GET, POST, PUT, PATCH, DELETE
- **Autenticación**: JWT (JSON Web Tokens)
- **Formato de respuesta**: JSON
- **Versionado**: API v1 (implícito)

---

## 🔐 **ENDPOINTS DE AUTENTICACIÓN Y PERMISOS**

### **📁 MÓDULO `architect/`**

#### **🔑 AUTENTICACIÓN JWT**
```
POST /api/auth/login/
├── Descripción: Inicio de sesión de usuario
├── Parámetros: username, password
├── Respuesta: access_token, refresh_token, user_data
└── Permisos: Público

POST /api/auth/refresh/
├── Descripción: Renovar token de acceso
├── Parámetros: refresh_token
├── Respuesta: access_token
└── Permisos: Usuario autenticado

POST /api/auth/logout/
├── Descripción: Cerrar sesión
├── Parámetros: refresh_token
├── Respuesta: success_message
└── Permisos: Usuario autenticado

POST /api/auth/register/
├── Descripción: Registro de nuevo usuario
├── Parámetros: username, email, password, confirm_password
├── Respuesta: user_data, success_message
└── Permisos: Público
```

#### **👥 GESTIÓN DE USUARIOS**
```
GET /api/users/
├── Descripción: Listar todos los usuarios
├── Parámetros: page, page_size, search, role
├── Respuesta: Lista paginada de usuarios
└── Permisos: Administradores

GET /api/users/{id}/
├── Descripción: Obtener usuario específico
├── Parámetros: id (path)
├── Respuesta: Datos del usuario
└── Permisos: Propio usuario o administradores

POST /api/users/
├── Descripción: Crear nuevo usuario
├── Parámetros: username, email, password, role, profile_data
├── Respuesta: Usuario creado
└── Permisos: Administradores

PUT /api/users/{id}/
├── Descripción: Actualizar usuario completo
├── Parámetros: id (path), user_data
├── Respuesta: Usuario actualizado
└── Permisos: Propio usuario o administradores

PATCH /api/users/{id}/
├── Descripción: Actualizar usuario parcialmente
├── Parámetros: id (path), partial_user_data
├── Respuesta: Usuario actualizado
└── Permisos: Propio usuario o administradores

DELETE /api/users/{id}/
├── Descripción: Eliminar usuario
├── Parámetros: id (path)
├── Respuesta: success_message
└── Permisos: Administradores
```

#### **🔒 GESTIÓN DE PERMISOS**
```
GET /api/permissions/
├── Descripción: Listar todos los permisos del sistema
├── Parámetros: page, page_size, module
├── Respuesta: Lista paginada de permisos
└── Permisos: Administradores

GET /api/permissions/{id}/
├── Descripción: Obtener permiso específico
├── Parámetros: id (path)
├── Respuesta: Datos del permiso
└── Permisos: Administradores

POST /api/permissions/
├── Descripción: Crear nuevo permiso
├── Parámetros: name, codename, content_type
├── Respuesta: Permiso creado
└── Permisos: Administradores

PUT /api/permissions/{id}/
├── Descripción: Actualizar permiso
├── Parámetros: id (path), permission_data
├── Respuesta: Permiso actualizado
└── Permisos: Administradores

DELETE /api/permissions/{id}/
├── Descripción: Eliminar permiso
├── Parámetros: id (path)
├── Respuesta: success_message
└── Permisos: Administradores
```

#### **👑 GESTIÓN DE ROLES**
```
GET /api/roles/
├── Descripción: Listar todos los roles del sistema
├── Parámetros: page, page_size, name
├── Respuesta: Lista paginada de roles
└── Permisos: Administradores

GET /api/roles/{id}/
├── Descripción: Obtener rol específico
├── Parámetros: id (path)
├── Respuesta: Datos del rol con permisos
└── Permisos: Administradores

POST /api/roles/
├── Descripción: Crear nuevo rol
├── Parámetros: name, description, permissions
├── Respuesta: Rol creado
└── Permisos: Administradores

PUT /api/roles/{id}/
├── Descripción: Actualizar rol
├── Parámetros: id (path), role_data
├── Respuesta: Rol actualizado
└── Permisos: Administradores

DELETE /api/roles/{id}/
├── Descripción: Eliminar rol
├── Parámetros: id (path)
├── Respuesta: success_message
└── Permisos: Administradores
```

---

## 👤 **ENDPOINTS DE PERFILES DE USUARIO**

### **📁 MÓDULO `users_profiles/`**

#### **👤 PERFILES DE USUARIO**
```
GET /api/users/profiles/
├── Descripción: Listar perfiles de usuario
├── Parámetros: page, page_size, user, role
├── Respuesta: Lista paginada de perfiles
└── Permisos: Administradores

GET /api/users/profiles/{id}/
├── Descripción: Obtener perfil específico
├── Parámetros: id (path)
├── Respuesta: Datos del perfil
└── Permisos: Propio perfil o administradores

POST /api/users/profiles/
├── Descripción: Crear nuevo perfil
├── Parámetros: user, first_name, last_name, phone, address
├── Respuesta: Perfil creado
└── Permisos: Administradores

PUT /api/users/profiles/{id}/
├── Descripción: Actualizar perfil completo
├── Parámetros: id (path), profile_data
├── Respuesta: Perfil actualizado
└── Permisos: Propio perfil o administradores

PATCH /api/users/profiles/{id}/
├── Descripción: Actualizar perfil parcialmente
├── Parámetros: id (path), partial_profile_data
├── Respuesta: Perfil actualizado
└── Permisos: Propio perfil o administradores

DELETE /api/users/profiles/{id}/
├── Descripción: Eliminar perfil
├── Parámetros: id (path)
├── Respuesta: success_message
└── Permisos: Administradores
```

---

## 🏥 **ENDPOINTS DE TERAPEUTAS**

### **📁 MÓDULO `therapists/`**

#### **👨‍⚕️ TERAPEUTAS**
```
GET /api/therapists/
├── Descripción: Listar todos los terapeutas
├── Parámetros: page, page_size, specialty, location, available
├── Respuesta: Lista paginada de terapeutas
└── Permisos: Usuarios autenticados

GET /api/therapists/{id}/
├── Descripción: Obtener terapeuta específico
├── Parámetros: id (path)
├── Respuesta: Datos del terapeuta con especialidades
└── Permisos: Usuarios autenticados

POST /api/therapists/
├── Descripción: Crear nuevo terapeuta
├── Parámetros: user, specialty, license_number, experience_years
├── Respuesta: Terapeuta creado
└── Permisos: Administradores

PUT /api/therapists/{id}/
├── Descripción: Actualizar terapeuta
├── Parámetros: id (path), therapist_data
├── Respuesta: Terapeuta actualizado
└── Permisos: Propio terapeuta o administradores

DELETE /api/therapists/{id}/
├── Descripción: Eliminar terapeuta
├── Parámetros: id (path)
├── Respuesta: success_message
└── Permisos: Administradores
```

#### **🎯 ESPECIALIDADES MÉDICAS**
```
GET /api/therapists/specialties/
├── Descripción: Listar todas las especialidades
├── Parámetros: page, page_size, name
├── Respuesta: Lista paginada de especialidades
└── Permisos: Usuarios autenticados

GET /api/therapists/specialties/{id}/
├── Descripción: Obtener especialidad específica
├── Parámetros: id (path)
├── Respuesta: Datos de la especialidad
└── Permisos: Usuarios autenticados

POST /api/therapists/specialties/
├── Descripción: Crear nueva especialidad
├── Parámetros: name, description, requirements
├── Respuesta: Especialidad creada
└── Permisos: Administradores

PUT /api/therapists/specialties/{id}/
├── Descripción: Actualizar especialidad
├── Parámetros: id (path), specialty_data
├── Respuesta: Especialidad actualizada
└── Permisos: Administradores

DELETE /api/therapists/specialties/{id}/
├── Descripción: Eliminar especialidad
├── Parámetros: id (path)
├── Respuesta: success_message
└── Permisos: Administradores
```

---

## 🧑‍⚕️ **ENDPOINTS DE PACIENTES Y DIAGNÓSTICOS**

### **📁 MÓDULO `patients_diagnoses/`**

#### **👥 PACIENTES**
```
GET /api/patients/
├── Descripción: Listar todos los pacientes
├── Parámetros: page, page_size, name, location, therapist
├── Respuesta: Lista paginada de pacientes
└── Permisos: Terapeutas y administradores

GET /api/patients/{id}/
├── Descripción: Obtener paciente específico
├── Parámetros: id (path)
├── Respuesta: Datos del paciente con historial
└── Permisos: Propio paciente, terapeutas asignados o administradores

POST /api/patients/
├── Descripción: Crear nuevo paciente
├── Parámetros: user, birth_date, gender, emergency_contact
├── Respuesta: Paciente creado
└── Permisos: Terapeutas y administradores

PUT /api/patients/{id}/
├── Descripción: Actualizar paciente
├── Parámetros: id (path), patient_data
├── Respuesta: Paciente actualizado
└── Permisos: Propio paciente, terapeutas asignados o administradores

DELETE /api/patients/{id}/
├── Descripción: Eliminar paciente
├── Parámetros: id (path)
├── Respuesta: success_message
└── Permisos: Administradores
```

#### **🔍 DIAGNÓSTICOS**
```
GET /api/patients/diagnoses/
├── Descripción: Listar todos los diagnósticos
├── Parámetros: page, page_size, patient, therapist, date_from, date_to
├── Respuesta: Lista paginada de diagnósticos
└── Permisos: Terapeutas y administradores

GET /api/patients/diagnoses/{id}/
├── Descripción: Obtener diagnóstico específico
├── Parámetros: id (path)
├── Respuesta: Datos del diagnóstico
└── Permisos: Propio diagnóstico, terapeutas asignados o administradores

POST /api/patients/diagnoses/
├── Descripción: Crear nuevo diagnóstico
├── Parámetros: patient, therapist, symptoms, diagnosis, treatment_plan
├── Respuesta: Diagnóstico creado
└── Permisos: Terapeutas

PUT /api/patients/diagnoses/{id}/
├── Descripción: Actualizar diagnóstico
├── Parámetros: id (path), diagnosis_data
├── Respuesta: Diagnóstico actualizado
└── Permisos: Propio diagnóstico o administradores

DELETE /api/patients/diagnoses/{id}/
├── Descripción: Eliminar diagnóstico
├── Parámetros: id (path)
├── Respuesta: success_message
└── Permisos: Administradores
```

#### **📋 HISTORIAL MÉDICO**
```
GET /api/patients/medical-histories/
├── Descripción: Listar historiales médicos
├── Parámetros: page, page_size, patient, therapist
├── Respuesta: Lista paginada de historiales
└── Permisos: Terapeutas y administradores

GET /api/patients/medical-histories/{id}/
├── Descripción: Obtener historial médico específico
├── Parámetros: id (path)
├── Respuesta: Datos del historial médico
└── Permisos: Propio historial, terapeutas asignados o administradores

POST /api/patients/medical-histories/
├── Descripción: Crear nuevo historial médico
├── Parámetros: patient, therapist, template, fields_data
├── Respuesta: Historial médico creado
└── Permisos: Terapeutas

PUT /api/patients/medical-histories/{id}/
├── Descripción: Actualizar historial médico
├── Parámetros: id (path), history_data
├── Respuesta: Historial médico actualizado
└── Permisos: Propio historial o administradores

DELETE /api/patients/medical-histories/{id}/
├── Descripción: Eliminar historial médico
├── Parámetros: id (path)
├── Respuesta: success_message
└── Permisos: Administradores
```

#### **💊 TRATAMIENTOS**
```
GET /api/patients/treatments/
├── Descripción: Listar todos los tratamientos
├── Parámetros: page, page_size, patient, therapist, status
├── Respuesta: Lista paginada de tratamientos
└── Permisos: Terapeutas y administradores

GET /api/patients/treatments/{id}/
├── Descripción: Obtener tratamiento específico
├── Parámetros: id (path)
├── Respuesta: Datos del tratamiento
└── Permisos: Propio tratamiento, terapeutas asignados o administradores

POST /api/patients/treatments/
├── Descripción: Crear nuevo tratamiento
├── Parámetros: patient, therapist, diagnosis, treatment_type, duration
├── Respuesta: Tratamiento creado
└── Permisos: Terapeutas

PUT /api/patients/treatments/{id}/
├── Descripción: Actualizar tratamiento
├── Parámetros: id (path), treatment_data
├── Respuesta: Tratamiento actualizado
└── Permisos: Propio tratamiento o administradores

DELETE /api/patients/treatments/{id}/
├── Descripción: Eliminar tratamiento
├── Parámetros: id (path)
├── Respuesta: success_message
└── Permisos: Administradores
```

---

## 📅 **ENDPOINTS DE CITAS MÉDICAS**

### **📁 MÓDULO `appointments_status/`**

#### **📅 CITAS MÉDICAS**
```
GET /api/appointments/
├── Descripción: Listar todas las citas
├── Parámetros: page, page_size, patient, therapist, status, date_from, date_to
├── Respuesta: Lista paginada de citas
└── Permisos: Usuarios autenticados (filtrado por rol)

GET /api/appointments/{id}/
├── Descripción: Obtener cita específica
├── Parámetros: id (path)
├── Respuesta: Datos de la cita con ticket
└── Permisos: Propia cita, terapeutas asignados o administradores

POST /api/appointments/
├── Descripción: Crear nueva cita
├── Parámetros: patient, therapist, date_time, duration, notes
├── Respuesta: Cita creada con ticket automático
└── Permisos: Terapeutas y asistentes

PUT /api/appointments/{id}/
├── Descripción: Actualizar cita
├── Parámetros: id (path), appointment_data
├── Respuesta: Cita actualizada
└── Permisos: Propia cita o administradores

DELETE /api/appointments/{id}/
├── Descripción: Cancelar/eliminar cita
├── Parámetros: id (path)
├── Respuesta: success_message
└── Permisos: Propia cita o administradores
```

#### **🎫 TICKETS DE CITAS**
```
GET /api/appointments/tickets/
├── Descripción: Listar todos los tickets
├── Parámetros: page, page_size, appointment, status, date_from, date_to
├── Respuesta: Lista paginada de tickets
└── Permisos: Usuarios autenticados (filtrado por rol)

GET /api/appointments/tickets/{id}/
├── Descripción: Obtener ticket específico
├── Parámetros: id (path)
├── Respuesta: Datos del ticket
└── Permisos: Propio ticket o administradores

POST /api/appointments/tickets/
├── Descripción: Crear ticket manualmente
├── Parámetros: appointment, ticket_number, priority
├── Respuesta: Ticket creado
└── Permisos: Asistentes y administradores

PUT /api/appointments/tickets/{id}/
├── Descripción: Actualizar ticket
├── Parámetros: id (path), ticket_data
├── Respuesta: Ticket actualizado
└── Permisos: Propio ticket o administradores

DELETE /api/appointments/tickets/{id}/
├── Descripción: Eliminar ticket
├── Parámetros: id (path)
├── Respuesta: success_message
└── Permisos: Administradores
```

#### **📊 ESTADOS DE CITAS**
```
GET /api/appointments/statuses/
├── Descripción: Listar todos los estados de citas
├── Parámetros: page, page_size, name
├── Respuesta: Lista paginada de estados
└── Permisos: Usuarios autenticados

GET /api/appointments/statuses/{id}/
├── Descripción: Obtener estado específico
├── Parámetros: id (path)
├── Respuesta: Datos del estado
└── Permisos: Usuarios autenticados

POST /api/appointments/statuses/
├── Descripción: Crear nuevo estado
├── Parámetros: name, description, color, is_active
├── Respuesta: Estado creado
└── Permisos: Administradores

PUT /api/appointments/statuses/{id}/
├── Descripción: Actualizar estado
├── Parámetros: id (path), status_data
├── Respuesta: Estado actualizado
└── Permisos: Administradores

DELETE /api/appointments/statuses/{id}/
├── Descripción: Eliminar estado
├── Parámetros: id (path)
├── Respuesta: success_message
└── Permisos: Administradores
```

---

## 📋 **ENDPOINTS DE CONFIGURACIÓN DE HISTORIALES**

### **📁 MÓDULO `histories_configurations/`**

#### **📄 PLANTILLAS DE HISTORIAL**
```
GET /api/histories/templates/
├── Descripción: Listar plantillas de historial
├── Parámetros: page, page_size, name, specialty, is_active
├── Respuesta: Lista paginada de plantillas
└── Permisos: Terapeutas y administradores

GET /api/histories/templates/{id}/
├── Descripción: Obtener plantilla específica
├── Parámetros: id (path)
├── Respuesta: Datos de la plantilla con campos
└── Permisos: Terapeutas y administradores

POST /api/histories/templates/
├── Descripción: Crear nueva plantilla
├── Parámetros: name, description, specialty, sections
├── Respuesta: Plantilla creada
└── Permisos: Administradores

PUT /api/histories/templates/{id}/
├── Descripción: Actualizar plantilla
├── Parámetros: id (path), template_data
├── Respuesta: Plantilla actualizada
└── Permisos: Administradores

DELETE /api/histories/templates/{id}/
├── Descripción: Eliminar plantilla
├── Parámetros: id (path)
├── Respuesta: success_message
└── Permisos: Administradores
```

#### **⚙️ CONFIGURACIÓN DE CAMPOS**
```
GET /api/histories/fields/
├── Descripción: Listar configuración de campos
├── Parámetros: page, page_size, template, field_type
├── Respuesta: Lista paginada de campos
└── Permisos: Terapeutas y administradores

GET /api/histories/fields/{id}/
├── Descripción: Obtener campo específico
├── Parámetros: id (path)
├── Respuesta: Datos del campo
└── Permisos: Terapeutas y administradores

POST /api/histories/fields/
├── Descripción: Crear nuevo campo
├── Parámetros: template, name, field_type, validation_rules
├── Respuesta: Campo creado
└── Permisos: Administradores

PUT /api/histories/fields/{id}/
├── Descripción: Actualizar campo
├── Parámetros: id (path), field_data
├── Respuesta: Campo actualizado
└── Permisos: Administradores

DELETE /api/histories/fields/{id}/
├── Descripción: Eliminar campo
├── Parámetros: id (path)
├── Respuesta: success_message
└── Permisos: Administradores
```

---

## 📊 **ENDPOINTS DE REPORTES EMPRESARIALES**

### **📁 MÓDULO `company_reports/`**

#### **🏢 EMPRESA**
```
GET /api/reports/company/
├── Descripción: Obtener información de la empresa
├── Parámetros: Ninguno
├── Respuesta: Datos de la empresa
└── Permisos: Usuarios autenticados

PUT /api/reports/company/
├── Descripción: Actualizar información de la empresa
├── Parámetros: company_data
├── Respuesta: Empresa actualizada
└── Permisos: Administradores
```

#### **📈 REPORTES**
```
GET /api/reports/
├── Descripción: Listar reportes disponibles
├── Parámetros: page, page_size, type, date_from, date_to
├── Respuesta: Lista paginada de reportes
└── Permisos: Usuarios autenticados (filtrado por rol)

GET /api/reports/{id}/
├── Descripción: Obtener reporte específico
├── Parámetros: id (path)
├── Respuesta: Datos del reporte
└── Permisos: Propio reporte o administradores

POST /api/reports/
├── Descripción: Generar nuevo reporte
├── Parámetros: type, parameters, date_range
├── Respuesta: Reporte generado
└── Permisos: Usuarios autorizados

DELETE /api/reports/{id}/
├── Descripción: Eliminar reporte
├── Parámetros: id (path)
├── Respuesta: success_message
└── Permisos: Propio reporte o administradores

GET /api/reports/improved-daily-cash/
├── Descripción: Reporte mejorado de caja chica diaria
├── Parámetros: date (YYYY-MM-DD)
├── Respuesta: Pagos detallados con resumen por método
└── Permisos: Usuarios autenticados

GET /api/reports/daily-paid-tickets/
├── Descripción: Reporte diario de tickets pagados
├── Parámetros: date (YYYY-MM-DD)
├── Respuesta: Tickets pagados con información completa
└── Permisos: Usuarios autenticados
```

#### **📊 ESTADÍSTICAS**
```
GET /api/reports/statistics/
├── Descripción: Obtener estadísticas generales
├── Parámetros: date_from, date_to, group_by
├── Respuesta: Estadísticas agregadas
└── Permisos: Usuarios autenticados (filtrado por rol)

GET /api/reports/statistics/appointments/
├── Descripción: Estadísticas de citas
├── Parámetros: date_from, date_to, therapist, specialty
├── Respuesta: Estadísticas de citas
└── Permisos: Terapeutas y administradores

GET /api/reports/statistics/patients/
├── Descripción: Estadísticas de pacientes
├── Parámetros: date_from, date_to, location, age_group
├── Respuesta: Estadísticas de pacientes
└── Permisos: Administradores

GET /api/reports/statistics/revenue/
├── Descripción: Estadísticas de ingresos
├── Parámetros: date_from, date_to, therapist, service
├── Respuesta: Estadísticas de ingresos
└── Permisos: Administradores
```

#### **📱 DASHBOARD**
```
GET /api/reports/dashboard/
├── Descripción: Obtener datos del dashboard
├── Parámetros: date_range, widgets
├── Respuesta: Datos del dashboard
└── Permisos: Usuarios autenticados (filtrado por rol)

GET /api/reports/dashboard/widgets/
├── Descripción: Listar widgets disponibles
├── Parámetros: Ninguno
├── Respuesta: Lista de widgets
└── Permisos: Usuarios autenticados
```

#### **📄 EXPORTACIÓN PDF**
```
GET /api/exports/pdf/citas-terapeuta/
├── Descripción: Exportar PDF de citas por terapeuta
├── Parámetros: date (YYYY-MM-DD)
├── Respuesta: Archivo PDF
└── Permisos: Usuarios autenticados

GET /api/exports/pdf/pacientes-terapeuta/
├── Descripción: Exportar PDF de pacientes por terapeuta
├── Parámetros: date (YYYY-MM-DD)
├── Respuesta: Archivo PDF
└── Permisos: Usuarios autenticados

GET /api/exports/pdf/resumen-caja/
├── Descripción: Exportar PDF de resumen de caja
├── Parámetros: date (YYYY-MM-DD)
├── Respuesta: Archivo PDF
└── Permisos: Usuarios autenticados

GET /api/exports/pdf/caja-chica-mejorada/
├── Descripción: Exportar PDF de caja chica mejorada
├── Parámetros: date (YYYY-MM-DD)
├── Respuesta: Archivo PDF
└── Permisos: Usuarios autenticados

GET /api/exports/pdf/tickets-pagados/
├── Descripción: Exportar PDF de tickets pagados
├── Parámetros: date (YYYY-MM-DD)
├── Respuesta: Archivo PDF
└── Permisos: Usuarios autenticados
```

#### **📊 EXPORTACIÓN EXCEL**
```
GET /api/exports/excel/citas-rango/
├── Descripción: Exportar Excel de citas entre fechas
├── Parámetros: start_date, end_date (YYYY-MM-DD)
├── Respuesta: Archivo Excel
└── Permisos: Usuarios autenticados

GET /api/exports/excel/caja-chica-mejorada/
├── Descripción: Exportar Excel de caja chica mejorada
├── Parámetros: date (YYYY-MM-DD)
├── Respuesta: Archivo Excel
└── Permisos: Usuarios autenticados

GET /api/exports/excel/tickets-pagados/
├── Descripción: Exportar Excel de tickets pagados
├── Parámetros: date (YYYY-MM-DD)
├── Respuesta: Archivo Excel
└── Permisos: Usuarios autenticados
```

---

## 🌍 **ENDPOINTS DE UBICACIONES GEOGRÁFICAS**

### **📁 MÓDULO `ubi_geo/`**

#### **🌍 PAÍSES**
```
GET /api/geo/countries/
├── Descripción: Listar todos los países
├── Parámetros: page, page_size, name, code
├── Respuesta: Lista paginada de países
└── Permisos: Usuarios autenticados

GET /api/geo/countries/{id}/
├── Descripción: Obtener país específico
├── Parámetros: id (path)
├── Respuesta: Datos del país
└── Permisos: Usuarios autenticados
```

#### **🏞️ REGIONES**
```
GET /api/geo/regions/
├── Descripción: Listar regiones por país
├── Parámetros: page, page_size, country, name
├── Respuesta: Lista paginada de regiones
└── Permisos: Usuarios autenticados

GET /api/geo/regions/{id}/
├── Descripción: Obtener región específica
├── Parámetros: id (path)
├── Respuesta: Datos de la región
└── Permisos: Usuarios autenticados
```

#### **🏙️ PROVINCIAS**
```
GET /api/geo/provinces/
├── Descripción: Listar provincias por región
├── Parámetros: page, page_size, region, name
├── Respuesta: Lista paginada de provincias
└── Permisos: Usuarios autenticados

GET /api/geo/provinces/{id}/
├── Descripción: Obtener provincia específica
├── Parámetros: id (path)
├── Respuesta: Datos de la provincia
└── Permisos: Usuarios autenticados
```

#### **🏘️ DISTRITOS**
```
GET /api/geo/districts/
├── Descripción: Listar distritos por provincia
├── Parámetros: page, page_size, province, name
├── Respuesta: Lista paginada de distritos
└── Permisos: Usuarios autenticados

GET /api/geo/districts/{id}/
├── Descripción: Obtener distrito específico
├── Parámetros: id (path)
├── Respuesta: Datos del distrito
└── Permisos: Usuarios autenticados
```

---

## 🔧 **ENDPOINTS DE ADMINISTRACIÓN DJANGO**

### **📁 ADMIN DJANGO**
```
GET /admin/
├── Descripción: Panel de administración de Django
├── Parámetros: Ninguno
├── Respuesta: Interfaz web de administración
└── Permisos: Superusuarios

POST /admin/login/
├── Descripción: Login del panel de administración
├── Parámetros: username, password
├── Respuesta: Redirección al admin
└── Permisos: Superusuarios
```

---

## 📋 **RESUMEN DE ENDPOINTS POR MÓDULO**

### **📊 ESTADÍSTICAS DETALLADAS:**
- **`architect/`**: 15 endpoints (Autenticación, usuarios, permisos, roles)
- **`users_profiles/`**: 6 endpoints (Perfiles de usuario)
- **`therapists/`**: 10 endpoints (Terapeutas y especialidades)
- **`patients_diagnoses/`**: 20 endpoints (Pacientes, diagnósticos, historiales, tratamientos)
- **`appointments_status/`**: 15 endpoints (Citas, tickets, estados)
- **`histories_configurations/`**: 10 endpoints (Plantillas y campos)
- **`company_reports/`**: 18 endpoints (Reportes, estadísticas, dashboard, exportaciones)
- **`ubi_geo/`**: 8 endpoints (Ubicaciones geográficas)
- **`admin/`**: 2 endpoints (Panel de administración)

### **🔢 TOTAL: 104 ENDPOINTS**

---

## 🔒 **SISTEMA DE PERMISOS POR ENDPOINT**

### **📊 NIVELES DE ACCESO:**
1. **PÚBLICO**: Solo endpoints de autenticación
2. **USUARIO AUTENTICADO**: Endpoints básicos del sistema
3. **TERAPEUTA**: Endpoints de pacientes y citas asignadas
4. **ASISTENTE**: Endpoints de citas y tickets
5. **ADMINISTRADOR**: Acceso total a todos los endpoints
6. **SUPERUSUARIO**: Acceso al panel de administración de Django

---

## 📡 **FORMATOS DE RESPUESTA**

### **✅ RESPUESTA EXITOSA:**
```json
{
    "success": true,
    "data": {...},
    "message": "Operación exitosa",
    "timestamp": "2025-01-27T10:30:00Z"
}
```

### **❌ RESPUESTA DE ERROR:**
```json
{
    "success": false,
    "error": {
        "code": "ERROR_CODE",
        "message": "Descripción del error",
        "details": {...}
    },
    "timestamp": "2025-01-27T10:30:00Z"
}
```

### **📄 RESPUESTA PAGINADA:**
```json
{
    "success": true,
    "data": {
        "results": [...],
        "count": 100,
        "next": "http://api.example.com/endpoint/?page=2",
        "previous": null,
        "page": 1,
        "page_size": 20
    }
}
```

---

## ✅ **ESTADO**
**COMPLETADO** - Documentación exhaustiva de todos los endpoints del backend.

---

*README generado para el Punto 3 de la lista de documentación*
*Proyecto: Backend-Optimizacion*
