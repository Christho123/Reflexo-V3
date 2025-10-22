# API Completa - Company Reports

## Descripción General

La API de Company Reports proporciona métricas, análisis y reportes de las citas médicas, **excluyendo automáticamente los domingos** de todos los cálculos. Las estadísticas se basan únicamente en días laborales (Lunes a Sábado).

## 📊 Endpoints de Estadísticas

### 1. Obtener Estadísticas Completas

**Endpoint:** `GET /reports/statistics/`

**Parámetros de consulta:**
- `start` (requerido): Fecha de inicio en formato `YYYY-MM-DD`
- `end` (requerido): Fecha de fin en formato `YYYY-MM-DD`

**Ejemplo de solicitud:**
```
GET /reports/statistics/?start=2024-01-01&end=2024-01-07
```

**Respuesta exitosa (200):**
```json
{
    "terapeutas": [
        {
            "id": 1,
            "terapeuta": "Juan Pérez",
            "sesiones": 15,
            "ingresos": 1500.0,
            "raiting": 4.5
        }
    ],
    "tipos_pago": {
        "Efectivo": 10,
        "Tarjeta": 5
    },
    "metricas": {
        "ttlpacientes": 20,
        "ttlsesiones": 15,
        "ttlganancias": 1500.0
    },
    "ingresos": {
        "Lunes": 300.0,
        "Martes": 250.0,
        "Miercoles": 400.0,
        "Jueves": 350.0,
        "Viernes": 200.0,
        "Sabado": 0.0
    },
    "sesiones": {
        "Lunes": 3,
        "Martes": 2,
        "Miercoles": 4,
        "Jueves": 3,
        "Viernes": 2,
        "Sabado": 1
    },
    "tipos_pacientes": {
        "c": 12,
        "cc": 3
    }
}
```

### 2. Obtener Estadísticas (ViewSet)

**Endpoint:** `GET /statistics/metricas/`

**Parámetros:** Igual que el endpoint anterior.

## 📋 Endpoints de Reportes

### 3. Citas por Terapeuta

**Endpoint:** `GET /reports/appointments-per-therapist/`

**Parámetros:**
- `date` (requerido): Fecha en formato `YYYY-MM-DD`

**Ejemplo:**
```
GET /reports/appointments-per-therapist/?date=2024-01-15
```

**Respuesta:**
```json
{
    "date": "2024-01-15",
    "therapists_appointments": [
        {
            "id": 1,
            "name": "Juan Pérez",
            "appointments_count": 5,
            "percentage": 50.0
        }
    ],
    "total_appointments_count": 10
}
```

### 4. Pacientes por Terapeuta

**Endpoint:** `GET /reports/patients-by-therapist/`

**Parámetros:**
- `date` (requerido): Fecha en formato `YYYY-MM-DD`

**Ejemplo:**
```
GET /reports/patients-by-therapist/?date=2024-01-15
```

**Respuesta:**
```json
{
    "date": "2024-01-15",
    "therapists_patients": [
        {
            "id": 1,
            "name": "Juan Pérez",
            "patients_count": 3,
            "percentage": 60.0
        }
    ],
    "total_patients_count": 5
}
```

### 5. Caja Diaria

**Endpoint:** `GET /reports/daily-cash/`

**Parámetros:**
- `date` (requerido): Fecha en formato `YYYY-MM-DD`

**Ejemplo:**
```
GET /reports/daily-cash/?date=2024-01-15
```

**Respuesta:**
```json
{
    "date": "2024-01-15",
    "daily_cash": [
        {
            "payment_type": "Efectivo",
            "total_amount": 500.0,
            "count": 5
        }
    ],
    "total_daily_amount": 500.0
}
```

### 6. Caja Diaria Mejorada

**Endpoint:** `GET /reports/improved-daily-cash/`

**Parámetros:**
- `date` (requerido): Fecha en formato `YYYY-MM-DD`

**Ejemplo:**
```
GET /reports/improved-daily-cash/?date=2024-01-15
```

**Respuesta:**
```json
{
    "date": "2024-01-15",
    "improved_daily_cash": [
        {
            "payment_type": "Efectivo",
            "total_amount": 500.0,
            "count": 5,
            "percentage": 100.0
        }
    ],
    "total_daily_amount": 500.0
}
```

### 7. Tickets Pagados Diarios

**Endpoint:** `GET /reports/daily-paid-tickets/`

**Parámetros:**
- `date` (requerido): Fecha en formato `YYYY-MM-DD`

**Ejemplo:**
```
GET /reports/daily-paid-tickets/?date=2024-01-15
```

**Respuesta:**
```json
{
    "date": "2024-01-15",
    "daily_paid_tickets": [
        {
            "ticket_number": "T001",
            "amount": 100.0,
            "payment_type": "Efectivo",
            "appointment_date": "2024-01-15"
        }
    ],
    "total_amount": 100.0,
    "total_count": 1
}
```

### 8. Citas entre Fechas

**Endpoint:** `GET /reports/appointments-between-dates/`

**Parámetros:**
- `start` (requerido): Fecha de inicio en formato `YYYY-MM-DD`
- `end` (requerido): Fecha de fin en formato `YYYY-MM-DD`

**Ejemplo:**
```
GET /reports/appointments-between-dates/?start=2024-01-01&end=2024-01-31
```

**Respuesta:**
```json
{
    "start_date": "2024-01-01",
    "end_date": "2024-01-31",
    "appointments": [
        {
            "id": 1,
            "appointment_date": "2024-01-15",
            "patient_name": "María García",
            "therapist_name": "Juan Pérez",
            "payment": 100.0,
            "payment_type": "Efectivo"
        }
    ],
    "total_appointments": 1,
    "total_amount": 100.0
}
```

## 📄 Endpoints de Exportación PDF

### 9. PDF - Citas por Terapeuta

**Endpoint:** `GET /exports/pdf/citas-terapeuta/`

**Parámetros:**
- `date` (requerido): Fecha en formato `YYYY-MM-DD`

**Respuesta:** Archivo PDF descargable

### 10. PDF - Pacientes por Terapeuta

**Endpoint:** `GET /exports/pdf/pacientes-terapeuta/`

**Parámetros:**
- `date` (requerido): Fecha en formato `YYYY-MM-DD`

**Respuesta:** Archivo PDF descargable

### 11. PDF - Resumen de Caja

**Endpoint:** `GET /exports/pdf/resumen-caja/`

**Parámetros:**
- `date` (requerido): Fecha en formato `YYYY-MM-DD`

**Respuesta:** Archivo PDF descargable

### 12. PDF - Caja Chica Mejorada

**Endpoint:** `GET /exports/pdf/caja-chica-mejorada/`

**Parámetros:**
- `date` (requerido): Fecha en formato `YYYY-MM-DD`

**Respuesta:** Archivo PDF descargable

### 13. PDF - Tickets Pagados

**Endpoint:** `GET /exports/pdf/tickets-pagados/`

**Parámetros:**
- `date` (requerido): Fecha en formato `YYYY-MM-DD`

**Respuesta:** Archivo PDF descargable

## 📊 Endpoints de Exportación Excel

### 14. Excel - Citas en Rango

**Endpoint:** `GET /exports/excel/citas-rango/`

**Parámetros:**
- `start` (requerido): Fecha de inicio en formato `YYYY-MM-DD`
- `end` (requerido): Fecha de fin en formato `YYYY-MM-DD`

**Respuesta:** Archivo Excel descargable

### 15. Excel - Caja Chica Mejorada

**Endpoint:** `GET /exports/excel/caja-chica-mejorada/`

**Parámetros:**
- `date` (requerido): Fecha en formato `YYYY-MM-DD`

**Respuesta:** Archivo Excel descargable

### 16. Excel - Tickets Pagados

**Endpoint:** `GET /exports/excel/tickets-pagados/`

**Parámetros:**
- `date` (requerido): Fecha en formato `YYYY-MM-DD`

**Respuesta:** Archivo Excel descargable

## 🏢 Endpoints de Company Data

### 17. Datos de la Empresa

**Endpoint:** `GET /company/`

**Respuesta:**
```json
{
    "id": 1,
    "name": "Clínica Reflexo",
    "address": "Calle Principal 123",
    "phone": "+1234567890",
    "email": "info@reflexo.com"
}
```

## Características Importantes

### ⚠️ Exclusión de Domingos

**Todas las estadísticas excluyen automáticamente los domingos:**

- **Ingresos por día:** Solo incluye Lunes (1) a Sábado (6)
- **Sesiones por día:** Solo incluye Lunes (1) a Sábado (6)
- **Métricas principales:** No cuenta citas de domingos
- **Rendimiento de terapeutas:** No incluye sesiones de domingos
- **Tipos de pago:** No cuenta transacciones de domingos
- **Tipos de pacientes:** No incluye citas de domingos

### Mapeo de Días de la Semana

```python
{
    1: "Lunes",
    2: "Martes", 
    3: "Miercoles",
    4: "Jueves",
    5: "Viernes",
    6: "Sabado"
    # Nota: No incluye 7 (Domingo)
}
```

## Estructura de Respuesta

### Terapeutas
- `id`: ID del terapeuta
- `terapeuta`: Nombre completo del terapeuta
- `sesiones`: Número total de sesiones (sin domingos)
- `ingresos`: Ingresos totales (sin domingos)
- `raiting`: Calificación promedio

### Tipos de Pago
- Clave: Nombre del tipo de pago
- Valor: Número de usos (sin domingos)

### Métricas Principales
- `ttlpacientes`: Total de pacientes únicos
- `ttlsesiones`: Total de sesiones (sin domingos)
- `ttlganancias`: Total de ganancias (sin domingos)

### Ingresos por Día
- Solo incluye días laborales (Lunes a Sábado)
- Clave: Nombre del día
- Valor: Monto total de ingresos

### Sesiones por Día
- Solo incluye días laborales (Lunes a Sábado)
- Clave: Nombre del día
- Valor: Número de sesiones

### Tipos de Pacientes
- `c`: Citas con status "C"
- `cc`: Citas con status "CC"

## Códigos de Error

### 400 Bad Request
```json
{
    "error": "Parámetros 'start' y 'end' son requeridos."
}
```

```json
{
    "error": "La fecha de inicio no puede ser mayor que la fecha de fin."
}
```

```json
{
    "error": "Formato de fecha inválido. Use YYYY-MM-DD."
}
```

### 500 Internal Server Error
```json
{
    "error": "Error interno del servidor: [detalle del error]"
}
```

## Ejemplos de Uso

### Obtener estadísticas de una semana (sin domingos)
```bash
curl "http://localhost:8000/reports/statistics/?start=2024-01-01&end=2024-01-07"
```

### Obtener estadísticas de un mes
```bash
curl "http://localhost:8000/reports/statistics/?start=2024-01-01&end=2024-01-31"
```

### Obtener citas por terapeuta
```bash
curl "http://localhost:8000/reports/appointments-per-therapist/?date=2024-01-15"
```

### Exportar PDF de caja diaria
```bash
curl "http://localhost:8000/exports/pdf/resumen-caja/?date=2024-01-15" -o caja_diaria.pdf
```

### Exportar Excel de citas en rango
```bash
curl "http://localhost:8000/exports/excel/citas-rango/?start=2024-01-01&end=2024-01-31" -o citas_enero.xlsx
```

## Notas Técnicas

1. **Filtrado automático:** El sistema usa `ExtractWeekDay` de Django para extraer el día de la semana y solo procesa días 1-6.

2. **Rendimiento:** Las consultas están optimizadas con agregaciones de base de datos.

3. **Consistencia:** Todas las métricas mantienen la misma lógica de exclusión de domingos.

4. **Formato de fechas:** Todas las fechas deben estar en formato ISO (YYYY-MM-DD).

5. **Soporte POST:** Los endpoints de reportes soportan tanto GET como POST con parámetros en el body.

6. **Exportaciones:** Los endpoints de exportación devuelven archivos binarios (PDF/Excel) listos para descargar.

## Testing

Se incluye un test completo en `test_statistics_sunday_exclusion.py` que verifica:
- Que los domingos no se incluyen en ingresos
- Que los domingos no se incluyen en sesiones  
- Que las métricas principales excluyen domingos
- Que el rendimiento de terapeutas excluye domingos
- Que los tipos de pago excluyen domingos
- Que los tipos de pacientes excluyen domingos

Para ejecutar el test:
```bash
python manage.py test company_reports.tests.test_statistics_sunday_exclusion
```

## Resumen de Endpoints

| Categoría | Endpoint | Método | Parámetros | Descripción |
|-----------|----------|--------|------------|-------------|
| **Estadísticas** | `/reports/statistics/` | GET | start, end | Estadísticas completas |
| **Estadísticas** | `/statistics/metricas/` | GET | start, end | Estadísticas (ViewSet) |
| **Reportes** | `/reports/appointments-per-therapist/` | GET/POST | date | Citas por terapeuta |
| **Reportes** | `/reports/patients-by-therapist/` | GET/POST | date | Pacientes por terapeuta |
| **Reportes** | `/reports/daily-cash/` | GET/POST | date | Caja diaria |
| **Reportes** | `/reports/improved-daily-cash/` | GET/POST | date | Caja diaria mejorada |
| **Reportes** | `/reports/daily-paid-tickets/` | GET/POST | date | Tickets pagados |
| **Reportes** | `/reports/appointments-between-dates/` | GET/POST | start, end | Citas entre fechas |
| **PDF** | `/exports/pdf/citas-terapeuta/` | GET | date | PDF citas por terapeuta |
| **PDF** | `/exports/pdf/pacientes-terapeuta/` | GET | date | PDF pacientes por terapeuta |
| **PDF** | `/exports/pdf/resumen-caja/` | GET | date | PDF resumen de caja |
| **PDF** | `/exports/pdf/caja-chica-mejorada/` | GET | date | PDF caja mejorada |
| **PDF** | `/exports/pdf/tickets-pagados/` | GET | date | PDF tickets pagados |
| **Excel** | `/exports/excel/citas-rango/` | GET | start, end | Excel citas en rango |
| **Excel** | `/exports/excel/caja-chica-mejorada/` | GET | date | Excel caja mejorada |
| **Excel** | `/exports/excel/tickets-pagados/` | GET | date | Excel tickets pagados |
| **Company** | `/company/` | GET | - | Datos de la empresa |
