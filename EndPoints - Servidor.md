# 🔌 API Endpoints Completo - Backend Reflexo MTV

## 🌐 Base URL
```
http://localhost:8000/  # Desarrollo local
```

## 📋 Estándar de URLs Unificado
Todas las APIs siguen el patrón: `/api/[modulo]/[recurso]/`

---

## 🏗️ Módulo 1: Arquitectura y Autenticación (`/api/architect/`)

### Autenticación

| Método     | Endpoint                                                | Descripción                       | Autenticación |
|------------|---------------------------------------------------------|-----------------------------------|---------------|
| **GET**    | `/api/architect/roles/`                                 | Listar Roles                      |   Requerida   |
| **POST**   | `/api/architect/roles/create/`                          | Crear Rol                         |   Requerida   |
| **PUT**    | `/api/architect/roles/{id}/edit/`                       | Editar Rol                        |   Requerida   |
| **DELETE** | `/api/architect/roles/{id}/delete/`                     | Eliminar Rol                      |   Requerida   |
|--------------------------------------------------------------------------------------------------------------------------|
| **POST**   | `/api/architect/auth/login/`                            | Login de usuario                  |  No Requerida |
| **POST**   | `/api/architect/auth/register/`                         | Registro de usuario               |  No Requerida |
| **POST**   | `/api/architect/auth/logout/`                           | Registro de usuario               |   Requerida   |
|--------------------------------------------------------------------------------------------------------------------------|
| **GET**    | `/api/architect/users/`                                 | Listar Usuarios                   |   Requerida   |
| **POST**   | `/api/architect/users/`                                 | Crear Usuario                     |   Requerida   |
| **PUT**    | `/api/architect/users/id/`                              | Editar Usuario                    |   Requerida   |
| **DELETE** | `/api/architect/users/id/`                              | Eliminar Usuario                  |   Requerida   |
| **GET**    | `/api/architect/users/id/`                              | Ver Usuario Especifico            |   Requerida   |
| **POST**   | `/api/architect/users/id/upload/`                       | Subir Foto de Usuario             |   Requerida   |
| **PUT**    | `/api/architect/users/id/upload/`                       | Actualizar Foto de Usuario        |   Requerida   |
| **DELETE** | `/api/architect/users/id/upload/`                       | Eliminar Foto de Usuario          |   Requerida   |
|--------------------------------------------------------------------------------------------------------------------------|

#### Ejemplos de Autenticación

**Crear Rol:**
- **Método:** POST
- **URL:** `http://localhost:8000/api/architect/roles/create/`
- **Auth:** Basic Auth
  - Crear usuario con 'python manage.py createsuperuser' desde el codigo fuente.
- **Headers:**
  ```
  Content-Type: application/json
  ```
- **Body (raw JSON):**
```json
{
    "name": "Admin",
    "guard_name": "Administrador"
}
```
**Respuesta Exitosa:**
```json
{
    "id": 6,
    "name": "Admin",
    "guard_name": "Administrador",
    "created_at": "2025-09-26T20:23:08.471629Z",
    "updated_at": "2025-09-26T20:23:08.471646Z"
}
```

---------------------------------------------------------------------------------------------------------------------------

**Listar Roles:**
- **Método:** GET
- **URL:** `http://127.0.0.1:8000/api/architect/roles/`
- **Auth:** Basic Auth
  - Crear usuario con 'python manage.py createsuperuser' desde el codigo fuente.
- **Headers:**
  ```
  Content-Type: application/json
  ```
- **Body (raw JSON):**
  ```json
  **vacio**
  ```
**Respuesta Exitosa:**
```json
[
    {
        "id": 6,
        "name": "Admin",
        "guard_name": "Administrador",
        "created_at": "2025-09-26T20:23:08.471629Z",
        "updated_at": "2025-09-26T20:23:08.471646Z"
    },
    {
        "id": 3,
        "name": "jqwrjqwrqwrqw",
        "guard_name": "qwrqwrqqwrqwrqww",
        "created_at": "2025-09-26T20:17:56.937957Z",
        "updated_at": "2025-09-26T20:17:56.937980Z"
    },
    {
        "id": 4,
        "name": "jqwrjqwrqwrqw",
        "guard_name": "qwrqwrqqwrqwrqww",
        "created_at": "2025-09-26T20:18:44.777515Z",
        "updated_at": "2025-09-26T20:18:44.777539Z"
    },
    {
        "id": 5,
        "name": "jqwrjqwrqwrqw",
        "guard_name": "qwrqwrqqwrqwrqww",
        "created_at": "2025-09-26T20:22:45.283337Z",
        "updated_at": "2025-09-26T20:22:45.283355Z"
    }
]
```

---------------------------------------------------------------------------------------------------------------------------

**Editar Rol:**
- **Método:** PUT
- **URL:** `http://localhost:8000/api/architect/roles/id/edit/`
- **Auth:** Basic Auth
  - Crear usuario con 'python manage.py createsuperuser' desde el codigo fuente.
- **Headers:**
  ```
  Content-Type: application/json
  ```
- **Body (raw JSON):**
```json
{
    "name": "Member",
    "guard_name": "Member"
}
```
**Respuesta Exitosa:**
```json
{
    "id": 3,
    "name": "Member",
    "guard_name": "Member",
    "created_at": "2025-09-26T20:17:56.937957Z",
    "updated_at": "2025-09-26T20:24:50.382867Z"
}
```

---------------------------------------------------------------------------------------------------------------------------

**Eliminar Rol:**
- **Método:** DELETE
- **URL:** `http://localhost:8000/api/architect/roles/id/delete/`
- **Auth:** Basic Auth
  - Crear usuario con 'python manage.py createsuperuser' desde el codigo fuente.
- **Headers:**
  ```
  Content-Type: application/json
  ```
- **Body (raw JSON):**
```json
**vacio**
```
**Respuesta Exitosa:**
```json
{
    "message": "Rol 'jqwrjqwrqwrqw' eliminado exitosamente",
    "deleted_role": {
        "id": 4,
        "name": "jqwrjqwrqwrqw"
    }
}
```

---------------------------------------------------------------------------------------------------------------------------

**Iniciar Sesion:**
- **Método:** POST
- **URL:** `http://localhost:8000/api/architect/auth/login/`
- **Auth:** Basic Auth
  - Crear usuario con 'python manage.py createsuperuser' desde el codigo fuente.
- **Headers:**
  ```
  Content-Type: application/json
  ```
- **Body (raw JSON):**
```json
{
    "email": "sosa2@gmail.com",
    "password": "Sosa2159//"
}
```
**Respuesta Exitosa:**
```json
{
    "email": "sosa2@gmail.com",
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc2NjY5NDQ0MCwiaWF0IjoxNzU4OTE4NDQwLCJqdGkiOiI0YzNkNzVlMjc1MDg0OGY2OWU3MzQ0MGE0MTQ0YmI5YyIsInVzZXJfaWQiOiI2In0.WV8wdbxvRigHqco4JW6q0k0H-qYufbEGvixbCPOWnFc",
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzYxNTEwNDQwLCJpYXQiOjE3NTg5MTg0NDAsImp0aSI6ImQ4YTg4ZjA2NjlkNjQzNTM5YWI4NjE3ODg5MTFmYzgwIiwidXNlcl9pZCI6IjYifQ._23OwPEukDFQdyHK5OXvj4BvHCOWxsVBv4JRfAyh-YY",
    "user_id": 6
}
```

---------------------------------------------------------------------------------------------------------------------------

**Registrar Usuario:**
- **Método:** POST
- **URL:** `http://localhost:8000/api/architect/auth/register/`
- **Auth:** Basic Auth
  - Crear usuario con 'python manage.py createsuperuser' desde el codigo fuente.
- **Headers:**
  ```
  Content-Type: application/json
  ```
- **Body (raw JSON):**
```json
{
    "user_name": "Juan Carlos",
    "email": "Juan@gmail.com",
    "document_number": "123456798",
    "password": "Juan159//",
    "password_confirm": "Juan159//"
}
```
**Respuesta Exitosa:**
```json
{
    "message": "Usuario registrado con éxito"
}
```

---------------------------------------------------------------------------------------------------------------------------

**Cerrar Sesion:**
- **Método:** POST
- **URL:** `http://localhost:8000/api/architect/auth/logout/`
- **Auth:** Basic Auth
  - Crear usuario con 'python manage.py createsuperuser' desde el codigo fuente.
- **Headers:**
  ```
  Content-Type: application/json
  ```
- **Body (raw JSON):**
```json
{
    "refresh": "Token Refresh que te dieron cuando iniciaste sesion"
}
```
**Respuesta Exitosa:**
```json
{
    "message": "Sesión cerrada exitosamente"
}
```

---------------------------------------------------------------------------------------------------------------------------

**Crear Usuario:**
- **Método:** POST
- **URL:** `http://localhost:8000/api/architect/users/`
- **Auth:** Basic Auth
  - Crear usuario con 'python manage.py createsuperuser' desde el codigo fuente.
- **Headers:**
  ```
  Content-Type: application/json
  ```
- **Body (raw JSON):**
```json
{
    "document_type": 4,
    "document_number": "32322678",
    "name": "Juan Carlos",
    "paternal_lastname": "Pérez",
    "maternal_lastname": "García",
    "email": "juanaaa@ejemplo.com",
    "sex": "M",
    "phone": "987654321",
    "user_name": "juanperezz",
    "password": "MiPassword123!",
    "password_change": false,
    "account_statement": "A",
    "country": 1
}
```
**Respuesta Exitosa:**
```json
{
    "id": 12,
    "document_type": 4,
    "document_type_name": "Carne de Extranjeria",
    "document_number": "32322678",
    "photo_url": null,
    "photo_url_display": null,
    "name": "Juan Carlos",
    "paternal_lastname": "Pérez",
    "maternal_lastname": "García",
    "full_name": "Juan Carlos Pérez García",
    "email": "juanaaa@ejemplo.com",
    "sex": "M",
    "phone": "987654321",
    "user_name": "juanperezz",
    "password_change": false,
    "last_session": "2025-09-27T15:16:41.308843Z",
    "account_statement": "A",
    "email_verified_at": null,
    "country": 1,
    "country_name": "Afganistán",
    "remember_token": null,
    "is_active": true,
    "is_staff": false,
    "is_superuser": false,
    "last_login": null,
    "date_joined": "2025-09-27T15:16:41.308808Z",
    "created_at": "2025-09-27T15:16:41.309118Z",
    "updated_at": "2025-09-27T15:16:41.309128Z",
    "deleted_at": null
}
```

---------------------------------------------------------------------------------------------------------------------------

**Listar Usuarios:**
- **Método:** GET
- **URL:** `http://127.0.0.1:8000/api/architect/users/`
- **Auth:** Basic Auth
  - Crear usuario con 'python manage.py createsuperuser' desde el codigo fuente.
- **Headers:**
  ```
  Content-Type: application/json
  ```
- **Body (raw JSON):**
  ```json
  **vacio**
  ```
**Respuesta Exitosa:**
```json
[
    {
        "id": 1,
        "document_type": null,
        "document_number": null,
        "photo_url": "http://localhost:8000/media/photo_pics/Captura_de_pantalla_2025-04-17_152643.png",
        "photo_url_display": "http://localhost:8000/media/photo_pics/Captura_de_pantalla_2025-04-17_152643.png",
        "name": null,
        "paternal_lastname": null,
        "maternal_lastname": null,
        "full_name": "",
        "email": "anonymous",
        "sex": null,
        "phone": null,
        "user_name": null,
        "password_change": false,
        "last_session": "2025-09-24T19:32:35.843317Z",
        "account_statement": "A",
        "email_verified_at": null,
        "country": null,
        "remember_token": null,
        "is_active": true,
        "is_staff": false,
        "is_superuser": false,
        "last_login": null,
        "date_joined": "2025-09-24T19:32:35.843296Z",
        "created_at": "2025-09-24T19:32:35.843581Z",
        "updated_at": "2025-09-24T19:32:35.843587Z",
        "deleted_at": null
    },
    {
        "id": 4,
        "document_type": null,
        "document_number": "9876543",
        "photo_url": "http://localhost:8000/media/photo_pics/Captura_de_pantalla_2025-04-17_152643_s6a0rBB.png",
        "photo_url_display": "http://localhost:8000/media/photo_pics/Captura_de_pantalla_2025-04-17_152643_s6a0rBB.png",
        "name": null,
        "paternal_lastname": null,
        "maternal_lastname": null,
        "full_name": "",
        "email": "sosa1@gmail.com",
        "sex": null,
        "phone": null,
        "user_name": "sosa1",
        "password_change": false,
        "last_session": "2025-09-24T19:52:55.480757Z",
        "account_statement": "A",
        "email_verified_at": null,
        "country": null,
        "remember_token": null,
        "is_active": true,
        "is_staff": true,
        "is_superuser": true,
        "last_login": "2025-09-24T19:53:25.991745Z",
        "date_joined": "2025-09-24T19:52:55.480738Z",
        "created_at": "2025-09-24T19:52:55.826726Z",
        "updated_at": "2025-09-24T19:52:55.826734Z",
        "deleted_at": null
    },
    {
        "id": 6,
        "document_type": null,
        "document_number": "98799999",
        "photo_url": null,
        "photo_url_display": null,
        "name": null,
        "paternal_lastname": null,
        "maternal_lastname": null,
        "full_name": "",
        "email": "sosa2@gmail.com",
        "sex": null,
        "phone": null,
        "user_name": "sosa2",
        "password_change": false,
        "last_session": "2025-09-25T18:32:05.603828Z",
        "account_statement": "A",
        "email_verified_at": null,
        "country": null,
        "remember_token": null,
        "is_active": true,
        "is_staff": true,
        "is_superuser": true,
        "last_login": null,
        "date_joined": "2025-09-25T18:32:05.603803Z",
        "created_at": "2025-09-25T18:32:05.958710Z",
        "updated_at": "2025-09-25T18:32:05.958717Z",
        "deleted_at": null
    },
    {
        "id": 8,
        "document_type": null,
        "document_number": "12345678",
        "photo_url": null,
        "photo_url_display": null,
        "name": null,
        "paternal_lastname": null,
        "maternal_lastname": null,
        "full_name": "",
        "email": "Christhoper@ejemplo.com",
        "sex": null,
        "phone": null,
        "user_name": "Christho",
        "password_change": false,
        "last_session": "2025-09-26T17:35:29.002280Z",
        "account_statement": "A",
        "email_verified_at": null,
        "country": null,
        "remember_token": null,
        "is_active": true,
        "is_staff": false,
        "is_superuser": false,
        "last_login": null,
        "date_joined": "2025-09-26T17:35:29.002252Z",
        "created_at": "2025-09-26T17:35:29.360478Z",
        "updated_at": "2025-09-26T17:35:29.360486Z",
        "deleted_at": null
    },
    {
        "id": 9,
        "document_type": null,
        "document_number": "123456798",
        "photo_url": null,
        "photo_url_display": null,
        "name": null,
        "paternal_lastname": null,
        "maternal_lastname": null,
        "full_name": "",
        "email": "Juan@gmail.com",
        "sex": null,
        "phone": null,
        "user_name": "Juan Carlos",
        "password_change": false,
        "last_session": "2025-09-26T20:29:20.148500Z",
        "account_statement": "A",
        "email_verified_at": null,
        "country": null,
        "remember_token": null,
        "is_active": true,
        "is_staff": false,
        "is_superuser": false,
        "last_login": null,
        "date_joined": "2025-09-26T20:29:20.148478Z",
        "created_at": "2025-09-26T20:29:20.517635Z",
        "updated_at": "2025-09-26T20:29:20.536015Z",
        "deleted_at": null
    },
    {
        "id": 10,
        "document_type": 4,
        "document_type_name": "Carne de Extranjeria",
        "document_number": "87654321",
        "photo_url": null,
        "photo_url_display": null,
        "name": "Sebastian Huamanni",
        "paternal_lastname": "Gonzales",
        "maternal_lastname": "Castillo",
        "full_name": "Sebastian Huamanni Gonzales Castillo",
        "email": "sebas@ejemplo.com",
        "sex": "M",
        "phone": "987654321",
        "user_name": "Sebas",
        "password_change": false,
        "last_session": "2025-09-26T20:36:09.717261Z",
        "account_statement": "A",
        "email_verified_at": null,
        "country": 1,
        "country_name": "Afganistán",
        "remember_token": null,
        "is_active": true,
        "is_staff": false,
        "is_superuser": false,
        "last_login": null,
        "date_joined": "2025-09-26T20:36:09.717230Z",
        "created_at": "2025-09-26T20:36:09.717524Z",
        "updated_at": "2025-09-26T20:38:03.957589Z",
        "deleted_at": "2025-09-26T20:38:27.574941Z"
    },
    {
        "id": 11,
        "document_type": 4,
        "document_type_name": "Carne de Extranjeria",
        "document_number": "32345678",
        "photo_url": null,
        "photo_url_display": null,
        "name": "Juan Carlos",
        "paternal_lastname": "Pérez",
        "maternal_lastname": "García",
        "full_name": "Juan Carlos Pérez García",
        "email": "juanaa.perez@ejemplo.com",
        "sex": "M",
        "phone": "987654321",
        "user_name": "juanperez",
        "password_change": false,
        "last_session": "2025-09-26T20:54:07.183958Z",
        "account_statement": "A",
        "email_verified_at": null,
        "country": 1,
        "country_name": "Afganistán",
        "remember_token": null,
        "is_active": true,
        "is_staff": false,
        "is_superuser": false,
        "last_login": null,
        "date_joined": "2025-09-26T20:54:07.183928Z",
        "created_at": "2025-09-26T20:54:07.184220Z",
        "updated_at": "2025-09-26T20:54:07.184227Z",
        "deleted_at": null
    },
    {
        "id": 12,
        "document_type": 4,
        "document_type_name": "Carne de Extranjeria",
        "document_number": "32322678",
        "photo_url": null,
        "photo_url_display": null,
        "name": "Juan Carlos",
        "paternal_lastname": "Pérez",
        "maternal_lastname": "García",
        "full_name": "Juan Carlos Pérez García",
        "email": "juanaaa@ejemplo.com",
        "sex": "M",
        "phone": "987654321",
        "user_name": "juanperezz",
        "password_change": false,
        "last_session": "2025-09-27T15:16:41.308843Z",
        "account_statement": "A",
        "email_verified_at": null,
        "country": 1,
        "country_name": "Afganistán",
        "remember_token": null,
        "is_active": true,
        "is_staff": false,
        "is_superuser": false,
        "last_login": null,
        "date_joined": "2025-09-27T15:16:41.308808Z",
        "created_at": "2025-09-27T15:16:41.309118Z",
        "updated_at": "2025-09-27T15:16:41.309128Z",
        "deleted_at": null
    }
]
```

---------------------------------------------------------------------------------------------------------------------------

**Editar Usuario:**
- **Método:** PUT
- **URL:** `http://localhost:8000/api/architect/users/id/`
- **Auth:** Basic Auth
  - Crear usuario con 'python manage.py createsuperuser' desde el codigo fuente.
- **Headers:**
  ```
  Content-Type: application/json
  ```
- **Body (raw JSON):**
```json
{
    "document_number": "32322678",
    "name": "Juannnn Carlossss",
    "paternal_lastname": "Pérezzz",
    "maternal_lastname": "Garcíaaaa",
    "email": "juanaaaaaaaaa@ejemplo.com",
    "sex": "M",
    "phone": "987654300",
    "user_name": "juanperezz",
    "password": "Juan159//"
}
```
**Respuesta Exitosa:**
```json
{
    "id": 12,
    "document_type": 4,
    "document_type_name": "Carne de Extranjeria",
    "document_number": "32322678",
    "photo_url": null,
    "photo_url_display": null,
    "name": "Juannnn Carlossss",
    "paternal_lastname": "Pérezzz",
    "maternal_lastname": "Garcíaaaa",
    "full_name": "Juannnn Carlossss Pérezzz Garcíaaaa",
    "email": "juanaaaaaaaaa@ejemplo.com",
    "sex": "M",
    "phone": "987654300",
    "user_name": "juanperezz",
    "password_change": false,
    "last_session": "2025-09-27T15:16:41.308843Z",
    "account_statement": "A",
    "email_verified_at": null,
    "country": 1,
    "country_name": "Afganistán",
    "remember_token": null,
    "is_active": true,
    "is_staff": false,
    "is_superuser": false,
    "last_login": null,
    "date_joined": "2025-09-27T15:16:41.308808Z",
    "created_at": "2025-09-27T15:16:41.309118Z",
    "updated_at": "2025-09-27T15:20:24.230685Z",
    "deleted_at": null
}
```

---------------------------------------------------------------------------------------------------------------------------

**Eliminar Usuario:**
- **Método:** DELETE
- **URL:** `http://localhost:8000/api/architect/users/id/`
- **Auth:** Basic Auth
  - Crear usuario con 'python manage.py createsuperuser' desde el codigo fuente.
- **Headers:**
  ```
  Content-Type: application/json
  ```
- **Body (raw JSON):**
```json
**vacio**
```
**Respuesta Exitosa:**
```json
{
    "message": "Usuario eliminado permanentemente (sin verificación)"
}
```

---------------------------------------------------------------------------------------------------------------------------

**Ver Usuario Especifico:**
- **Método:** GET
- **URL:** `http://localhost:8000/api/architect/users/id/`
- **Auth:** Basic Auth
  - Crear usuario con 'python manage.py createsuperuser' desde el codigo fuente.
- **Headers:**
  ```
  Content-Type: application/json
  ```
- **Body (raw JSON):**
```json
**vacio**
```
**Respuesta Exitosa:**
```json
{
    "id": 9,
    "document_type": null,
    "document_number": "123456798",
    "photo_url": "http://localhost:8000/media/photo_pics/Captura_de_pantalla_2025-04-17_184057.png",
    "photo_url_display": "http://localhost:8000/media/photo_pics/Captura_de_pantalla_2025-04-17_184057.png",
    "name": null,
    "paternal_lastname": null,
    "maternal_lastname": null,
    "full_name": "",
    "email": "Juan@gmail.com",
    "sex": null,
    "phone": null,
    "user_name": "Juan Carlos",
    "password_change": false,
    "last_session": "2025-09-26T20:29:20.148500Z",
    "account_statement": "A",
    "email_verified_at": null,
    "country": null,
    "remember_token": null,
    "is_active": true,
    "is_staff": false,
    "is_superuser": false,
    "last_login": null,
    "date_joined": "2025-09-26T20:29:20.148478Z",
    "created_at": "2025-09-26T20:29:20.517635Z",
    "updated_at": "2025-09-26T20:29:20.536015Z",
    "deleted_at": null
}
```

---------------------------------------------------------------------------------------------------------------------------

**Subir Foto de Usuario:**
- **Método:** POST
- **URL:** `http://localhost:8000/api/architect/users/id/`
- **Auth:** Basic Auth
  - Crear usuario con 'python manage.py createsuperuser' desde el codigo fuente.
- **Headers:**
  ```
  Content-Type: application/json
  ```
- **Body (raw JSON):**
```json
  - Key: photo_url --- File
  - Value: Elige foto de tu computadora
```
**Respuesta Exitosa:**
```json
{
    "message": "Foto de perfil subida exitosamente",
    "id": 9,
    "user_name": "Juan Carlos",
    "email": "Juan@gmail.com",
    "photo_url": "/media/photo_pics/Captura_de_pantalla_2025-04-17_184057.png",
    "uploaded_at": "2025-09-26T20:29:20.536015+00:00"
}
```

---------------------------------------------------------------------------------------------------------------------------

**Actualizar Foto de Usuario:**
- **Método:** PUT
- **URL:** `http://localhost:8000/api/architect/users/id/upload/`
- **Auth:** Basic Auth
  - Crear usuario con 'python manage.py createsuperuser' desde el codigo fuente.
- **Headers:**
  ```
  Content-Type: application/json
  ```
- **Body (raw JSON):**
```json
  - Key: photo_url --- File
  - Value: Elige foto de tu computadora
```
**Respuesta Exitosa:**
```json
{
    "message": "Foto de perfil actualizada exitosamente",
    "id": 9,
    "user_name": "Juan Carlos",
    "email": "Juan@gmail.com",
    "photo_url": "/media/photo_pics/Christhoper_Sosa_4_-_BK_4_3.png",
    "updated_at": "2025-09-26T20:29:20.536015+00:00"
}
```

---------------------------------------------------------------------------------------------------------------------------

**Eliminar Foto de Usuario:**
- **Método:** DELETE
- **URL:** `http://localhost:8000/api/architect/users/id/upload/`
- **Auth:** Basic Auth
  - Crear usuario con 'python manage.py createsuperuser' desde el codigo fuente.
- **Headers:**
  ```
  Content-Type: application/json
  ```
- **Body (raw JSON):**
```json
**vacio**
```
**Respuesta Exitosa:**
```json
{
    "message": "Foto de perfil eliminada exitosamente",
    "id": 9,
    "user_name": "Juan Carlos",
    "email": "Juan@gmail.com",
    "photo_url": null,
    "deleted_at": "2025-09-26T20:29:20.536015+00:00"
}
```

---------------------------------------------------------------------------------------------------------------------------

## 👤 Módulo 2: Perfiles de Usuarios (`/api/profiles/`)

### Gestión de Usuario
| Método     | Endpoint                                                | Descripción                       | Autenticación |
|------------|---------------------------------------------------------|-----------------------------------|---------------|
| **GET**    | `/api/profiles/users/me/`                               | Listar Mi Perfil                  |   Requerida   |
| **PUT**    | `/api/profiles/users/me/update/`                        | Editar Mi Perfil                  |   Requerida   |
| **POST**   | `/api/profiles/users/me/photo/`                         | Subir Mi Foto de Perfil           |   Requerida   |
| **PUT**    | `/api/profiles/users/me/photo/`                         | Actualizar Mi Foto de Perfil      |   Requerida   |
| **DELETE** | `/api/profiles/users/me/photo/`                         | Eliminar Mi Foto de Perfil        |   Requerida   |
| **GET**    | `/api/profiles/users/search/?q=dana`                    | Buscar Usuario                    |   Requerida   |
| **POST**   | `/api/profiles/password/change/`                        | Cambiar Contraseña                |   Requerida   |
| **POST**   | `/api/profiles/password/reset/`                         | Solicitar Reseteo de Contraseña   |   Requerida   |
| **POST**   | `/api/profiles/password/reset/confirm/`                 | Confirmar Reseteo de Contraseña   |   Requerida   |
| **PATCH**  | `/api/profiles/profiles/settings/`                      | Actualizar Configuracion de Perfil|   Requerida   |
| **POST**   | `/api/profiles/password/strength/`                      | Validar Fortaleza de Contraseña   |   Requerida   |
| **GET**    | `/api/profiles/password/history/`                       | Historial de Cambios de Contraseña|   Requerida   |
| **GET**    | `/api/profiles/password/policy/`                        | Listar Politicas de Contraseña    |   Requerida   |
| **POST**   | `/api/profiles/verification/code/`                      | Solicitar Verificacion de Email   |   Requerida   |
| **POST**   | `/api/profiles/verification/code/resend/`               | Reenviar Codigo de Verificacion   |   Requerida   |
| **POST**   | `/api/profiles/verification/email/change/`              | Solicitar Cambio de Email         |   Requerida   |
| **POST**   | `/api/profiles/verification/email/change/confirm/`      | confirmar Cambio de Email         |   Requerida   |
|--------------------------------------------------------------------------------------------------------------------------|

#### Ejemplos de Perfiles

**Listar Mi Perfil:**
- **Método:** GET
- **URL:** `http://localhost:8000/api/profiles/users/me/`
- **Auth:** Bearer Token
- **Headers:**
  ```
  Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
  ```
- **Respuesta Exitosa:**
```json
{
    "id": 14,
    "user_name": "dana_user",
    "email": "dana@gmail.com",
    "name": "Dana",
    "paternal_lastname": "Smith",
    "maternal_lastname": "Johnson",
    "full_name": "Dana Smith Johnson",
    "phone": "+1234567890",
    "account_statement": "A",
    "is_active": true,
    "date_joined": "2024-01-15T10:30:00Z",
    "last_login": "2024-01-20T14:45:00Z",
    "profile_photo_url": "http://localhost:8000/media/photo_pics/imagen.jpg",
    "document_number": "12345678",
    "document_type": 1,
    "sex": "F",
    "country": 1
}
```

---------------------------------------------------------------------------------------------------------------------------

**Editar Mi Perfil:**
- **Método:** PUT
- **URL:** `http://localhost:8000/api/profiles/users/me/update/`
- **Auth:** Bearer Token
- **Headers:**
  ```
  Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
  Content-Type: application/json
  ```
- **Body (raw JSON):**
```json
{
    "name": "Dana",
    "paternal_lastname": "Smith",
    "maternal_lastname": "Johnson",
    "phone": "+1234567890"
}
```
- **Respuesta Exitosa:**
```json
{
    "message": "Información del usuario actualizada exitosamente",
    "user": {
        "id": 14,
        "user_name": "dana_user",
        "email": "dana@gmail.com",
        "name": "Dana",
        "paternal_lastname": "Smith",
        "maternal_lastname": "Johnson",
        "full_name": "Dana Smith Johnson",
        "phone": "+1234567890",
        "account_statement": "A",
        "is_active": true,
        "date_joined": "2024-01-15T10:30:00Z",
        "last_login": "2024-01-20T14:45:00Z",
        "profile_photo_url": "http://localhost:8000/media/photo_pics/imagen.jpg",
        "document_number": "12345678",
        "document_type": 1,
        "sex": "F",
        "country": 1
    }
}
```

---------------------------------------------------------------------------------------------------------------------------

**Subir Mi Foto de Perfil:**
- **Método:** POST
- **URL:** `http://localhost:8000/api/profiles/users/me/photo/`
- **Auth:** Bearer Token
- **Headers:**
  ```
  Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
  Content-Type: multipart/form-data
  ```
- **Body (form-data):**
  ```
  photo: [archivo de imagen]
  ```
- **Respuesta Exitosa:**
```json
{
    "message": "Foto de perfil subida exitosamente",
    "photo_url": "http://localhost:8000/media/photo_pics/imagen_123456.jpg"
}
```

---------------------------------------------------------------------------------------------------------------------------

**Actualizar Mi Foto de Perfil:**
- **Método:** PUT
- **URL:** `http://localhost:8000/api/profiles/users/me/photo/`
- **Auth:** Bearer Token
- **Headers:**
  ```
  Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
  Content-Type: multipart/form-data
  ```
- **Body (form-data):**
  ```
  photo: [archivo de imagen]
  ```
- **Respuesta Exitosa:**
```json
{
    "message": "Foto de perfil actualizada exitosamente",
    "photo_url": "http://localhost:8000/media/photo_pics/imagen_123456.jpg"
}
```

---------------------------------------------------------------------------------------------------------------------------

**Eliminar Mi Foto de Perfil:**
- **Método:** DELETE
- **URL:** `http://localhost:8000/api/profiles/users/me/photo/`
- **Auth:** Bearer Token
- **Headers:**
  ```
  Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
  ```
- **Respuesta Exitosa:**
```json
{
    "message": "Foto de perfil eliminada exitosamente"
}
```

---------------------------------------------------------------------------------------------------------------------------

**Buscar Usuario:**
- **Método:** GET
- **URL:** `http://localhost:8000/api/profiles/users/search/?q=dana`
- **Auth:** Bearer Token
- **Headers:**
  ```
  Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
  ```
- **Respuesta Exitosa:**
```json
[
    {
        "id": 14,
        "user_name": "dana_user",
        "email": "dana@gmail.com",
        "name": "Dana",
        "paternal_lastname": "Smith",
        "maternal_lastname": "Johnson",
        "full_name": "Dana Smith Johnson",
        "phone": "+1234567890",
        "account_statement": "A",
        "is_active": true,
        "date_joined": "2024-01-15T10:30:00Z",
        "last_login": "2024-01-20T14:45:00Z",
        "profile_photo_url": "http://localhost:8000/media/photo_pics/imagen.jpg",
        "document_number": "12345678",
        "document_type": 1,
        "sex": "F",
        "country": 1
    }
]
```

---------------------------------------------------------------------------------------------------------------------------

**Cambiar Contraseña:**
- **Método:** POST
- **URL:** `http://localhost:8000/api/profiles/password/change/`
- **Auth:** Bearer Token
- **Headers:**
  ```
  Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
  Content-Type: application/json
  ```
- **Body (raw JSON):**
```json
{
    "current_password": "mi_contraseña_actual",
    "new_password": "MiNuevaContraseña123!",
    "new_password_confirm": "MiNuevaContraseña123!"
}
```
- **Respuesta Exitosa:**
```json
{
    "message": "Contraseña cambiada exitosamente"
}
```

---------------------------------------------------------------------------------------------------------------------------

**Solicitar Reseteo de Contraseña:**
- **Método:** POST
- **URL:** `http://localhost:8000/api/profiles/password/reset/`
- **Auth:** Bearer Token
- **Headers:**
  ```
  Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
  Content-Type: application/json
  ```
- **Body (raw JSON):**
```json
{
    "email": "dana@gmail.com"
}
```
- **Respuesta Exitosa (si el email existe):**
```json
{
    "message": "Se ha enviado un código de verificación a tu email",
    "code": "123456",
    "expires_at": "2024-01-20T15:30:00Z"
}
```
- **Respuesta (si el email NO existe):**
```json
{
    "message": "Si el email existe, se ha enviado un código de verificación"
}
```

---------------------------------------------------------------------------------------------------------------------------

**Confirmar Reseteo de Contraseña:**
- **Método:** POST
- **URL:** `http://localhost:8000/api/profiles/password/reset/confirm/`
- **Auth:** Bearer Token
- **Headers:**
  ```
  Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
  Content-Type: application/json
  ```
- **Body (raw JSON):**
```json
{
    "code": "123456",
    "new_password": "MiNuevaContraseña123!",
    "new_password_confirm": "MiNuevaContraseña123!"
}
```
- **Respuesta Exitosa:**
```json
{
    "message": "Contraseña restablecida exitosamente"
}
```
- **Respuesta si el código expiró:**
```json
{
    "error": "El código de verificación ha expirado"
}
```
- **Respuesta si el código es inválido:**
```json
{
    "error": "Código de verificación inválido"
}
```

---------------------------------------------------------------------------------------------------------------------------

**Actualizar Configuración de Perfil:**
- **Método:** PATCH
- **URL:** `http://localhost:8000/api/profiles/profiles/settings/`
- **Auth:** Bearer Token
- **Headers:**
  ```
  Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
  Content-Type: application/json
  ```
- **Body (raw JSON):**
```json
{
    "account_statement": "A"
}
```
- **Respuesta Exitosa:**
```json
{
    "message": "Configuraciones del perfil actualizadas exitosamente",
    "settings": {
        "account_statement": "A"
    }
}
```

---------------------------------------------------------------------------------------------------------------------------

**Validar Fortaleza de Contraseña:**
- **Método:** POST
- **URL:** `http://localhost:8000/api/profiles/password/strength/`
- **Auth:** Bearer Token
- **Headers:**
  ```
  Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
  Content-Type: application/json
  ```
- **Body (raw JSON):**
```json
{
    "password": "MiContraseña123!"
}
```
- **Respuesta Exitosa:**
```json
{
    "message": "La contraseña cumple con los requisitos de seguridad",
    "is_strong": true
}
```
- **Respuesta con errores:**
```json
{
    "message": "La contraseña no cumple con los requisitos de seguridad",
    "is_strong": false,
    "errors": {
        "password": ["Esta contraseña es muy común."]
    }
}
```

---------------------------------------------------------------------------------------------------------------------------

**Historial de Cambios de Contraseña:**
- **Método:** GET
- **URL:** `http://localhost:8000/api/profiles/password/history/`
- **Auth:** Bearer Token
- **Headers:**
  ```
  Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
  ```
- **Respuesta Exitosa:**
```json
{
    "message": "Historial de cambios de contraseña",
    "last_changed": "2024-01-20T14:45:00Z",
    "total_changes": 1
}
```

---------------------------------------------------------------------------------------------------------------------------

**Listar Políticas de Contraseña:**
- **Método:** GET
- **URL:** `http://localhost:8000/api/profiles/password/policy/`
- **Auth:** Bearer Token
- **Headers:**
  ```
  Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
  ```
- **Respuesta Exitosa:**
```json
{
    "message": "Política de contraseñas",
    "requirements": [
        "Mínimo 8 caracteres",
        "Al menos una letra mayúscula",
        "Al menos una letra minúscula",
        "Al menos un número",
        "Al menos un carácter especial",
        "No puede ser similar a información personal",
        "No puede ser una contraseña común"
    ]
}
```

---------------------------------------------------------------------------------------------------------------------------

**Solicitar Verificación de Email:**
- **Método:** POST
- **URL:** `http://localhost:8000/api/profiles/verification/code/`
- **Auth:** Bearer Token
- **Headers:**
  ```
  Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
  Content-Type: application/json
  ```
- **Body (raw JSON):**
```json
{
    "verification_type": "email_verification",
    "target_email": "dana@gmail.com"
}
```
- **Respuesta Exitosa:**
```json
{
    "message": "Código de verificación enviado exitosamente",
    "code": "123456",
    "expires_at": "2024-01-20T15:30:00Z",
    "verification_type": "email_verification"
}
```

---------------------------------------------------------------------------------------------------------------------------

**Reenviar Código de Verificación:**
- **Método:** POST
- **URL:** `http://localhost:8000/api/profiles/verification/code/resend/`
- **Auth:** Bearer Token
- **Headers:**
  ```
  Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
  Content-Type: application/json
  ```
- **Body (raw JSON):**
```json
{
    "verification_type": "email_verification",
    "target_email": "dana@gmail.com"
}
```
- **Respuesta Exitosa:**
```json
{
    "message": "Nuevo código de verificación enviado exitosamente",
    "code": "789012",
    "expires_at": "2024-01-20T15:35:00Z"
}
```

---------------------------------------------------------------------------------------------------------------------------

**Solicitar Cambio de Email:**
- **Método:** POST
- **URL:** `http://localhost:8000/api/profiles/verification/email/change/`
- **Auth:** Bearer Token
- **Headers:**
  ```
  Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
  Content-Type: application/json
  ```
- **Body (raw JSON):**
```json
{
    "new_email": "dana.new@gmail.com"
}
```
- **Respuesta Exitosa:**
```json
{
    "message": "Se ha enviado un código de verificación a tu nuevo email",
    "code": "345678",
    "expires_at": "2024-01-20T15:30:00Z",
    "target_email": "dana.new@gmail.com"
}
```

---------------------------------------------------------------------------------------------------------------------------

**Confirmar Cambio de Email:**
- **Método:** POST
- **URL:** `http://localhost:8000/api/profiles/verification/email/change/confirm/`
- **Auth:** Bearer Token
- **Headers:**
  ```
  Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
  Content-Type: application/json
  ```
- **Body (raw JSON):**
```json
{
    "code": "345678"
}
```
- **Respuesta Exitosa:**
```json
{
    "message": "Email cambiado exitosamente",
    "new_email": "dana.new@gmail.com"
}
```
- **Respuesta si el código expiró:**
```json
{
    "error": "El código de verificación ha expirado"
}
```
- **Respuesta si el código es inválido:**
```json
{
    "error": "Código de verificación inválido"
}
```
- **Respuesta si falta email objetivo:**
```json
{
    "error": "El código de verificación no tiene un email objetivo válido"
}
```

---------------------------------------------------------------------------------------------------------------------------

## 🩺 Módulo 3: Pacientes y Diagnósticos (`/api/patients/`)

### Pacientes
| Método     | Endpoint                                                | Descripción                       | Autenticación |
|------------|---------------------------------------------------------|-----------------------------------|---------------|
| **GET**    | `/api/patients/diagnoses/`                              | Listar Diagnosticos               |   Requerida   |
| **POST**   | `/api/patients/diagnoses/create/`                       | Crear Diagnostico                 |   Requerida   |
| **PUT**    | `/api/patients/diagnoses/{id}/edit/`                    | Editar Diagnostico                |   Requerida   |
| **DELETE** | `/api/patients/diagnoses/{id}/delete/`                  | Eliminar Diagnostico              |   Requerida   |
---------------------------------------------------------------------------------------------------------------------------|
| **GET**    | `/api/patients/patients/`                               | Listar Pacientes                  |   Requerida   |
| **POST**   | `/api/patients/patients/`                               | Crear Paciente                    |   Requerida   |
| **PUT**    | `/api/patients/patients/{id}/`                          | Actualizar Paciente               |   Requerida   |
| **DELETE** | `/api/patients/patients/{id}/`                          | Eliminar Paciente                 |   Requerida   |
| **GET**    | `/api/patients/patients/{id}/`                          | Ver Paciente Específico           |   Requerida   |
---------------------------------------------------------------------------------------------------------------------------|
| **GET**    | `/api/patients/medical-records/`                        | Listar Historiales Medicos        |   Requerida   |
| **POST**   | `/api/patients/medical-records/`                        | Crear Historial Medico            |   Requerida   |
| **PUT**    | `/api/patients/medical-records/{id}/`                   | Actualizar Historial Medico       |   Requerida   |
| **DELETE** | `/api/patients/medical-records/{id}/`                   | Eliminar Historial Medico         |   Requerida   |
| **GET**    | `/api/patients/medical-records/{id}/`                   | Ver Historial Medico Específico   |   Requerida   |
| **GET**    | `/api/patients/patients/{id}/medical-history/`          | Ver Historial Medico de Paciente  |   Requerida   |---------------------------------------------------------------------------------------------------------------------------|

#### Ejemplos de Diagnosticos

**Crear Diagnostico:**
- **Método:** POST
- **URL:** `http://localhost:8000/api/patients/diagnoses/create/`
- **Auth:** Basic Auth
  - Crear usuario con 'python manage.py createsuperuser' desde el codigo fuente.
- **Headers:**
  ```
  Content-Type: application/json
  ```
- **Body (raw JSON):**
```json
{
    "code": "HOLAAAAA",
    "name": "qwrqwrqwrwqr"
}
```
**Respuesta Exitosa:**
```json
{
    "id": 2,
    "code": "HOLAAAAA",
    "name": "qwrqwrqwrwqr"
}
```

---------------------------------------------------------------------------------------------------------------------------

**Listar Diagnosticos:**
- **Método:** GET
- **URL:** `http://127.0.0.1:8000/api/patients/diagnoses/`
- **Auth:** Basic Auth
  - Crear usuario con 'python manage.py createsuperuser' desde el codigo fuente.
- **Headers:**
  ```
  Content-Type: application/json
  ```
- **Body (raw JSON):**
  ```json
  **vacio**
  ```
**Respuesta Exitosa:**
```json
{
    "diagnoses": [
        {
            "id": 2,
            "code": "HOLAAAAA",
            "name": "qwrqwrqwrwqr"
        },
        {
            "id": 3,
            "code": "HOLAAAAAAAA",
            "name": "qwrqwrqwrwqrWREWR"
        }
    ]
}
```

---------------------------------------------------------------------------------------------------------------------------

**Editar Diagnostico:**
- **Método:** PUT
- **URL:** `http://127.0.0.1:8000/api/patients/diagnoses/id/edit/`
- **Auth:** Basic Auth
  - Crear usuario con 'python manage.py createsuperuser' desde el codigo fuente.
- **Headers:**
  ```
  Content-Type: application/json
  ```
- **Body (raw JSON):**
```json
{
    "code": "HOLI",
    "name": "Como tas?"
}
```
**Respuesta Exitosa:**
```json
{
    "id": 3,
    "code": "HOLI",
    "name": "Como tas?"
}
```

---------------------------------------------------------------------------------------------------------------------------

**Eliminar Diagnostico:**
- **Método:** DELETE
- **URL:** `http://127.0.0.1:8000/api/patients/diagnoses/id/delete/`
- **Auth:** Basic Auth
  - Crear usuario con 'python manage.py createsuperuser' desde el codigo fuente.
- **Headers:**
  ```
  Content-Type: application/json
  ```
- **Body (raw JSON):**
```json
**vacio**
```
**Respuesta Exitosa:**
```json
{
    "status": "deleted",
    "id": 3
}
```

---------------------------------------------------------------------------------------------------------------------------

**Crear Paciente:**
- **Método:** POST
- **URL:** `http://localhost:8000/api/patients/patients/`
- **Auth:** Basic Auth
  - Crear usuario con 'python manage.py createsuperuser' desde el codigo fuente.
- **Headers:**
  ```
  Content-Type: application/json
  ```
- **Body (raw JSON):**
```json
{
        "document_number": "88877766",
        "name": "Christhoper",
        "paternal_lastname": "Sosa",
        "maternal_lastname": "Morales",
        "sex": "M",
        "phone1": "902887587",
        "phone2": "902587887",
        "email": "cristofersosa@gmail.com",
        "personal_reference": "qewrqrqwrqwr",
        "ocupation": "Ingeniero de Sistemas",
        "health_condition": "bien",
        "region_id": 1,
        "province_id": 1,
        "district_id": 1,
        "document_type_id": 4,
        "address": "Av. Libertad 456",
        "birth_date": "1988-04-18T00:00:00Z"
}
```
**Respuesta Exitosa:**
```json
{
    "id": 11,
    "document_number": "88877766",
    "paternal_lastname": "Sosa",
    "maternal_lastname": "Morales",
    "name": "Christhoper",
    "full_name": "Christhoper Sosa Morales",
    "personal_reference": "qewrqrqwrqwr",
    "birth_date": "1988-04-18T00:00:00Z",
    "sex": "M",
    "phone1": "902887587",
    "phone2": "902587887",
    "email": "cristofersosa@gmail.com",
    "ocupation": "Ingeniero de Sistemas",
    "health_condition": "bien",
    "address": "Av. Libertad 456",
    "region": {
        "id": 1,
        "name": "Amazonas",
        "country": 180,
        "created_at": "2025-09-24T21:27:17.604182Z",
        "updated_at": "2025-09-24T21:27:17.604198Z",
        "deleted_at": null
    },
    "province": {
        "id": 1,
        "name": "Chachapoyas",
        "region": 1,
        "region_name": "Amazonas",
        "created_at": "2025-09-24T21:27:17.714490Z",
        "updated_at": "2025-09-24T21:27:17.714508Z",
        "deleted_at": null
    },
    "district": {
        "id": 1,
        "name": "Chachapoyas",
        "province": 1,
        "province_name": "Chachapoyas",
        "region_name": "Amazonas",
        "created_at": "2025-09-24T21:27:17.965328Z",
        "updated_at": "2025-09-24T21:27:17.965349Z",
        "deleted_at": null
    },
    "document_type": {
        "id": 4,
        "name": "Carne de Extranjeria",
        "description": "Carne de Extranjeria",
        "created_at": "2025-09-25T14:58:39.072486Z",
        "updated_at": "2025-09-25T14:58:39.072514Z"
    },
    "created_at": "2025-09-26T17:50:28.311367Z",
    "updated_at": "2025-09-26T17:50:28.311375Z",
    "deleted_at": null
}
```

---------------------------------------------------------------------------------------------------------------------------

**Listar Pacientes:**
- **Método:** GET
- **URL:** `http://127.0.0.1:8000/api/patients/patients/`
- **Auth:** Basic Auth
  - Crear usuario con 'python manage.py createsuperuser' desde el codigo fuente.
- **Headers:**
  ```
  Content-Type: application/json
  ```
- **Body (raw JSON):**
  ```json
  **vacio**
  ```
**Respuesta Exitosa:**
```json
[
    {
        "id": 11,
        "document_number": "88877766",
        "name": "Christhoper",
        "paternal_lastname": "Sosa",
        "maternal_lastname": "Morales",
        "full_name": "Christhoper Sosa Morales",
        "age": 37,
        "sex": "M",
        "phone1": "902887587",
        "phone2": "902587887",
        "email": "cristofersosa@gmail.com",
        "personal_reference": "qewrqrqwrqwr",
        "ocupation": "Ingeniero de Sistemas",
        "health_condition": "bien",
        "region_name": "Amazonas",
        "province_name": "Chachapoyas",
        "district_name": "Chachapoyas",
        "document_type_name": "Carne de Extranjeria",
        "address": "Av. Libertad 456",
        "birth_date": "1988-04-18T00:00:00Z",
        "created_at": "2025-09-26T17:50:28.311367Z"
    },
    {
        "id": 9,
        "document_number": "24017561",
        "name": "Roberto Carlos",
        "paternal_lastname": "Lópezz",
        "maternal_lastname": "Moralesss",
        "full_name": "Roberto Carlos Lópezz Moralesss",
        "age": 37,
        "sex": "M",
        "phone1": "+51 423 000 333",
        "phone2": "+51 902 000 412",
        "email": "chris124@ejemplo.com",
        "personal_reference": "qewrqrqwrqwr",
        "ocupation": "Ingeee",
        "health_condition": "qwrqwrwqr",
        "region_name": "Amazonas",
        "province_name": "Chachapoyas",
        "district_name": "Chachapoyas",
        "document_type_name": "Carne de Extranjeria",
        "address": "Av. Libertad 456",
        "birth_date": "1988-04-18T00:00:00Z",
        "created_at": "2025-09-26T17:23:47.333966Z"
    },
    {
        "id": 8,
        "document_number": "24117561",
        "name": "Roberto Carlos",
        "paternal_lastname": "Lópezz",
        "maternal_lastname": "Moralesss",
        "full_name": "Roberto Carlos Lópezz Moralesss",
        "age": 37,
        "sex": "M",
        "phone1": "+51 423 000 333",
        "phone2": "+51 902 000 412",
        "email": "rrqwqwqwrqwrqwrrqwrrqwqwerf@ejemplo.com",
        "personal_reference": "qewrqrqwrqwr",
        "ocupation": "Ingeee",
        "health_condition": "qwrqwrwqr",
        "region_name": "Amazonas",
        "province_name": "Chachapoyas",
        "district_name": "Chachapoyas",
        "document_type_name": "Carne de Extranjeria",
        "address": "Av. Libertad 456",
        "birth_date": "1988-04-18T00:00:00Z",
        "created_at": "2025-09-26T17:22:02.957801Z"
    },
    {
        "id": 7,
        "document_number": "24111111",
        "name": "Roberto Carlos",
        "paternal_lastname": "López",
        "maternal_lastname": "Moralesss",
        "full_name": "Roberto Carlos López Moralesss",
        "age": 37,
        "sex": "M",
        "phone1": "+51 423 333 333",
        "phone2": "+51 902 412 412",
        "email": "rrqwrqwqwerf@ejemplo.com",
        "personal_reference": "qewrqrqwrqwr",
        "ocupation": "Ingeee",
        "health_condition": "qwrwqr",
        "region_name": "Amazonas",
        "province_name": "Chachapoyas",
        "district_name": "Chachapoyas",
        "document_type_name": "Carne de Extranjeria",
        "address": "Av. Libertad 456",
        "birth_date": "1988-04-18T00:00:00Z",
        "created_at": "2025-09-26T17:18:54.216204Z"
    },
    {
        "id": 6,
        "document_number": "21111111",
        "name": "Roberto Carlos",
        "paternal_lastname": "López",
        "maternal_lastname": "Moraless",
        "full_name": "Roberto Carlos López Moraless",
        "age": 37,
        "sex": "M",
        "phone1": "+51 453 333 333",
        "phone2": "+51 812 412 412",
        "email": "roberaeaeto.carlos@ejemplo.com",
        "personal_reference": "qewrqrqwrqwr",
        "ocupation": "Ingeee",
        "health_condition": "qwrwqr",
        "region_name": "Amazonas",
        "province_name": "Chachapoyas",
        "district_name": "Chachapoyas",
        "document_type_name": "Carne de Extranjeria",
        "address": "Av. Libertad 456",
        "birth_date": "1988-04-18T00:00:00Z",
        "created_at": "2025-09-26T17:16:58.354271Z"
    },
    {
        "id": 4,
        "document_number": "22221201",
        "name": "Roberto Carloss",
        "paternal_lastname": "López",
        "maternal_lastname": "Moralessss",
        "full_name": "Roberto Carloss López Moralessss",
        "age": 37,
        "sex": "M",
        "phone1": "+51 333 333 333",
        "phone2": "+51 123 333 333",
        "email": "robwwre@ejemplo.com",
        "personal_reference": "qewrqrqwrqwr",
        "ocupation": "Ingeniero",
        "health_condition": "buena",
        "region_name": "Amazonas",
        "province_name": "Chachapoyas",
        "district_name": "Chachapoyas",
        "document_type_name": "Carne de Extranjeria",
        "address": "Av. Libertad 456",
        "birth_date": "1988-04-18T00:00:00Z",
        "created_at": "2025-09-25T18:37:04.588942Z"
    },
    {
        "id": 3,
        "document_number": "22222211",
        "name": "Roberto Carloss",
        "paternal_lastname": "López",
        "maternal_lastname": "Morales",
        "full_name": "Roberto Carloss López Morales",
        "age": 37,
        "sex": "M",
        "phone1": "+51 333 333 333",
        "phone2": "+51 123 333 333",
        "email": "robe@ejemplo.com",
        "personal_reference": "qewrqrqwrqwr",
        "ocupation": "Ingeniero",
        "health_condition": "buena",
        "region_name": "Amazonas",
        "province_name": "Chachapoyas",
        "district_name": "Chachapoyas",
        "document_type_name": "Carne de Extranjeria",
        "address": "Av. Libertad 456",
        "birth_date": "1988-04-18T00:00:00Z",
        "created_at": "2025-09-25T18:36:42.236276Z"
    },
    {
        "id": 1,
        "document_number": "22222222",
        "name": "Roberto Carlos",
        "paternal_lastname": "López",
        "maternal_lastname": "Morales",
        "full_name": "Roberto Carlos López Morales",
        "age": 37,
        "sex": "M",
        "phone1": "+51 333 333 333",
        "phone2": "+51 123 333 333",
        "email": "roberto@ejemplo.com",
        "personal_reference": "qewrqrqwrqwr",
        "ocupation": "Ingeniero",
        "health_condition": "buena",
        "region_name": "Amazonas",
        "province_name": "Chachapoyas",
        "district_name": "Chachapoyas",
        "document_type_name": "Carne de Extranjeria",
        "address": "Av. Libertad 456",
        "birth_date": "1988-04-18T00:00:00Z",
        "created_at": "2025-09-25T18:07:27.853389Z"
    }
]
```

---------------------------------------------------------------------------------------------------------------------------

**Editar Paciente:**
- **Método:** PUT
- **URL:** `http://127.0.0.1:8000/api/patients/patients/id/`
- **Auth:** Basic Auth
  - Crear usuario con 'python manage.py createsuperuser' desde el codigo fuente.
- **Headers:**
  ```
  Content-Type: application/json
  ```
- **Body (raw JSON):**
```json
{
        "document_number": "88877766",
        "name": "Christhoperrrr",
        "paternal_lastname": "Sosaaaa",
        "maternal_lastname": "Moralesss",
        "sex": "M",
        "phone1": "902887587",
        "phone2": "902587887",
        "email": "cristofersosa@gmail.com",
        "personal_reference": "qewrqrqwrqwr",
        "ocupation": "Ingeniero de Sistemas",
        "health_condition": "bien",
        "region_id": 1,
        "province_id": 1,
        "district_id": 1,
        "document_type_id": 4,
        "address": "Av. Libertad 456",
        "birth_date": "1988-04-18T00:00:00Z"
    }
```
**Respuesta Exitosa:**
```json
{
    "id": 11,
    "document_number": "88877766",
    "paternal_lastname": "Sosaaaa",
    "maternal_lastname": "Moralesss",
    "name": "Christhoperrrr",
    "full_name": "Christhoperrrr Sosaaaa Moralesss",
    "personal_reference": "qewrqrqwrqwr",
    "birth_date": "1988-04-18T00:00:00Z",
    "sex": "M",
    "phone1": "902887587",
    "phone2": "902587887",
    "email": "cristofersosa@gmail.com",
    "ocupation": "Ingeniero de Sistemas",
    "health_condition": "bien",
    "address": "Av. Libertad 456",
    "region": {
        "id": 1,
        "name": "Amazonas",
        "country": 180,
        "created_at": "2025-09-24T21:27:17.604182Z",
        "updated_at": "2025-09-24T21:27:17.604198Z",
        "deleted_at": null
    },
    "province": {
        "id": 1,
        "name": "Chachapoyas",
        "region": 1,
        "region_name": "Amazonas",
        "created_at": "2025-09-24T21:27:17.714490Z",
        "updated_at": "2025-09-24T21:27:17.714508Z",
        "deleted_at": null
    },
    "district": {
        "id": 1,
        "name": "Chachapoyas",
        "province": 1,
        "province_name": "Chachapoyas",
        "region_name": "Amazonas",
        "created_at": "2025-09-24T21:27:17.965328Z",
        "updated_at": "2025-09-24T21:27:17.965349Z",
        "deleted_at": null
    },
    "document_type": {
        "id": 4,
        "name": "Carne de Extranjeria",
        "description": "Carne de Extranjeria",
        "created_at": "2025-09-25T14:58:39.072486Z",
        "updated_at": "2025-09-25T14:58:39.072514Z"
    },
    "created_at": "2025-09-26T17:50:28.311367Z",
    "updated_at": "2025-09-26T17:50:28.311375Z",
    "deleted_at": null
}
```

---------------------------------------------------------------------------------------------------------------------------

**Eliminar Paciente:**
- **Método:** DELETE
- **URL:** `http://127.0.0.1:8000/api/patients/patients/id/`
- **Auth:** Basic Auth
  - Crear usuario con 'python manage.py createsuperuser' desde el codigo fuente.
- **Headers:**
  ```
  Content-Type: application/json
  ```
- **Body (raw JSON):**
```json
**vacio**
```
**Respuesta Exitosa:**
```json
{
    "message": "Paciente eliminado exitosamente",
    "id": 11,
    "name": "Christhoperrrr Sosaaaa Moralesss",
    "deleted_at": "2025-09-26T17:53:01.230919+00:00"
}
```

---------------------------------------------------------------------------------------------------------------------------

**Buscar Paciente Especifico:**
- **Método:** GET
- **URL:** `http://127.0.0.1:8000/api/patients/patients/id/`
- **Auth:** Basic Auth
  - Crear usuario con 'python manage.py createsuperuser' desde el codigo fuente.
- **Headers:**
  ```
  Content-Type: application/json
  ```
- **Body (raw JSON):**
```json
**vacio**
```
**Respuesta Exitosa:**
```json
{
    "id": 9,
    "document_number": "24017561",
    "paternal_lastname": "Lópezz",
    "maternal_lastname": "Moralesss",
    "name": "Roberto Carlos",
    "full_name": "Roberto Carlos Lópezz Moralesss",
    "personal_reference": "qewrqrqwrqwr",
    "birth_date": "1988-04-18T00:00:00Z",
    "sex": "M",
    "phone1": "+51 423 000 333",
    "phone2": "+51 902 000 412",
    "email": "chris124@ejemplo.com",
    "ocupation": "Ingeee",
    "health_condition": "qwrqwrwqr",
    "address": "Av. Libertad 456",
    "region": {
        "id": 1,
        "name": "Amazonas",
        "country": 180,
        "created_at": "2025-09-24T21:27:17.604182Z",
        "updated_at": "2025-09-24T21:27:17.604198Z",
        "deleted_at": null
    },
    "province": {
        "id": 1,
        "name": "Chachapoyas",
        "region": 1,
        "region_name": "Amazonas",
        "created_at": "2025-09-24T21:27:17.714490Z",
        "updated_at": "2025-09-24T21:27:17.714508Z",
        "deleted_at": null
    },
    "district": {
        "id": 1,
        "name": "Chachapoyas",
        "province": 1,
        "province_name": "Chachapoyas",
        "region_name": "Amazonas",
        "created_at": "2025-09-24T21:27:17.965328Z",
        "updated_at": "2025-09-24T21:27:17.965349Z",
        "deleted_at": null
    },
    "document_type": {
        "id": 4,
        "name": "Carne de Extranjeria",
        "description": "Carne de Extranjeria",
        "created_at": "2025-09-25T14:58:39.072486Z",
        "updated_at": "2025-09-25T14:58:39.072514Z"
    },
    "created_at": "2025-09-26T17:23:47.333966Z",
    "updated_at": "2025-09-26T17:23:47.333976Z",
    "deleted_at": null
}
```

---------------------------------------------------------------------------------------------------------------------------

**Crear Historial Medico:**
- **Método:** POST
- **URL:** `http://127.0.0.1:8000/api/patients/medical-records/`
- **Auth:** Basic Auth
  - Crear usuario con 'python manage.py createsuperuser' desde el codigo fuente.
- **Headers:**
  ```
  Content-Type: application/json
  ```
- **Body (raw JSON):**
```json
{
    "patient_id": 9,
    "diagnose_id": 2,
    "diagnosis_date": "2024-04-15",
    "symptoms": "Dolorrr de cabeza, fiebre, malestar general",
    "treatment": "Reposo, paracetamol cada 8 horas",
    "notes": "Paciente presenta síntomas gripales",
    "status": "active"
}
```
**Respuesta Exitosa:**
```json
{
    "id": 4,
    "patient_name": "Roberto Carlos Lópezz Moralesss",
    "patient_id": 9,
    "diagnose_name": "qwrqwrqwrwqr",
    "diagnose_code": "HOLAAAAA",
    "diagnose_id": 2,
    "diagnosis_date": "2024-04-15",
    "symptoms": "Dolorrr de cabeza, fiebre, malestar general",
    "treatment": "Reposo, paracetamol cada 8 horas",
    "notes": "Paciente presenta síntomas gripales",
    "status": "active",
    "created_at": "2025-09-26T18:16:26.938711Z",
    "updated_at": "2025-09-26T18:16:26.938727Z",
    "message": "Historial médico creado exitosamente"
}
```

---------------------------------------------------------------------------------------------------------------------------

**Listar Historiales Medicos:**
- **Método:** GET
- **URL:** `http://127.0.0.1:8000/api/patients/medical-records/`
- **Auth:** Basic Auth
  - Crear usuario con 'python manage.py createsuperuser' desde el codigo fuente.
- **Headers:**
  ```
  Content-Type: application/json
  ```
- **Body (raw JSON):**
  ```json
  **vacio**
  ```
**Respuesta Exitosa:**
```json
{
    "count": 3,
    "num_pages": 1,
    "current_page": 1,
    "results": [
        {
            "id": 4,
            "patient_name": "Roberto Carlos Lópezz Moralesss",
            "diagnose_name": "qwrqwrqwrwqr",
            "diagnose_code": "HOLAAAAA",
            "diagnosis_date": "2024-04-15",
            "symptoms": "Dolorrr de cabeza, fiebre, malestar general",
            "treatment": "Reposo, paracetamol cada 8 horas",
            "notes": "Paciente presenta síntomas gripales",
            "status": "active",
            "created_at": "2025-09-26T18:16:26.938711Z"
        },
        {
            "id": 3,
            "patient_name": "Roberto Carlos Lópezz Moralesss",
            "diagnose_name": "qwrqwrqwrwqr",
            "diagnose_code": "HOLAAAAA",
            "diagnosis_date": "2024-03-15",
            "symptoms": "Dolorrr de cabeza, fiebre, malestar general",
            "treatment": "Reposo, paracetamol cada 8 horas",
            "notes": "Paciente presenta síntomas gripales",
            "status": "active",
            "created_at": "2025-09-26T18:06:01.778142Z"
        },
        {
            "id": 2,
            "patient_name": "Roberto Carlos Lópezz Moralesss",
            "diagnose_name": "qwrqwrqwrwqr",
            "diagnose_code": "HOLAAAAA",
            "diagnosis_date": "2024-02-15",
            "symptoms": "Dolor de cabeza, fiebre, malestar general",
            "treatment": "Reposo, paracetamol cada 8 horas",
            "notes": "Paciente presenta síntomas gripales",
            "status": "active",
            "created_at": "2025-09-26T18:04:01.604883Z"
        }
    ]
}
```

---------------------------------------------------------------------------------------------------------------------------

**Editar Historial Medico:**
- **Método:** PUT
- **URL:** `http://127.0.0.1:8000/api/patients/medical-records/id/`
- **Auth:** Basic Auth
  - Crear usuario con 'python manage.py createsuperuser' desde el codigo fuente.
- **Headers:**
  ```
  Content-Type: application/json
  ```
- **Body (raw JSON):**
```json
{
    "diagnosis_date": "2024-04-16",
    "symptoms": "Dolor de cabeza, fiebre, malestar general",
    "treatment": "Reposo, paracetamol cada 8 horas",
    "notes": "Paciente presenta síntomas gripales",
    "status": "active"
}
```
**Respuesta Exitosa:**
```json
{
    "id": 4,
    "patient_name": "Roberto Carlos Lópezz Moralesss",
    "patient_id": 9,
    "diagnose_name": "qwrqwrqwrwqr",
    "diagnose_code": "HOLAAAAA",
    "diagnose_id": 2,
    "diagnosis_date": "2024-04-16",
    "symptoms": "Dolor de cabeza, fiebre, malestar general",
    "treatment": "Reposo, paracetamol cada 8 horas",
    "notes": "Paciente presenta síntomas gripales",
    "status": "active",
    "created_at": "2025-09-26T18:16:26.938711Z",
    "updated_at": "2025-09-26T18:27:31.523125Z",
    "message": "Historial médico actualizado exitosamente"
}
```

---------------------------------------------------------------------------------------------------------------------------

**Eliminar Historial Medico:**
- **Método:** DELETE
- **URL:** `http://127.0.0.1:8000/api/patients/medical-records/1/`
- **Auth:** Basic Auth
  - Crear usuario con 'python manage.py createsuperuser' desde el codigo fuente.
- **Headers:**
  ```
  Content-Type: application/json
  ```
- **Body (raw JSON):**
```json
**vacio**
```
**Respuesta Exitosa:**
```json
{
    "detail": "Historial médico eliminado correctamente."
}
```

---------------------------------------------------------------------------------------------------------------------------

**Ver Historial Medico Especifico:**
- **Método:** GET
- **URL:** `http://127.0.0.1:8000/api/patients/medical-records/id/`
- **Auth:** Basic Auth
  - Crear usuario con 'python manage.py createsuperuser' desde el codigo fuente.
- **Headers:**
  ```
  Content-Type: application/json
  ```
- **Body (raw JSON):**
```json
**vacio**
```
**Respuesta Exitosa:**
```json
{
    "id": 2,
    "patient_name": "Roberto Carlos Lópezz Moralesss",
    "patient_id": 9,
    "diagnose_name": "qwrqwrqwrwqr",
    "diagnose_code": "HOLAAAAA",
    "diagnose_id": 2,
    "diagnosis_date": "2024-02-15",
    "symptoms": "Dolor de cabeza, fiebre, malestar general",
    "treatment": "Reposo, paracetamol cada 8 horas",
    "notes": "Paciente presenta síntomas gripales",
    "status": "active",
    "created_at": "2025-09-26T18:04:01.604883Z",
    "updated_at": "2025-09-26T18:04:01.604901Z"
}
```

---------------------------------------------------------------------------------------------------------------------------

**Ver Historial Medico de un Paciente Especifico:**
- **Método:** GET
- **URL:** `http://127.0.0.1:8000/api/patients/patients/id/medical-history/`
- **Auth:** Basic Auth
  - Crear usuario con 'python manage.py createsuperuser' desde el codigo fuente.
- **Headers:**
  ```
  Content-Type: application/json
  ```
- **Body (raw JSON):**
```json
**vacio**
```
**Respuesta Exitosa:**
```json
{
    "count": 2,
    "num_pages": 1,
    "current_page": 1,
    "results": [
        {
            "id": 3,
            "patient_name": "Roberto Carlos Lópezz Moralesss",
            "diagnose_name": "qwrqwrqwrwqr",
            "diagnose_code": "HOLAAAAA",
            "diagnosis_date": "2024-03-15",
            "symptoms": "Dolorrr de cabeza, fiebre, malestar general",
            "treatment": "Reposo, paracetamol cada 8 horas",
            "notes": "Paciente presenta síntomas gripales",
            "status": "active",
            "created_at": "2025-09-26T18:06:01.778142Z"
        },
        {
            "id": 2,
            "patient_name": "Roberto Carlos Lópezz Moralesss",
            "diagnose_name": "qwrqwrqwrwqr",
            "diagnose_code": "HOLAAAAA",
            "diagnosis_date": "2024-02-15",
            "symptoms": "Dolor de cabeza, fiebre, malestar general",
            "treatment": "Reposo, paracetamol cada 8 horas",
            "notes": "Paciente presenta síntomas gripales",
            "status": "active",
            "created_at": "2025-09-26T18:04:01.604883Z"
        }
    ]
}
```

---------------------------------------------------------------------------------------------------------------------------

## 👨‍⚕️ Módulo 4: Terapeutas (`/api/therapists/`)

### Terapeutas

| Método     | Endpoint                                                | Descripción                       | Autenticación |
|------------|---------------------------------------------------------|-----------------------------------|---------------|
| **GET**    | `/api/therapists/therapists/`                           | Listar Terapeuta                  |   Requerida   |
| **POST**   | `/api/therapists/therapists/`                           | Crear Terapeuta                   |   Requerida   |
| **PUT**    | `/api/therapists/therapists{id}/`                       | Editar Terapeuta                  |   Requerida   |
| **DELETE** | `/api/therapists/therapists/{id}/`                      | Eliminar Terapeuta                |   Requerida   |
| **GET**    | `/api/therapists/therapists/{id}/`                      | Ver Terapeuta Específico          |   Requerida   |
| **GET**    | `/api/therapists/therapists/?active=false`              | Ver Terapeutas Inactivos          |   Requerida   |
| **GET**    | `/api/therapists/therapists/?active=true`               | Ver Terapeutas Activos            |   Requerida   |
| **POST**   | `/api/therapists/therapists/{id}/restore/`              | Restaurar Terapeuta               |   Requerida   |
| **GET**    | `/api/therapists/therapists/{id}/upload_photo/`         | Subir Foto de Terapeuta           |   Requerida   |
| **PUT**    | `/api/therapists/therapists/{id}/upload_photo/`         | Actualizar Foto de Terapeuta      |   Requerida   |
| **DELETE** | `/api/therapists/therapists/{id}/upload_photo/`         | Eliminar Foto de Terapeuta        |   Requerida   |
---------------------------------------------------------------------------------------------------------------------------|

#### Ejemplos de Terapeutas

**Crear Terapeuta:**
- **Método:** POST
- **URL:** `http://localhost:8000/api/therapists/therapists/`
- **Auth:** Basic Auth
  - Crear usuario con 'python manage.py createsuperuser' desde el codigo fuente.
- **Headers:**
  ```
  Content-Type: application/json
  ```
- **Body (raw JSON):**
```json
{
    "document_type_id": 4,
    "document_number": "12345000",
    "last_name_paternal": "Pérez",
    "last_name_maternal": "García",
    "first_name": "Juan Carlos",
    "birth_date": "1990-05-15T00:00:00Z",
    "gender": "M",
    "personal_reference": "REF123",
    "is_active": true,
    "phone": "987654321",
    "email": "juan@gmail.com",
    "region_id": 1,
    "province_id": 1,
    "district_id": 1,
    "address": "Av. Principal 123, Lima"
}
```
**Respuesta Exitosa:**
```json
{
    "id": 4,
    "document_type": {
        "id": 4,
        "name": "Carne de Extranjeria",
        "description": "Carne de Extranjeria",
        "created_at": "2025-09-25T14:58:39.072486Z",
        "updated_at": "2025-09-25T14:58:39.072514Z"
    },
    "document_type_name": "Carne de Extranjeria",
    "document_number": "12345000",
    "last_name_paternal": "Pérez",
    "last_name_maternal": "García",
    "first_name": "Juan Carlos",
    "full_name": "Juan Carlos Pérez García",
    "birth_date": "1990-05-15T00:00:00Z",
    "gender": "M",
    "personal_reference": "REF123",
    "is_active": true,
    "phone": "987654321",
    "email": "juan@gmail.com",
    "region": {
        "id": 1,
        "name": "Amazonas",
        "country": 180,
        "created_at": "2025-09-24T21:27:17.604182Z",
        "updated_at": "2025-09-24T21:27:17.604198Z",
        "deleted_at": null
    },
    "region_name": "Amazonas",
    "province": {
        "id": 1,
        "name": "Chachapoyas",
        "region": 1,
        "region_name": "Amazonas",
        "created_at": "2025-09-24T21:27:17.714490Z",
        "updated_at": "2025-09-24T21:27:17.714508Z",
        "deleted_at": null
    },
    "province_name": "Chachapoyas",
    "district": {
        "id": 1,
        "name": "Chachapoyas",
        "province": 1,
        "province_name": "Chachapoyas",
        "region_name": "Amazonas",
        "created_at": "2025-09-24T21:27:17.965328Z",
        "updated_at": "2025-09-24T21:27:17.965349Z",
        "deleted_at": null
    },
    "district_name": "Chachapoyas",
    "address": "Av. Principal 123, Lima",
    "profile_picture": null,
    "created_at": "2025-09-26T19:08:46.485662Z",
    "updated_at": "2025-09-26T19:08:46.485670Z",
    "deleted_at": null
}
```

---------------------------------------------------------------------------------------------------------------------------

**Listar Terapeutas:**
- **Método:** GET
- **URL:** `http://localhost:8000/api/therapists/therapists/`
- **Auth:** Basic Auth
  - Crear usuario con 'python manage.py createsuperuser' desde el codigo fuente.
- **Headers:**
  ```
  Content-Type: application/json
  ```
- **Body (raw JSON):**
  ```json
  **vacio**
  ```
**Respuesta Exitosa:**
```json
{
    "count": 4,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "document_type": {
                "id": 4,
                "name": "Carne de Extranjeria",
                "description": "Carne de Extranjeria",
                "created_at": "2025-09-25T14:58:39.072486Z",
                "updated_at": "2025-09-25T14:58:39.072514Z"
            },
            "document_type_name": "Carne de Extranjeria",
            "document_number": "87654321",
            "last_name_paternal": "Rodríguez",
            "last_name_maternal": "Martínez",
            "first_name": "Carlos",
            "full_name": "Carlos Rodríguez Martínez",
            "birth_date": "1988-07-15T00:00:00Z",
            "gender": "M",
            "personal_reference": null,
            "is_active": true,
            "phone": "888888888",
            "email": "carlos@gmail.com",
            "region": {
                "id": 1,
                "name": "Amazonas",
                "country": 180,
                "created_at": "2025-09-24T21:27:17.604182Z",
                "updated_at": "2025-09-24T21:27:17.604198Z",
                "deleted_at": null
            },
            "region_name": "Amazonas",
            "province": {
                "id": 1,
                "name": "Chachapoyas",
                "region": 1,
                "region_name": "Amazonas",
                "created_at": "2025-09-24T21:27:17.714490Z",
                "updated_at": "2025-09-24T21:27:17.714508Z",
                "deleted_at": null
            },
            "province_name": "Chachapoyas",
            "district": {
                "id": 1,
                "name": "Chachapoyas",
                "province": 1,
                "province_name": "Chachapoyas",
                "region_name": "Amazonas",
                "created_at": "2025-09-24T21:27:17.965328Z",
                "updated_at": "2025-09-24T21:27:17.965349Z",
                "deleted_at": null
            },
            "district_name": "Chachapoyas",
            "address": "Calle Principal 456",
            "profile_picture": null,
            "created_at": "2025-09-25T18:41:55.078705Z",
            "updated_at": "2025-09-25T18:41:55.078717Z",
            "deleted_at": null
        },
        {
            "id": 3,
            "document_type": {
                "id": 4,
                "name": "Carne de Extranjeria",
                "description": "Carne de Extranjeria",
                "created_at": "2025-09-25T14:58:39.072486Z",
                "updated_at": "2025-09-25T14:58:39.072514Z"
            },
            "document_type_name": "Carne de Extranjeria",
            "document_number": "12345612",
            "last_name_paternal": "Pérez",
            "last_name_maternal": "García",
            "first_name": "Juan Carlos",
            "full_name": "Juan Carlos Pérez García",
            "birth_date": "1990-05-15T00:00:00Z",
            "gender": "M",
            "personal_reference": "REF123",
            "is_active": true,
            "phone": "987654321",
            "email": "juancarlssssosss@gmail.com",
            "region": {
                "id": 1,
                "name": "Amazonas",
                "country": 180,
                "created_at": "2025-09-24T21:27:17.604182Z",
                "updated_at": "2025-09-24T21:27:17.604198Z",
                "deleted_at": null
            },
            "region_name": "Amazonas",
            "province": {
                "id": 1,
                "name": "Chachapoyas",
                "region": 1,
                "region_name": "Amazonas",
                "created_at": "2025-09-24T21:27:17.714490Z",
                "updated_at": "2025-09-24T21:27:17.714508Z",
                "deleted_at": null
            },
            "province_name": "Chachapoyas",
            "district": {
                "id": 1,
                "name": "Chachapoyas",
                "province": 1,
                "province_name": "Chachapoyas",
                "region_name": "Amazonas",
                "created_at": "2025-09-24T21:27:17.965328Z",
                "updated_at": "2025-09-24T21:27:17.965349Z",
                "deleted_at": null
            },
            "district_name": "Chachapoyas",
            "address": "Av. Principal 123, Lima",
            "profile_picture": null,
            "created_at": "2025-09-26T19:03:11.002796Z",
            "updated_at": "2025-09-26T19:03:11.002803Z",
            "deleted_at": null
        },
        {
            "id": 4,
            "document_type": {
                "id": 4,
                "name": "Carne de Extranjeria",
                "description": "Carne de Extranjeria",
                "created_at": "2025-09-25T14:58:39.072486Z",
                "updated_at": "2025-09-25T14:58:39.072514Z"
            },
            "document_type_name": "Carne de Extranjeria",
            "document_number": "12345000",
            "last_name_paternal": "Pérez",
            "last_name_maternal": "García",
            "first_name": "Juan Carlos",
            "full_name": "Juan Carlos Pérez García",
            "birth_date": "1990-05-15T00:00:00Z",
            "gender": "M",
            "personal_reference": "REF123",
            "is_active": true,
            "phone": "987654321",
            "email": "juan@gmail.com",
            "region": {
                "id": 1,
                "name": "Amazonas",
                "country": 180,
                "created_at": "2025-09-24T21:27:17.604182Z",
                "updated_at": "2025-09-24T21:27:17.604198Z",
                "deleted_at": null
            },
            "region_name": "Amazonas",
            "province": {
                "id": 1,
                "name": "Chachapoyas",
                "region": 1,
                "region_name": "Amazonas",
                "created_at": "2025-09-24T21:27:17.714490Z",
                "updated_at": "2025-09-24T21:27:17.714508Z",
                "deleted_at": null
            },
            "province_name": "Chachapoyas",
            "district": {
                "id": 1,
                "name": "Chachapoyas",
                "province": 1,
                "province_name": "Chachapoyas",
                "region_name": "Amazonas",
                "created_at": "2025-09-24T21:27:17.965328Z",
                "updated_at": "2025-09-24T21:27:17.965349Z",
                "deleted_at": null
            },
            "district_name": "Chachapoyas",
            "address": "Av. Principal 123, Lima",
            "profile_picture": null,
            "created_at": "2025-09-26T19:08:46.485662Z",
            "updated_at": "2025-09-26T19:08:46.485670Z",
            "deleted_at": null
        },
        {
            "id": 2,
            "document_type": {
                "id": 4,
                "name": "Carne de Extranjeria",
                "description": "Carne de Extranjeria",
                "created_at": "2025-09-25T14:58:39.072486Z",
                "updated_at": "2025-09-25T14:58:39.072514Z"
            },
            "document_type_name": "Carne de Extranjeria",
            "document_number": "12345679",
            "last_name_paternal": "Pérez",
            "last_name_maternal": "García",
            "first_name": "Juannn Carlosss",
            "full_name": "Juannn Carlosss Pérez García",
            "birth_date": "1990-05-15T00:00:00Z",
            "gender": "M",
            "personal_reference": "REF123",
            "is_active": true,
            "phone": "987654320",
            "email": "juancarlosss@gmail.com",
            "region": {
                "id": 1,
                "name": "Amazonas",
                "country": 180,
                "created_at": "2025-09-24T21:27:17.604182Z",
                "updated_at": "2025-09-24T21:27:17.604198Z",
                "deleted_at": null
            },
            "region_name": "Amazonas",
            "province": {
                "id": 1,
                "name": "Chachapoyas",
                "region": 1,
                "region_name": "Amazonas",
                "created_at": "2025-09-24T21:27:17.714490Z",
                "updated_at": "2025-09-24T21:27:17.714508Z",
                "deleted_at": null
            },
            "province_name": "Chachapoyas",
            "district": {
                "id": 1,
                "name": "Chachapoyas",
                "province": 1,
                "province_name": "Chachapoyas",
                "region_name": "Amazonas",
                "created_at": "2025-09-24T21:27:17.965328Z",
                "updated_at": "2025-09-24T21:27:17.965349Z",
                "deleted_at": null
            },
            "district_name": "Chachapoyas",
            "address": "Av. Principal 1223, Lima",
            "profile_picture": null,
            "created_at": "2025-09-26T18:59:49.726484Z",
            "updated_at": "2025-09-26T19:00:22.471933Z",
            "deleted_at": null
        }
    ]
}
```

---------------------------------------------------------------------------------------------------------------------------

**Editar Terapeuta:**
- **Método:** PUT
- **URL:** `http://localhost:8000/api/therapists/therapists/`
- **Auth:** Basic Auth
  - Crear usuario con 'python manage.py createsuperuser' desde el codigo fuente.
- **Headers:**
  ```
  Content-Type: application/json
  ```
- **Body (raw JSON):**
```json
{
    "document_number": "12345020",
    "last_name_paternal": "Pérez",
    "last_name_maternal": "García",
    "first_name": "Juan Carlos",
    "birth_date": "1990-05-15T00:00:00Z",
    "gender": "M",
    "personal_reference": "REF123",
    "is_active": true,
    "phone": "987654321",
    "email": "juans@gmail.com",
    "region_id": 1,
    "province_id": 1,
    "district_id": 1,
    "address": "Av. Principal 123, Lima"
}
```
**Respuesta Exitosa:**
```json
{
    "id": 1,
    "document_type": {
        "id": 4,
        "name": "Carne de Extranjeria",
        "description": "Carne de Extranjeria",
        "created_at": "2025-09-25T14:58:39.072486Z",
        "updated_at": "2025-09-25T14:58:39.072514Z"
    },
    "document_type_name": "Carne de Extranjeria",
    "document_number": "12345020",
    "last_name_paternal": "Pérez",
    "last_name_maternal": "García",
    "first_name": "Juan Carlos",
    "full_name": "Juan Carlos Pérez García",
    "birth_date": "1990-05-15T00:00:00Z",
    "gender": "M",
    "personal_reference": "REF123",
    "is_active": true,
    "phone": "987654321",
    "email": "juans@gmail.com",
    "region": {
        "id": 1,
        "name": "Amazonas",
        "country": 180,
        "created_at": "2025-09-24T21:27:17.604182Z",
        "updated_at": "2025-09-24T21:27:17.604198Z",
        "deleted_at": null
    },
    "region_name": "Amazonas",
    "province": {
        "id": 1,
        "name": "Chachapoyas",
        "region": 1,
        "region_name": "Amazonas",
        "created_at": "2025-09-24T21:27:17.714490Z",
        "updated_at": "2025-09-24T21:27:17.714508Z",
        "deleted_at": null
    },
    "province_name": "Chachapoyas",
    "district": {
        "id": 1,
        "name": "Chachapoyas",
        "province": 1,
        "province_name": "Chachapoyas",
        "region_name": "Amazonas",
        "created_at": "2025-09-24T21:27:17.965328Z",
        "updated_at": "2025-09-24T21:27:17.965349Z",
        "deleted_at": null
    },
    "district_name": "Chachapoyas",
    "address": "Av. Principal 123, Lima",
    "profile_picture": null,
    "created_at": "2025-09-25T18:41:55.078705Z",
    "updated_at": "2025-09-26T19:11:27.158375Z",
    "deleted_at": null
}
```

---------------------------------------------------------------------------------------------------------------------------

**Eliminar Terapeuta:**
- **Método:** DELETE
- **URL:** `http://localhost:8000/api/therapists/therapists/id/`
- **Auth:** Basic Auth
  - Crear usuario con 'python manage.py createsuperuser' desde el codigo fuente.
- **Headers:**
  ```
  Content-Type: application/json
  ```
- **Body (raw JSON):**
```json
**vacio**
```
**Respuesta Exitosa:**
```json
{
    "message": "Terapeuta marcado como inactivo exitosamente",
    "id": 1,
    "name": "Juan Carlos Pérez García",
    "deleted_at": "2025-09-26T19:13:12.780839+00:00"
}
```

---------------------------------------------------------------------------------------------------------------------------

**Ver Terapeuta Especifico:**
- **Método:** GET
- **URL:** `http://localhost:8000/api/therapists/therapists/id/`
- **Auth:** Basic Auth
  - Crear usuario con 'python manage.py createsuperuser' desde el codigo fuente.
- **Headers:**
  ```
  Content-Type: application/json
  ```
- **Body (raw JSON):**
```json
**vacio**
```
**Respuesta Exitosa:**
```json
{
    "id": 2,
    "document_type": {
        "id": 4,
        "name": "Carne de Extranjeria",
        "description": "Carne de Extranjeria",
        "created_at": "2025-09-25T14:58:39.072486Z",
        "updated_at": "2025-09-25T14:58:39.072514Z"
    },
    "document_type_name": "Carne de Extranjeria",
    "document_number": "12345679",
    "last_name_paternal": "Pérez",
    "last_name_maternal": "García",
    "first_name": "Juannn Carlosss",
    "full_name": "Juannn Carlosss Pérez García",
    "birth_date": "1990-05-15T00:00:00Z",
    "gender": "M",
    "personal_reference": "REF123",
    "is_active": true,
    "phone": "987654320",
    "email": "juancarlosss@gmail.com",
    "region": {
        "id": 1,
        "name": "Amazonas",
        "country": 180,
        "created_at": "2025-09-24T21:27:17.604182Z",
        "updated_at": "2025-09-24T21:27:17.604198Z",
        "deleted_at": null
    },
    "region_name": "Amazonas",
    "province": {
        "id": 1,
        "name": "Chachapoyas",
        "region": 1,
        "region_name": "Amazonas",
        "created_at": "2025-09-24T21:27:17.714490Z",
        "updated_at": "2025-09-24T21:27:17.714508Z",
        "deleted_at": null
    },
    "province_name": "Chachapoyas",
    "district": {
        "id": 1,
        "name": "Chachapoyas",
        "province": 1,
        "province_name": "Chachapoyas",
        "region_name": "Amazonas",
        "created_at": "2025-09-24T21:27:17.965328Z",
        "updated_at": "2025-09-24T21:27:17.965349Z",
        "deleted_at": null
    },
    "district_name": "Chachapoyas",
    "address": "Av. Principal 1223, Lima",
    "profile_picture": null,
    "created_at": "2025-09-26T18:59:49.726484Z",
    "updated_at": "2025-09-26T19:00:22.471933Z",
    "deleted_at": null
}
```

---------------------------------------------------------------------------------------------------------------------------

**Ver Terapeutas Inactivos:**
- **Método:** GET
- **URL:** `http://localhost:8000/api/therapists/therapists/?active=false`
- **Auth:** Basic Auth
  - Crear usuario con 'python manage.py createsuperuser' desde el codigo fuente.
- **Headers:**
  ```
  Content-Type: application/json
  ```
- **Body (raw JSON):**
```json
**vacio**
```
**Respuesta Exitosa:**
```json
{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "document_type": {
                "id": 4,
                "name": "Carne de Extranjeria",
                "description": "Carne de Extranjeria",
                "created_at": "2025-09-25T14:58:39.072486Z",
                "updated_at": "2025-09-25T14:58:39.072514Z"
            },
            "document_type_name": "Carne de Extranjeria",
            "document_number": "12345020",
            "last_name_paternal": "Pérez",
            "last_name_maternal": "García",
            "first_name": "Juan Carlos",
            "full_name": "Juan Carlos Pérez García",
            "birth_date": "1990-05-15T00:00:00Z",
            "gender": "M",
            "personal_reference": "REF123",
            "is_active": false,
            "phone": "987654321",
            "email": "juans@gmail.com",
            "region": {
                "id": 1,
                "name": "Amazonas",
                "country": 180,
                "created_at": "2025-09-24T21:27:17.604182Z",
                "updated_at": "2025-09-24T21:27:17.604198Z",
                "deleted_at": null
            },
            "region_name": "Amazonas",
            "province": {
                "id": 1,
                "name": "Chachapoyas",
                "region": 1,
                "region_name": "Amazonas",
                "created_at": "2025-09-24T21:27:17.714490Z",
                "updated_at": "2025-09-24T21:27:17.714508Z",
                "deleted_at": null
            },
            "province_name": "Chachapoyas",
            "district": {
                "id": 1,
                "name": "Chachapoyas",
                "province": 1,
                "province_name": "Chachapoyas",
                "region_name": "Amazonas",
                "created_at": "2025-09-24T21:27:17.965328Z",
                "updated_at": "2025-09-24T21:27:17.965349Z",
                "deleted_at": null
            },
            "district_name": "Chachapoyas",
            "address": "Av. Principal 123, Lima",
            "profile_picture": null,
            "created_at": "2025-09-25T18:41:55.078705Z",
            "updated_at": "2025-09-26T19:11:27.158375Z",
            "deleted_at": "2025-09-26T19:13:12.780839Z"
        }
    ]
}
```

---------------------------------------------------------------------------------------------------------------------------

**Restaurar Terapeuta:**
- **Método:** POST
- **URL:** `http://localhost:8000/api/therapists/therapists/id/restore/`
- **Auth:** Basic Auth
  - Crear usuario con 'python manage.py createsuperuser' desde el codigo fuente.
- **Headers:**
  ```
  Content-Type: application/json
  ```
- **Body (raw JSON):**
```json
**vacio**
```
**Respuesta Exitosa:**
```json
{
    "message": "Terapeuta restaurado exitosamente",
    "id": 1,
    "name": "Juan Carlos Pérez García",
    "is_active": true,
    "restored_at": "2025-09-26T19:11:27.158375+00:00"
}
```

---------------------------------------------------------------------------------------------------------------------------

**Ver Terapeutas Activos:**
- **Método:** GET
- **URL:** `http://localhost:8000/api/therapists/therapists/?active=true`
- **Auth:** Basic Auth
  - Crear usuario con 'python manage.py createsuperuser' desde el codigo fuente.
- **Headers:**
  ```
  Content-Type: application/json
  ```
- **Body (raw JSON):**
```json
**vacio**
```
**Respuesta Exitosa:**
```json
{
    "count": 3,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 3,
            "document_type": {
                "id": 4,
                "name": "Carne de Extranjeria",
                "description": "Carne de Extranjeria",
                "created_at": "2025-09-25T14:58:39.072486Z",
                "updated_at": "2025-09-25T14:58:39.072514Z"
            },
            "document_type_name": "Carne de Extranjeria",
            "document_number": "12345612",
            "last_name_paternal": "Pérez",
            "last_name_maternal": "García",
            "first_name": "Juan Carlos",
            "full_name": "Juan Carlos Pérez García",
            "birth_date": "1990-05-15T00:00:00Z",
            "gender": "M",
            "personal_reference": "REF123",
            "is_active": true,
            "phone": "987654321",
            "email": "juancarlssssosss@gmail.com",
            "region": {
                "id": 1,
                "name": "Amazonas",
                "country": 180,
                "created_at": "2025-09-24T21:27:17.604182Z",
                "updated_at": "2025-09-24T21:27:17.604198Z",
                "deleted_at": null
            },
            "region_name": "Amazonas",
            "province": {
                "id": 1,
                "name": "Chachapoyas",
                "region": 1,
                "region_name": "Amazonas",
                "created_at": "2025-09-24T21:27:17.714490Z",
                "updated_at": "2025-09-24T21:27:17.714508Z",
                "deleted_at": null
            },
            "province_name": "Chachapoyas",
            "district": {
                "id": 1,
                "name": "Chachapoyas",
                "province": 1,
                "province_name": "Chachapoyas",
                "region_name": "Amazonas",
                "created_at": "2025-09-24T21:27:17.965328Z",
                "updated_at": "2025-09-24T21:27:17.965349Z",
                "deleted_at": null
            },
            "district_name": "Chachapoyas",
            "address": "Av. Principal 123, Lima",
            "profile_picture": null,
            "created_at": "2025-09-26T19:03:11.002796Z",
            "updated_at": "2025-09-26T19:03:11.002803Z",
            "deleted_at": null
        },
        {
            "id": 4,
            "document_type": {
                "id": 4,
                "name": "Carne de Extranjeria",
                "description": "Carne de Extranjeria",
                "created_at": "2025-09-25T14:58:39.072486Z",
                "updated_at": "2025-09-25T14:58:39.072514Z"
            },
            "document_type_name": "Carne de Extranjeria",
            "document_number": "12345000",
            "last_name_paternal": "Pérez",
            "last_name_maternal": "García",
            "first_name": "Juan Carlos",
            "full_name": "Juan Carlos Pérez García",
            "birth_date": "1990-05-15T00:00:00Z",
            "gender": "M",
            "personal_reference": "REF123",
            "is_active": true,
            "phone": "987654321",
            "email": "juan@gmail.com",
            "region": {
                "id": 1,
                "name": "Amazonas",
                "country": 180,
                "created_at": "2025-09-24T21:27:17.604182Z",
                "updated_at": "2025-09-24T21:27:17.604198Z",
                "deleted_at": null
            },
            "region_name": "Amazonas",
            "province": {
                "id": 1,
                "name": "Chachapoyas",
                "region": 1,
                "region_name": "Amazonas",
                "created_at": "2025-09-24T21:27:17.714490Z",
                "updated_at": "2025-09-24T21:27:17.714508Z",
                "deleted_at": null
            },
            "province_name": "Chachapoyas",
            "district": {
                "id": 1,
                "name": "Chachapoyas",
                "province": 1,
                "province_name": "Chachapoyas",
                "region_name": "Amazonas",
                "created_at": "2025-09-24T21:27:17.965328Z",
                "updated_at": "2025-09-24T21:27:17.965349Z",
                "deleted_at": null
            },
            "district_name": "Chachapoyas",
            "address": "Av. Principal 123, Lima",
            "profile_picture": null,
            "created_at": "2025-09-26T19:08:46.485662Z",
            "updated_at": "2025-09-26T19:08:46.485670Z",
            "deleted_at": null
        },
        {
            "id": 2,
            "document_type": {
                "id": 4,
                "name": "Carne de Extranjeria",
                "description": "Carne de Extranjeria",
                "created_at": "2025-09-25T14:58:39.072486Z",
                "updated_at": "2025-09-25T14:58:39.072514Z"
            },
            "document_type_name": "Carne de Extranjeria",
            "document_number": "12345679",
            "last_name_paternal": "Pérez",
            "last_name_maternal": "García",
            "first_name": "Juannn Carlosss",
            "full_name": "Juannn Carlosss Pérez García",
            "birth_date": "1990-05-15T00:00:00Z",
            "gender": "M",
            "personal_reference": "REF123",
            "is_active": true,
            "phone": "987654320",
            "email": "juancarlosss@gmail.com",
            "region": {
                "id": 1,
                "name": "Amazonas",
                "country": 180,
                "created_at": "2025-09-24T21:27:17.604182Z",
                "updated_at": "2025-09-24T21:27:17.604198Z",
                "deleted_at": null
            },
            "region_name": "Amazonas",
            "province": {
                "id": 1,
                "name": "Chachapoyas",
                "region": 1,
                "region_name": "Amazonas",
                "created_at": "2025-09-24T21:27:17.714490Z",
                "updated_at": "2025-09-24T21:27:17.714508Z",
                "deleted_at": null
            },
            "province_name": "Chachapoyas",
            "district": {
                "id": 1,
                "name": "Chachapoyas",
                "province": 1,
                "province_name": "Chachapoyas",
                "region_name": "Amazonas",
                "created_at": "2025-09-24T21:27:17.965328Z",
                "updated_at": "2025-09-24T21:27:17.965349Z",
                "deleted_at": null
            },
            "district_name": "Chachapoyas",
            "address": "Av. Principal 1223, Lima",
            "profile_picture": null,
            "created_at": "2025-09-26T18:59:49.726484Z",
            "updated_at": "2025-09-26T19:00:22.471933Z",
            "deleted_at": null
        }
    ]
}
```

---------------------------------------------------------------------------------------------------------------------------

**Subir Foto de Terapeuta:**
- **Método:** POST
- **URL:** `http://localhost:8000/api/therapists/therapists/id/upload_photo/`
- **Auth:** Basic Auth
  - Crear usuario con 'python manage.py createsuperuser' desde el codigo fuente.
- **Headers:**
  ```
  Content-Type: application/json
  ```
- **Body (form-data):**
```json
  - Key: profile_picture --- File
  - Value: Elige la foto desdee tu computadora
```
**Respuesta Exitosa:**
```json
{
    "message": "Foto de perfil subida exitosamente",
    "id": 1,
    "name": "Juan Carlos Pérez García",
    "profile_picture_url": "/media/profile_pics/Captura_de_pantalla_2025-04-17_184057_pz9loI0.png",
    "uploaded_at": "2025-09-26T19:11:27.158375+00:00"
}
```

---------------------------------------------------------------------------------------------------------------------------

**Actualizar Foto de Terapeuta:**
- **Método:** PUT
- **URL:** `http://localhost:8000/api/therapists/therapists/id/upload_photo/`
- **Auth:** Basic Auth
  - Crear usuario con 'python manage.py createsuperuser' desde el codigo fuente.
- **Headers:**
  ```
  Content-Type: application/json
  ```
- **Body (form-data):**
```json
  - Key: profile_picture --- File
  - Value: Elige la foto desdee tu computadora
```
**Respuesta Exitosa:**
```json
{
    "message": "Foto de perfil actualizada exitosamente",
    "id": 1,
    "name": "Juan Carlos Pérez García",
    "profile_picture_url": "/media/profile_pics/Christhoper_Sosa_4_-_BK_4_3.png",
    "updated_at": "2025-09-26T19:11:27.158375+00:00"
}
```

---------------------------------------------------------------------------------------------------------------------------

**Eliminar Foto de Terapeuta:**
- **Método:** DELETE
- **URL:** `http://localhost:8000/api/therapists/therapists/id/upload_photo/`
- **Auth:** Basic Auth
  - Crear usuario con 'python manage.py createsuperuser' desde el codigo fuente.
- **Headers:**
  ```
  Content-Type: application/json
  ```
- **Body (form-data):**
```json
**vacio**
```
**Respuesta Exitosa:**
```json
{
    "message": "Foto de perfil eliminada exitosamente",
    "id": 1,
    "name": "Juan Carlos Pérez García",
    "profile_picture_url": null,
    "deleted_at": "2025-09-26T19:11:27.158375+00:00"
}
```

---------------------------------------------------------------------------------------------------------------------------

## 📅 Módulo 5: Citas y Estados (`/api/appointments/`)

### Estados de Citas

| Método     | Endpoint                                                       | Descripción                                  | Autenticación |
|------------|----------------------------------------------------------------|----------------------------------------------|---------------|
| **GET**    | `/api/appointments/appointment-statuses/`                      | Listar Estados de Citas                      |   Requerida   |
| **POST**   | `/api/appointments/appointment-statuses/`                      | Crear Estado de Cita                         |   Requerida   |
| **PUT**    | `/api/appointments/appointment-statuses/{id}/`                 | Editar Estado de Cita                        |   Requerida   |
| **DELETE** | `/api/appointments/appointment-statuses/{id}/`                 | Eliminar Estado de Cita                      |   Requerida   |
| **POST**   | `/api/appointments/appointment-statuses/{id}/restore/`         | Restaurar Estado de Cita                     |   Requerida   |
| **GET**    | `/api/appointments/appointment-statuses/{id}/`                 | Ver Estado de Cita Específico                |   Requerida   |
| **GET**    | `/api/appointments/appointment-statuses/all_including_deleted/`| Listar Estados de Citas incluyendo Eliminados|   Requerida   |
---------------------------------------------------------------------------------------------------------------------------------------------|
| **GET**    | `/api/appointments/appointments/`                              | Listar Citas                                 |   Requerida   |
| **POST**   | `/api/appointments/appointments/`                              | Crear Cita                                   |   Requerida   |
| **PUT**    | `/api/appointments/appointments/{id}/`                         | Editar Cita                                  |   Requerida   |
| **DELETE** | `/api/appointments/appointments/{id}/`                         | Eliminar Cita                                |   Requerida   |
| **GET**    | `/api/appointments/appointments/{id}/`                         | Ver Cita Específico                          |   Requerida   |
| **GET**    | `/api/appointments/appointments/completed/`                    | Listar Citas Completadas                     |   Requerida   |
| **GET**    | `/api/appointments/appointments/pending/`                      | Listar Citas Pendientes                      |   Requerida   |
| **GET**    | `/api/appointments/appointments/by_date_range/`                | Listar Citas por Rango de Fechas             |   Requerida   |
---------------------------------------------------------------------------------------------------------------------------------------------|
| **GET**    | `/api/appointments/tickets/`                                   | Listar Tickets                               |   Requerida   |
| **GET**    | `/api/appointments/tickets/`                                   | Crear Tickets                                |   Requerida   |
| **PUT**    | `/api/appointments/tickets/{id}/`                              | Editar Ticket                                |   Requerida   |
| **DELETE** | `/api/appointments/tickets/{id}/`                              | Eliminar Ticket                              |   Requerida   |
| **GET**    | `/api/appointments/tickets/{id}/`                              | Ver Ticket Específico                        |   Requerida   |
| **GET**    | `/api/appointments/tickets/paid/`                              | Listar Tickets Pagados                       |   Requerida   |
| **GET**    | `/api/appointments/tickets/pending/`                           | Listar Tickets Pendientes                    |   Requerida   |
| **POST**   | `/api/appointments/tickets/{id}/mark_as_paid/`                 | Marcar Ticket como pagado                    |   Requerida   |
---------------------------------------------------------------------------------------------------------------------------------------------|

#### Ejemplos de Estados de Citas

**Crear Estado de Cita:**
- **Método:** POST
- **URL:** `http://localhost:8000/api/appointments/appointment-statuses/`
- **Auth:** Basic Auth
  - Crear usuario con 'python manage.py createsuperuser' desde el codigo fuente.
- **Headers:**
  ```
  Content-Type: application/json
  ```
- **Body (raw JSON):**
```json
{
    "name": "Completadaa",
    "description": "Cita completada exitosamente"
}
```
**Respuesta Exitosa:**
```json
{
    "id": 3,
    "name": "Completadaa",
    "description": "Cita completada exitosamente",
    "created_at": "2025-09-27T16:19:36.612431Z",
    "updated_at": "2025-09-27T16:19:36.612448Z",
    "deleted_at": null
}
```

---------------------------------------------------------------------------------------------------------------------------

**Listar Estados de Citas:**
- **Método:** GET
- **URL:** `http://localhost:8000/api/appointments/appointment-statuses/`
- **Auth:** Basic Auth
  - Crear usuario con 'python manage.py createsuperuser' desde el codigo fuente.
- **Headers:**
  ```
  Content-Type: application/json
  ```
- **Body (raw JSON):**
```json
**vacio**
```
**Respuesta Exitosa:**
```json
{
    "count": 3,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "name": "Completada",
            "description": "Cita completada exitosamente",
            "created_at": "2025-09-27T16:02:24.072027Z",
            "updated_at": "2025-09-27T16:03:20.134065Z",
            "deleted_at": null
        },
        {
            "id": 2,
            "name": "Completada",
            "description": "Cita completada exitosamente",
            "created_at": "2025-09-27T16:12:09.188743Z",
            "updated_at": "2025-09-27T16:13:49.725918Z",
            "deleted_at": null
        },
        {
            "id": 3,
            "name": "Completadaa",
            "description": "Cita completada exitosamente",
            "created_at": "2025-09-27T16:19:36.612431Z",
            "updated_at": "2025-09-27T16:19:36.612448Z",
            "deleted_at": null
        }
    ]
}
```

---------------------------------------------------------------------------------------------------------------------------

**Editar Estado de Cita:**
- **Método:** PUT
- **URL:** `http://localhost:8000/api/appointments/appointment-statuses/id/`
- **Auth:** Basic Auth
  - Crear usuario con 'python manage.py createsuperuser' desde el codigo fuente.
- **Headers:**
  ```
  Content-Type: application/json
  ```
- **Body (raw JSON):**
```json
{
    "name": "Completadaaaaa",
    "description": "Cita completada exitosamenteeeee"
}
```
**Respuesta Exitosa:**
```json
{
    "id": 3,
    "name": "Completadaaaaa",
    "description": "Cita completada exitosamenteeeee",
    "created_at": "2025-09-27T16:19:36.612431Z",
    "updated_at": "2025-09-27T16:21:30.997663Z",
    "deleted_at": null
}
```

---------------------------------------------------------------------------------------------------------------------------

**Eliminar Estado de Cita:**
- **Método:** DELETE
- **URL:** `http://localhost:8000/api/appointments/appointment-statuses/id/`
- **Auth:** Basic Auth
  - Crear usuario con 'python manage.py createsuperuser' desde el codigo fuente.
- **Headers:**
  ```
  Content-Type: application/json
  ```
- **Body (raw JSON):**
```json
**vacio**
```
**Respuesta Exitosa:**
```json
{
    "message": "Estado 'Completadaaaaa' eliminado correctamente"
}
```

---------------------------------------------------------------------------------------------------------------------------

**Restaurar Estado de Cita:**
- **Método:** POST
- **URL:** `http://localhost:8000/api/appointments/appointment-statuses/id/restore/`
- **Auth:** Basic Auth
  - Crear usuario con 'python manage.py createsuperuser' desde el codigo fuente.
- **Headers:**
  ```
  Content-Type: application/json
  ```
- **Body (raw JSON):**
```json
**vacio**
```
**Respuesta Exitosa:**
```json
{
    "message": "Estado 'Completadaaaaa' restaurado correctamente",
    "data": {
        "id": 3,
        "name": "Completadaaaaa",
        "description": "Cita completada exitosamenteeeee",
        "created_at": "2025-09-27T16:19:36.612431Z",
        "updated_at": "2025-09-27T16:21:30.997663Z",
        "deleted_at": null
    }
}
```

---------------------------------------------------------------------------------------------------------------------------

**Ver Estado de Cita Especifico:**
- **Método:** GET
- **URL:** `http://localhost:8000/api/appointments/appointment-statuses/id/`
- **Auth:** Basic Auth
  - Crear usuario con 'python manage.py createsuperuser' desde el codigo fuente.
- **Headers:**
  ```
  Content-Type: application/json
  ```
- **Body (raw JSON):**
```json
**vacio**
```
**Respuesta Exitosa:**
```json
{
    "id": 3,
    "name": "Completadaaaaa",
    "description": "Cita completada exitosamenteeeee",
    "created_at": "2025-09-27T16:19:36.612431Z",
    "updated_at": "2025-09-27T16:21:30.997663Z",
    "deleted_at": null
}
```

---------------------------------------------------------------------------------------------------------------------------

**Listar Estados de Citas incluyendo Eliminados:**
- **Método:** GET
- **URL:** `http://localhost:8000/api/appointments/appointment-statuses/all_including_deleted/`
- **Auth:** Basic Auth
  - Crear usuario con 'python manage.py createsuperuser' desde el codigo fuente.
- **Headers:**
  ```
  Content-Type: application/json
  ```
- **Body (raw JSON):**
```json
**vacio**
```
**Respuesta Exitosa:**
```json
{
    "message": "Estados obtenidos (incluyendo eliminados)",
    "data": [
        {
            "id": 1,
            "name": "Completada",
            "description": "Cita completada exitosamente",
            "created_at": "2025-09-27T16:02:24.072027Z",
            "updated_at": "2025-09-27T16:03:20.134065Z",
            "deleted_at": null
        },
        {
            "id": 2,
            "name": "Completada",
            "description": "Cita completada exitosamente",
            "created_at": "2025-09-27T16:12:09.188743Z",
            "updated_at": "2025-09-27T16:13:49.725918Z",
            "deleted_at": null
        },
        {
            "id": 3,
            "name": "Completadaaaaa",
            "description": "Cita completada exitosamenteeeee",
            "created_at": "2025-09-27T16:19:36.612431Z",
            "updated_at": "2025-09-27T16:21:30.997663Z",
            "deleted_at": null
        }
    ]
}
```

---------------------------------------------------------------------------------------------------------------------------

**Crear Cita:**
- **Método:** POST
- **URL:** `http://localhost:8000/api/appointments/appointments/`
- **Auth:** Basic Auth
  - Crear usuario con 'python manage.py createsuperuser' desde el codigo fuente.
- **Headers:**
  ```
  Content-Type: application/json
  ```
- **Body (raw JSON):**
```json
{
    "patient": 8,
    "appointment_date": "2025-10-28T10:00:00Z",
    "hour": "10:00:00",
    "ailments": "Dolor de espalda crónico, migrañas ocasionales",
    "diagnosis": "Lumbalgia crónica, cefalea tensional",
    "surgeries": "Ninguna cirugía previa",
    "reflexology_diagnostics": "Puntos sensibles en zona lumbar y cervical",
    "medications": "Ibuprofeno 400mg cada 8 horas",
    "observation": "Paciente presenta tensión muscular en zona cervical",
    "initial_date": "2025-09-28",
    "final_date": "2025-10-05",
    "appointment_type": "Consulta inicial",
    "room": 1,
    "social_benefit": true,
    "payment_type": 2,
    "appointment_status": 2
}
```
**Respuesta Exitosa:**
```json
{
    "message": "Cita creada exitosamente con ticket automático",
    "appointment": {
        "id": 4,
        "history": null,
        "patient": 8,
        "patient_name": "Roberto Carlos Lópezz Moralesss",
        "therapist": null,
        "therapist_name": null,
        "appointment_date": "2025-10-28T10:00:00Z",
        "hour": "10:00:00",
        "ailments": "Dolor de espalda crónico, migrañas ocasionales",
        "diagnosis": "Lumbalgia crónica, cefalea tensional",
        "surgeries": "Ninguna cirugía previa",
        "reflexology_diagnostics": "Puntos sensibles en zona lumbar y cervical",
        "medications": "Ibuprofeno 400mg cada 8 horas",
        "observation": "Paciente presenta tensión muscular en zona cervical",
        "initial_date": "2025-09-28",
        "final_date": "2025-10-05",
        "appointment_type": "Consulta inicial",
        "room": 1,
        "social_benefit": true,
        "payment_detail": null,
        "payment": null,
        "payment_type": 2,
        "payment_type_name": "Tarjeta",
        "payment_status": null,
        "payment_status_name": null,
        "ticket_number": null,
        "appointment_status": 2,
        "is_completed": false,
        "is_pending": true,
        "created_at": "2025-09-27T18:01:19.056447Z",
        "updated_at": "2025-09-27T18:01:19.056455Z",
        "deleted_at": null
    },
    "ticket_number": "TKT-002"
}
```

---------------------------------------------------------------------------------------------------------------------------

**Listar Citas:**
- **Método:** GET
- **URL:** `http://localhost:8000/api/appointments/appointments/`
- **Auth:** Basic Auth
  - Crear usuario con 'python manage.py createsuperuser' desde el codigo fuente.
- **Headers:**
  ```
  Content-Type: application/json
  ```
- **Body (raw JSON):**
```json
**vacio**
```
**Respuesta Exitosa:**
```json
{
    "count": 4,
    "results": [
        {
            "id": 4,
            "history": null,
            "patient": 8,
            "patient_name": "Roberto Carlos Lópezz Moralesss",
            "therapist": null,
            "therapist_name": null,
            "appointment_date": "2025-10-28T10:00:00Z",
            "hour": "10:00:00",
            "ailments": "Dolor de espalda crónico, migrañas ocasionales",
            "diagnosis": "Lumbalgia crónica, cefalea tensional",
            "surgeries": "Ninguna cirugía previa",
            "reflexology_diagnostics": "Puntos sensibles en zona lumbar y cervical",
            "medications": "Ibuprofeno 400mg cada 8 horas",
            "observation": "Paciente presenta tensión muscular en zona cervical",
            "initial_date": "2025-09-28",
            "final_date": "2025-10-05",
            "appointment_type": "Consulta inicial",
            "room": 1,
            "social_benefit": true,
            "payment_detail": null,
            "payment": null,
            "payment_type": 2,
            "payment_type_name": "Tarjeta",
            "payment_status": null,
            "payment_status_name": null,
            "ticket_number": "TKT-002",
            "appointment_status": 2,
            "is_completed": false,
            "is_pending": true,
            "created_at": "2025-09-27T18:01:19.056447Z",
            "updated_at": "2025-09-27T18:01:19.056455Z",
            "deleted_at": null
        },
        {
            "id": 1,
            "history": 10,
            "patient": 9,
            "patient_name": "Roberto Carlos Lópezz Moralesss",
            "therapist": 1,
            "therapist_name": "Juan Carlos Pérez García",
            "appointment_date": "2025-09-28T10:00:00Z",
            "hour": "10:00:00",
            "ailments": "Dolor de espalda crónico, migrañas ocasionales",
            "diagnosis": "Lumbalgia crónica, cefalea tensional",
            "surgeries": "Ninguna cirugía previa",
            "reflexology_diagnostics": "Puntos sensibles en zona lumbar y cervical",
            "medications": "Ibuprofeno 400mg cada 8 horas",
            "observation": "Paciente presenta tensión muscular en zona cervical",
            "initial_date": "2025-09-28",
            "final_date": "2025-10-05",
            "appointment_type": "Consulta inicial",
            "room": 1,
            "social_benefit": true,
            "payment_detail": null,
            "payment": null,
            "payment_type": 2,
            "payment_type_name": "Tarjeta",
            "payment_status": null,
            "payment_status_name": null,
            "ticket_number": null,
            "appointment_status": 2,
            "is_completed": false,
            "is_pending": true,
            "created_at": "2025-09-27T17:50:53.452436Z",
            "updated_at": "2025-09-27T17:50:53.452446Z",
            "deleted_at": null
        },
        {
            "id": 2,
            "history": 10,
            "patient": 9,
            "patient_name": "Roberto Carlos Lópezz Moralesss",
            "therapist": 1,
            "therapist_name": "Juan Carlos Pérez García",
            "appointment_date": "2025-09-28T10:00:00Z",
            "hour": "10:00:00",
            "ailments": "Dolor de espalda crónico, migrañas ocasionales",
            "diagnosis": "Lumbalgia crónica, cefalea tensional",
            "surgeries": "Ninguna cirugía previa",
            "reflexology_diagnostics": "Puntos sensibles en zona lumbar y cervical",
            "medications": "Ibuprofeno 400mg cada 8 horas",
            "observation": "Paciente presenta tensión muscular en zona cervical",
            "initial_date": "2025-09-28",
            "final_date": "2025-10-05",
            "appointment_type": "Consulta inicial",
            "room": 1,
            "social_benefit": true,
            "payment_detail": null,
            "payment": null,
            "payment_type": 2,
            "payment_type_name": "Tarjeta",
            "payment_status": null,
            "payment_status_name": null,
            "ticket_number": null,
            "appointment_status": 2,
            "is_completed": false,
            "is_pending": true,
            "created_at": "2025-09-27T17:53:22.385290Z",
            "updated_at": "2025-09-27T17:53:22.385301Z",
            "deleted_at": null
        },
        {
            "id": 3,
            "history": 10,
            "patient": 9,
            "patient_name": "Roberto Carlos Lópezz Moralesss",
            "therapist": 1,
            "therapist_name": "Juan Carlos Pérez García",
            "appointment_date": "2025-09-28T10:00:00Z",
            "hour": "10:00:00",
            "ailments": "Dolor de espalda crónico, migrañas ocasionales",
            "diagnosis": "Lumbalgia crónica, cefalea tensional",
            "surgeries": "Ninguna cirugía previa",
            "reflexology_diagnostics": "Puntos sensibles en zona lumbar y cervical",
            "medications": "Ibuprofeno 400mg cada 8 horas",
            "observation": "Paciente presenta tensión muscular en zona cervical",
            "initial_date": "2025-09-28",
            "final_date": "2025-10-05",
            "appointment_type": "Consulta inicial",
            "room": 1,
            "social_benefit": true,
            "payment_detail": null,
            "payment": null,
            "payment_type": 2,
            "payment_type_name": "Tarjeta",
            "payment_status": null,
            "payment_status_name": null,
            "ticket_number": "TKT-001",
            "appointment_status": 2,
            "is_completed": false,
            "is_pending": true,
            "created_at": "2025-09-27T17:54:02.801015Z",
            "updated_at": "2025-09-27T17:54:02.801024Z",
            "deleted_at": null
        }
    ]
}
```

---------------------------------------------------------------------------------------------------------------------------

**Editar Cita:**
- **Método:** PUT
- **URL:** `http://localhost:8000/api/appointments/appointments/id/`
- **Auth:** Basic Auth
  - Crear usuario con 'python manage.py createsuperuser' desde el codigo fuente.
- **Headers:**
  ```
  Content-Type: application/json
  ```
- **Body (raw JSON):**
```json
{
    "therapist": 1,
    "appointment_date": "2025-11-28T10:00:00Z",
    "hour": "12:00:00",
    "ailments": "Dolorr de espalda crónico, migrañas ocasionales",
    "diagnosis": "Lumbaalgia crónica, cefalea tensional",
    "surgeries": "Ningunaa cirugía previa",
    "reflexology_diagnostics": "Puntos sensibles en zona lumbar y cervical",
    "medications": "Ibuprofeno 400mg cada 8 horas",
    "observation": "Paciente presenta tensión muscular en zona cervical",
    "initial_date": "2025-09-28",
    "final_date": "2025-10-05",
    "appointment_type": "Consulta inicial",
    "room": 1,
    "social_benefit": true,
    "payment_type": 2,
    "appointment_status": 2
}
```
**Respuesta Exitosa:**
```json
{
    "message": "Cita actualizada exitosamente",
    "appointment": {
        "id": 4,
        "history": null,
        "patient": 8,
        "patient_name": "Roberto Carlos Lópezz Moralesss",
        "therapist": 1,
        "therapist_name": "Juan Carlos Pérez García",
        "appointment_date": "2025-11-28T10:00:00Z",
        "hour": "12:00:00",
        "ailments": "Dolorr de espalda crónico, migrañas ocasionales",
        "diagnosis": "Lumbaalgia crónica, cefalea tensional",
        "surgeries": "Ningunaa cirugía previa",
        "reflexology_diagnostics": "Puntos sensibles en zona lumbar y cervical",
        "medications": "Ibuprofeno 400mg cada 8 horas",
        "observation": "Paciente presenta tensión muscular en zona cervical",
        "initial_date": "2025-09-28",
        "final_date": "2025-10-05",
        "appointment_type": "Consulta inicial",
        "room": 1,
        "social_benefit": true,
        "payment_detail": null,
        "payment": null,
        "payment_type": 2,
        "payment_type_name": "Tarjeta",
        "payment_status": null,
        "payment_status_name": null,
        "ticket_number": "TKT-002",
        "appointment_status": 2,
        "is_completed": false,
        "is_pending": true,
        "created_at": "2025-09-27T18:01:19.056447Z",
        "updated_at": "2025-09-27T18:06:14.837152Z",
        "deleted_at": null
    }
}
```

---------------------------------------------------------------------------------------------------------------------------

**Eliminar Cita:**
- **Método:** DELETE
- **URL:** `http://localhost:8000/api/appointments/appointments/id/`
- **Auth:** Basic Auth
  - Crear usuario con 'python manage.py createsuperuser' desde el codigo fuente.
- **Headers:**
  ```
  Content-Type: application/json
  ```
- **Body (raw JSON):**
```json
**vacio**
```
**Respuesta Exitosa:**
```json
{
    "message": "Cita eliminada exitosamente"
}
```

---------------------------------------------------------------------------------------------------------------------------

**Ver Cita Especifica:**
- **Método:** GET
- **URL:** `http://localhost:8000/api/appointments/appointments/id/`
- **Auth:** Basic Auth
  - Crear usuario con 'python manage.py createsuperuser' desde el codigo fuente.
- **Headers:**
  ```
  Content-Type: application/json
  ```
- **Body (raw JSON):**
```json
**vacio**
```
**Respuesta Exitosa:**
```json
{
    "id": 1,
    "history": 10,
    "patient": 9,
    "patient_name": "Roberto Carlos Lópezz Moralesss",
    "therapist": 1,
    "therapist_name": "Juan Carlos Pérez García",
    "appointment_date": "2025-09-28T10:00:00Z",
    "hour": "10:00:00",
    "ailments": "Dolor de espalda crónico, migrañas ocasionales",
    "diagnosis": "Lumbalgia crónica, cefalea tensional",
    "surgeries": "Ninguna cirugía previa",
    "reflexology_diagnostics": "Puntos sensibles en zona lumbar y cervical",
    "medications": "Ibuprofeno 400mg cada 8 horas",
    "observation": "Paciente presenta tensión muscular en zona cervical",
    "initial_date": "2025-09-28",
    "final_date": "2025-10-05",
    "appointment_type": "Consulta inicial",
    "room": 1,
    "social_benefit": true,
    "payment_detail": null,
    "payment": null,
    "payment_type": 2,
    "payment_type_name": "Tarjeta",
    "payment_status": null,
    "payment_status_name": null,
    "ticket_number": null,
    "appointment_status": 2,
    "is_completed": false,
    "is_pending": true,
    "created_at": "2025-09-27T17:50:53.452436Z",
    "updated_at": "2025-09-27T17:50:53.452446Z",
    "deleted_at": null
}
```

---------------------------------------------------------------------------------------------------------------------------

**Listar Citas Completadas:**
- **Método:** GET
- **URL:** `http://localhost:8000/api/appointments/appointments/completed/`
- **Auth:** Basic Auth
  - Crear usuario con 'python manage.py createsuperuser' desde el codigo fuente.
- **Headers:**
  ```
  Content-Type: application/json
  ```
- **Body (raw JSON):**
```json
**vacio**
```
**Respuesta Exitosa:**
```json
{
    "count": 4,
    "results": [
        {
            "id": 1,
            "history": 10,
            "patient": 9,
            "patient_name": "Roberto Carlos Lópezz Moralesss",
            "therapist": 1,
            "therapist_name": "Juan Carlos Pérez García",
            "appointment_date": "2025-09-28T10:00:00Z",
            "hour": "10:00:00",
            "ailments": "Dolor de espalda crónico, migrañas ocasionales",
            "diagnosis": "Lumbalgia crónica, cefalea tensional",
            "surgeries": "Ninguna cirugía previa",
            "reflexology_diagnostics": "Puntos sensibles en zona lumbar y cervical",
            "medications": "Ibuprofeno 400mg cada 8 horas",
            "observation": "Paciente presenta tensión muscular en zona cervical",
            "initial_date": "2025-09-28",
            "final_date": "2025-10-05",
            "appointment_type": "Consulta inicial",
            "room": 1,
            "social_benefit": true,
            "payment_detail": null,
            "payment": null,
            "payment_type": 2,
            "payment_type_name": "Tarjeta",
            "payment_status": null,
            "payment_status_name": null,
            "ticket_number": null,
            "appointment_status": 2,
            "is_completed": true,
            "is_pending": false,
            "created_at": "2025-09-27T17:50:53.452436Z",
            "updated_at": "2025-09-27T17:50:53.452446Z",
            "deleted_at": null
        },
        {
            "id": 2,
            "history": 10,
            "patient": 9,
            "patient_name": "Roberto Carlos Lópezz Moralesss",
            "therapist": 1,
            "therapist_name": "Juan Carlos Pérez García",
            "appointment_date": "2025-09-28T10:00:00Z",
            "hour": "10:00:00",
            "ailments": "Dolor de espalda crónico, migrañas ocasionales",
            "diagnosis": "Lumbalgia crónica, cefalea tensional",
            "surgeries": "Ninguna cirugía previa",
            "reflexology_diagnostics": "Puntos sensibles en zona lumbar y cervical",
            "medications": "Ibuprofeno 400mg cada 8 horas",
            "observation": "Paciente presenta tensión muscular en zona cervical",
            "initial_date": "2025-09-28",
            "final_date": "2025-10-05",
            "appointment_type": "Consulta inicial",
            "room": 1,
            "social_benefit": true,
            "payment_detail": null,
            "payment": null,
            "payment_type": 2,
            "payment_type_name": "Tarjeta",
            "payment_status": null,
            "payment_status_name": null,
            "ticket_number": null,
            "appointment_status": 2,
            "is_completed": true,
            "is_pending": false,
            "created_at": "2025-09-27T17:53:22.385290Z",
            "updated_at": "2025-09-27T17:53:22.385301Z",
            "deleted_at": null
        },
        {
            "id": 3,
            "history": 10,
            "patient": 9,
            "patient_name": "Roberto Carlos Lópezz Moralesss",
            "therapist": 1,
            "therapist_name": "Juan Carlos Pérez García",
            "appointment_date": "2025-09-28T10:00:00Z",
            "hour": "10:00:00",
            "ailments": "Dolor de espalda crónico, migrañas ocasionales",
            "diagnosis": "Lumbalgia crónica, cefalea tensional",
            "surgeries": "Ninguna cirugía previa",
            "reflexology_diagnostics": "Puntos sensibles en zona lumbar y cervical",
            "medications": "Ibuprofeno 400mg cada 8 horas",
            "observation": "Paciente presenta tensión muscular en zona cervical",
            "initial_date": "2025-09-28",
            "final_date": "2025-10-05",
            "appointment_type": "Consulta inicial",
            "room": 1,
            "social_benefit": true,
            "payment_detail": null,
            "payment": null,
            "payment_type": 2,
            "payment_type_name": "Tarjeta",
            "payment_status": null,
            "payment_status_name": null,
            "ticket_number": "TKT-001",
            "appointment_status": 2,
            "is_completed": true,
            "is_pending": false,
            "created_at": "2025-09-27T17:54:02.801015Z",
            "updated_at": "2025-09-27T17:54:02.801024Z",
            "deleted_at": null
        },
        {
            "id": 5,
            "history": null,
            "patient": 8,
            "patient_name": "Roberto Carlos Lópezz Moralesss",
            "therapist": 1,
            "therapist_name": "Juan Carlos Pérez García",
            "appointment_date": "2025-09-27T10:00:00Z",
            "hour": "10:00:00",
            "ailments": "Dolorr de espalda crónico, migrañas ocasionales",
            "diagnosis": "Lumbaalgia crónica, cefalea tensional",
            "surgeries": "Ningunaa cirugía previa",
            "reflexology_diagnostics": "Puntos sensibles en zona lumbar y cervical",
            "medications": "Ibuprofeno 400mg cada 8 horas",
            "observation": "Paciente presenta tensión muscular en zona cervical",
            "initial_date": "2025-09-27",
            "final_date": "2025-09-27",
            "appointment_type": "Consulta inicial",
            "room": 1,
            "social_benefit": true,
            "payment_detail": null,
            "payment": null,
            "payment_type": 2,
            "payment_type_name": "Tarjeta",
            "payment_status": null,
            "payment_status_name": null,
            "ticket_number": "TKT-003",
            "appointment_status": 2,
            "is_completed": true,
            "is_pending": false,
            "created_at": "2025-09-27T18:09:16.115201Z",
            "updated_at": "2025-09-27T18:20:16.301917Z",
            "deleted_at": null
        }
    ]
}
```

---------------------------------------------------------------------------------------------------------------------------

**Listar Citas en Espera:**
- **Método:** GET
- **URL:** `http://localhost:8000/api/appointments/appointments/pending/`
- **Auth:** Basic Auth
  - Crear usuario con 'python manage.py createsuperuser' desde el codigo fuente.
- **Headers:**
  ```
  Content-Type: application/json
  ```
- **Body (raw JSON):**
```json
**vacio**
```
**Respuesta Exitosa:**
```json
{
    "count": 1,
    "results": [
        {
            "id": 5,
            "history": null,
            "patient": 8,
            "patient_name": "Roberto Carlos Lópezz Moralesss",
            "therapist": 1,
            "therapist_name": "Juan Carlos Pérez García",
            "appointment_date": "2025-09-27T10:00:00Z",
            "hour": "12:00:00",
            "ailments": "Dolorr de espalda crónico, migrañas ocasionales",
            "diagnosis": "Lumbaalgia crónica, cefalea tensional",
            "surgeries": "Ningunaa cirugía previa",
            "reflexology_diagnostics": "Puntos sensibles en zona lumbar y cervical",
            "medications": "Ibuprofeno 400mg cada 8 horas",
            "observation": "Paciente presenta tensión muscular en zona cervical",
            "initial_date": "2025-09-27",
            "final_date": "2025-09-27",
            "appointment_type": "Consulta inicial",
            "room": 1,
            "social_benefit": true,
            "payment_detail": null,
            "payment": null,
            "payment_type": 2,
            "payment_type_name": "Tarjeta",
            "payment_status": null,
            "payment_status_name": null,
            "ticket_number": "TKT-003",
            "appointment_status": 4,
            "is_completed": false,
            "is_pending": true,
            "created_at": "2025-09-27T18:09:16.115201Z",
            "updated_at": "2025-09-27T18:29:35.812243Z",
            "deleted_at": null
        }
    ]
}
```

---------------------------------------------------------------------------------------------------------------------------

**Listar Citas por Rango de Fechas:**
- **Método:** GET
- **URL:** `http://localhost:8000/api/appointments/appointments/by_date_range/?start_date=2025-09-01&end_date=2025-09-30`
- **Auth:** Basic Auth
  - Crear usuario con 'python manage.py createsuperuser' desde el codigo fuente.
- **Headers:**
  ```
  Content-Type: application/json
  ```
- **Body (raw JSON):**
```json
**vacio**
```
**Respuesta Exitosa:**
```json
{
    "count": 4,
    "results": [
        {
            "id": 1,
            "history": 10,
            "patient": 9,
            "patient_name": "Roberto Carlos Lópezz Moralesss",
            "therapist": 1,
            "therapist_name": "Juan Carlos Pérez García",
            "appointment_date": "2025-09-28T10:00:00Z",
            "hour": "10:00:00",
            "ailments": "Dolor de espalda crónico, migrañas ocasionales",
            "diagnosis": "Lumbalgia crónica, cefalea tensional",
            "surgeries": "Ninguna cirugía previa",
            "reflexology_diagnostics": "Puntos sensibles en zona lumbar y cervical",
            "medications": "Ibuprofeno 400mg cada 8 horas",
            "observation": "Paciente presenta tensión muscular en zona cervical",
            "initial_date": "2025-09-28",
            "final_date": "2025-10-05",
            "appointment_type": "Consulta inicial",
            "room": 1,
            "social_benefit": true,
            "payment_detail": null,
            "payment": null,
            "payment_type": 2,
            "payment_type_name": "Tarjeta",
            "payment_status": null,
            "payment_status_name": null,
            "ticket_number": null,
            "appointment_status": 2,
            "is_completed": true,
            "is_pending": false,
            "created_at": "2025-09-27T17:50:53.452436Z",
            "updated_at": "2025-09-27T17:50:53.452446Z",
            "deleted_at": null
        },
        {
            "id": 2,
            "history": 10,
            "patient": 9,
            "patient_name": "Roberto Carlos Lópezz Moralesss",
            "therapist": 1,
            "therapist_name": "Juan Carlos Pérez García",
            "appointment_date": "2025-09-28T10:00:00Z",
            "hour": "10:00:00",
            "ailments": "Dolor de espalda crónico, migrañas ocasionales",
            "diagnosis": "Lumbalgia crónica, cefalea tensional",
            "surgeries": "Ninguna cirugía previa",
            "reflexology_diagnostics": "Puntos sensibles en zona lumbar y cervical",
            "medications": "Ibuprofeno 400mg cada 8 horas",
            "observation": "Paciente presenta tensión muscular en zona cervical",
            "initial_date": "2025-09-28",
            "final_date": "2025-10-05",
            "appointment_type": "Consulta inicial",
            "room": 1,
            "social_benefit": true,
            "payment_detail": null,
            "payment": null,
            "payment_type": 2,
            "payment_type_name": "Tarjeta",
            "payment_status": null,
            "payment_status_name": null,
            "ticket_number": null,
            "appointment_status": 2,
            "is_completed": true,
            "is_pending": false,
            "created_at": "2025-09-27T17:53:22.385290Z",
            "updated_at": "2025-09-27T17:53:22.385301Z",
            "deleted_at": null
        },
        {
            "id": 3,
            "history": 10,
            "patient": 9,
            "patient_name": "Roberto Carlos Lópezz Moralesss",
            "therapist": 1,
            "therapist_name": "Juan Carlos Pérez García",
            "appointment_date": "2025-09-28T10:00:00Z",
            "hour": "10:00:00",
            "ailments": "Dolor de espalda crónico, migrañas ocasionales",
            "diagnosis": "Lumbalgia crónica, cefalea tensional",
            "surgeries": "Ninguna cirugía previa",
            "reflexology_diagnostics": "Puntos sensibles en zona lumbar y cervical",
            "medications": "Ibuprofeno 400mg cada 8 horas",
            "observation": "Paciente presenta tensión muscular en zona cervical",
            "initial_date": "2025-09-28",
            "final_date": "2025-10-05",
            "appointment_type": "Consulta inicial",
            "room": 1,
            "social_benefit": true,
            "payment_detail": null,
            "payment": null,
            "payment_type": 2,
            "payment_type_name": "Tarjeta",
            "payment_status": null,
            "payment_status_name": null,
            "ticket_number": "TKT-001",
            "appointment_status": 2,
            "is_completed": true,
            "is_pending": false,
            "created_at": "2025-09-27T17:54:02.801015Z",
            "updated_at": "2025-09-27T17:54:02.801024Z",
            "deleted_at": null
        },
        {
            "id": 5,
            "history": null,
            "patient": 8,
            "patient_name": "Roberto Carlos Lópezz Moralesss",
            "therapist": 1,
            "therapist_name": "Juan Carlos Pérez García",
            "appointment_date": "2025-09-27T10:00:00Z",
            "hour": "12:00:00",
            "ailments": "Dolorr de espalda crónico, migrañas ocasionales",
            "diagnosis": "Lumbaalgia crónica, cefalea tensional",
            "surgeries": "Ningunaa cirugía previa",
            "reflexology_diagnostics": "Puntos sensibles en zona lumbar y cervical",
            "medications": "Ibuprofeno 400mg cada 8 horas",
            "observation": "Paciente presenta tensión muscular en zona cervical",
            "initial_date": "2025-09-27",
            "final_date": "2025-09-27",
            "appointment_type": "Consulta inicial",
            "room": 1,
            "social_benefit": true,
            "payment_detail": null,
            "payment": null,
            "payment_type": 2,
            "payment_type_name": "Tarjeta",
            "payment_status": null,
            "payment_status_name": null,
            "ticket_number": "TKT-003",
            "appointment_status": 4,
            "is_completed": false,
            "is_pending": true,
            "created_at": "2025-09-27T18:09:16.115201Z",
            "updated_at": "2025-09-27T18:29:35.812243Z",
            "deleted_at": null
        }
    ]
}
```

---------------------------------------------------------------------------------------------------------------------------

**Crear Ticket:**
- **Método:** POST
- **URL:** `http://localhost:8000/api/appointments/tickets/`
- **Auth:** Basic Auth
  - Crear usuario con 'python manage.py createsuperuser' desde el codigo fuente.
- **Headers:**
  ```
  Content-Type: application/json
  ```
- **Body (raw JSON):**
```json
{
    "appointment": 5,
    "payment_date": "2025-09-27T18:24:15.014122Z",
    "amount": "150.00",
    "payment_type": 2,
    "description": "Ticket generado automáticamente para cita #5",
    "status": "pending",
    "is_paid": false,
    "is_pending": true,
    "created_at": "2025-09-27T18:24:15.014162Z",
    "updated_at": "2025-09-27T18:24:15.014169Z",
    "deleted_at": null
}
```
**Respuesta Exitosa:**
```json
{
    "message": "Ticket creado exitosamente",
    "ticket": {
        "id": 7,
        "appointment": 5,
        "appointment_details": "Cita 5 - 2025-09-27 10:00:00+00:00 12:00:00",
        "ticket_number": "TKT-007",
        "payment_date": "2025-09-27T18:52:32.888070Z",
        "amount": "150.00",
        "payment_type": 2,
        "payment_type_name": "Tarjeta",
        "description": "Ticket generado automáticamente para cita #5",
        "status": "pending",
        "is_paid": false,
        "is_pending": true,
        "created_at": "2025-09-27T18:52:32.888104Z",
        "updated_at": "2025-09-27T18:52:32.888111Z",
        "deleted_at": null
    }
}
```

---------------------------------------------------------------------------------------------------------------------------

**Listar Tickets:**
- **Método:** GET
- **URL:** `http://localhost:8000/api/appointments/tickets/`
- **Auth:** Basic Auth
  - Crear usuario con 'python manage.py createsuperuser' desde el codigo fuente.
- **Headers:**
  ```
  Content-Type: application/json
  ```
- **Body (raw JSON):**
```json
**vacio**
```
**Respuesta Exitosa:**
```json
{
    "count": 2,
    "results": [
        {
            "id": 4,
            "appointment": 6,
            "appointment_details": "Cita 6 - 2025-10-10 10:00:00+00:00 12:00:00",
            "ticket_number": "TKT-004",
            "payment_date": "2025-09-27T18:24:15.014122Z",
            "amount": "150.00",
            "payment_type": 2,
            "payment_type_name": "Tarjeta",
            "description": "Ticket generado automáticamente para cita #6",
            "status": "paid",
            "is_paid": true,
            "is_pending": false,
            "created_at": "2025-09-27T18:24:15.014162Z",
            "updated_at": "2025-09-27T18:38:24.469988Z",
            "deleted_at": null
        },
        {
            "id": 3,
            "appointment": 5,
            "appointment_details": "Cita 5 - 2025-09-27 10:00:00+00:00 12:00:00",
            "ticket_number": "TKT-003",
            "payment_date": "2025-09-27T18:09:16.116944Z",
            "amount": "150.00",
            "payment_type": 2,
            "payment_type_name": "Tarjeta",
            "description": "Ticket generado automáticamente para cita #6",
            "status": "paid",
            "is_paid": true,
            "is_pending": false,
            "created_at": "2025-09-27T18:09:16.116968Z",
            "updated_at": "2025-09-27T18:45:56.723923Z",
            "deleted_at": null
        }
    ]
}
```

---------------------------------------------------------------------------------------------------------------------------

**Editar Ticket:**
- **Método:** PUT
- **URL:** `http://localhost:8000/api/appointments/tickets/id/`
- **Auth:** Basic Auth
  - Crear usuario con 'python manage.py createsuperuser' desde el codigo fuente.
- **Headers:**
  ```
  Content-Type: application/json
  ```
- **Body (raw JSON):**
```json
{
    "payment_date": "2025-09-27T18:24:15.014122Z",
    "amount": "150.00",
    "payment_type": 2,
    "description": "Ticket generado automáticamente para cita #6",
    "status": "paid",
    "is_paid": false,
    "is_pending": true,
    "created_at": "2025-09-27T18:24:15.014162Z",
    "updated_at": "2025-09-27T18:24:15.014169Z",
    "deleted_at": null
}
```
**Respuesta Exitosa:**
```json
{
    "message": "Ticket actualizado exitosamente",
    "ticket": {
        "id": 3,
        "appointment": 5,
        "appointment_details": "Cita 5 - 2025-09-27 10:00:00+00:00 12:00:00",
        "ticket_number": "TKT-003",
        "payment_date": "2025-09-27T18:09:16.116944Z",
        "amount": "150.00",
        "payment_type": 2,
        "payment_type_name": "Tarjeta",
        "description": "Ticket generado automáticamente para cita #6",
        "status": "paid",
        "is_paid": true,
        "is_pending": false,
        "created_at": "2025-09-27T18:09:16.116968Z",
        "updated_at": "2025-09-27T18:45:56.723923Z",
        "deleted_at": null
    }
}
```

---------------------------------------------------------------------------------------------------------------------------

**ELiminar Ticket:**
- **Método:** DELETE
- **URL:** `http://localhost:8000/api/appointments/tickets/id/`
- **Auth:** Basic Auth
  - Crear usuario con 'python manage.py createsuperuser' desde el codigo fuente.
- **Headers:**
  ```
  Content-Type: application/json
  ```
- **Body (raw JSON):**
```json
**vacio**
```
**Respuesta Exitosa:**
```json
{
    "message": "Ticket eliminado exitosamente"
}
```

---------------------------------------------------------------------------------------------------------------------------

**Listar Tickets:**
- **Método:** GET
- **URL:** `http://localhost:8000/api/appointments/tickets/`
- **Auth:** Basic Auth
  - Crear usuario con 'python manage.py createsuperuser' desde el codigo fuente.
- **Headers:**
  ```
  Content-Type: application/json
  ```
- **Body (raw JSON):**
```json
**vacio**
```
**Respuesta Exitosa:**
```json
{
    "count": 2,
    "results": [
        {
            "id": 4,
            "appointment": 6,
            "appointment_details": "Cita 6 - 2025-10-10 10:00:00+00:00 12:00:00",
            "ticket_number": "TKT-004",
            "payment_date": "2025-09-27T18:24:15.014122Z",
            "amount": "150.00",
            "payment_type": 2,
            "payment_type_name": "Tarjeta",
            "description": "Ticket generado automáticamente para cita #6",
            "status": "paid",
            "is_paid": true,
            "is_pending": false,
            "created_at": "2025-09-27T18:24:15.014162Z",
            "updated_at": "2025-09-27T18:38:24.469988Z",
            "deleted_at": null
        },
        {
            "id": 3,
            "appointment": 5,
            "appointment_details": "Cita 5 - 2025-09-27 10:00:00+00:00 12:00:00",
            "ticket_number": "TKT-003",
            "payment_date": "2025-09-27T18:09:16.116944Z",
            "amount": "150.00",
            "payment_type": 2,
            "payment_type_name": "Tarjeta",
            "description": "Ticket generado automáticamente para cita #6",
            "status": "paid",
            "is_paid": true,
            "is_pending": false,
            "created_at": "2025-09-27T18:09:16.116968Z",
            "updated_at": "2025-09-27T18:45:56.723923Z",
            "deleted_at": null
        }
    ]
}
```

---------------------------------------------------------------------------------------------------------------------------

**Ver Ticket Especifico:**
- **Método:** GET
- **URL:** `http://localhost:8000/api/appointments/tickets/id/`
- **Auth:** Basic Auth
  - Crear usuario con 'python manage.py createsuperuser' desde el codigo fuente.
- **Headers:**
  ```
  Content-Type: application/json
  ```
- **Body (raw JSON):**
```json
**vacio**
```
**Respuesta Exitosa:**
```json
{
    "id": 4,
    "appointment": 6,
    "appointment_details": "Cita 6 - 2025-10-10 10:00:00+00:00 12:00:00",
    "ticket_number": "TKT-004",
    "payment_date": "2025-09-27T18:24:15.014122Z",
    "amount": "150.00",
    "payment_type": 2,
    "payment_type_name": "Tarjeta",
    "description": "Ticket generado automáticamente para cita #6",
    "status": "paid",
    "is_paid": true,
    "is_pending": false,
    "created_at": "2025-09-27T18:24:15.014162Z",
    "updated_at": "2025-09-27T18:38:24.469988Z",
    "deleted_at": null
}
```

---------------------------------------------------------------------------------------------------------------------------

**Listar Ticket Pagados:**
- **Método:** GET
- **URL:** `http://localhost:8000/api/appointments/tickets/paid/`
- **Auth:** Basic Auth
  - Crear usuario con 'python manage.py createsuperuser' desde el codigo fuente.
- **Headers:**
  ```
  Content-Type: application/json
  ```
- **Body (raw JSON):**
```json
**vacio**
```
**Respuesta Exitosa:**
```json
{
    "count": 1,
    "results": [
        {
            "id": 4,
            "appointment": 6,
            "appointment_details": "Cita 6 - 2025-10-10 10:00:00+00:00 12:00:00",
            "ticket_number": "TKT-004",
            "payment_date": "2025-09-27T18:24:15.014122Z",
            "amount": "150.00",
            "payment_type": 2,
            "payment_type_name": "Tarjeta",
            "description": "Ticket generado automáticamente para cita #6",
            "status": "paid",
            "is_paid": true,
            "is_pending": false,
            "created_at": "2025-09-27T18:24:15.014162Z",
            "updated_at": "2025-09-27T18:38:24.469988Z",
            "deleted_at": null
        }
    ]
}
```

---------------------------------------------------------------------------------------------------------------------------

**Listar Ticket Pendientes:**
- **Método:** GET
- **URL:** `http://localhost:8000/api/appointments/tickets/pending/`
- **Auth:** Basic Auth
  - Crear usuario con 'python manage.py createsuperuser' desde el codigo fuente.
- **Headers:**
  ```
  Content-Type: application/json
  ```
- **Body (raw JSON):**
```json
**vacio**
```
**Respuesta Exitosa:**
```json
{
    "count": 1,
    "results": [
        {
            "id": 5,
            "appointment": 5,
            "appointment_details": "Cita 5 - 2025-09-27 10:00:00+00:00 12:00:00",
            "ticket_number": "TKT-005",
            "payment_date": "2025-09-27T18:50:49.802724Z",
            "amount": "150.00",
            "payment_type": 2,
            "payment_type_name": "Tarjeta",
            "description": "Ticket generado automáticamente para cita #6",
            "status": "pending",
            "is_paid": false,
            "is_pending": true,
            "created_at": "2025-09-27T18:50:49.802752Z",
            "updated_at": "2025-09-27T18:50:49.802758Z",
            "deleted_at": null
        }
    ]
}
```

---------------------------------------------------------------------------------------------------------------------------

**Marcar Ticket Pagado:**
- **Método:** POST
- **URL:** `http://localhost:8000/api/appointments/tickets/id/mark_as_paid/`
- **Auth:** Basic Auth
  - Crear usuario con 'python manage.py createsuperuser' desde el codigo fuente.
- **Headers:**
  ```
  Content-Type: application/json
  ```
- **Body (raw JSON):**
```json
**vacio**
```
**Respuesta Exitosa:**
```json
{
    "message": "Ticket marcado como pagado exitosamente",
    "ticket": {
        "id": 7,
        "appointment": 5,
        "appointment_details": "Cita 5 - 2025-09-27 10:00:00+00:00 12:00:00",
        "ticket_number": "TKT-007",
        "payment_date": "2025-09-27T18:52:32.888070Z",
        "amount": "150.00",
        "payment_type": 2,
        "payment_type_name": "Tarjeta",
        "description": "Ticket generado automáticamente para cita #5",
        "status": "paid",
        "is_paid": true,
        "is_pending": false,
        "created_at": "2025-09-27T18:52:32.888104Z",
        "updated_at": "2025-09-27T18:53:18.616783Z",
        "deleted_at": null
    }
}
```

---------------------------------------------------------------------------------------------------------------------------

## ⚙️ Módulo 6: Historiales y Configuraciones (`/api/configurations/`)

### Historiales
| Método     | Endpoint                                                | Descripción                       | Autenticación |
|------------|---------------------------------------------------------|-----------------------------------|---------------|
| **GET**    | `/api/configurations/document_types/`                   | Listar Tipos de Documentos        |   Requerida   |
| **POST**   | `/api/configurations/document_types/create/`            | Crear Tipo de Documento           |   Requerida   |
| **PUT**    | `/api/configurations/document_types/{id}/edit/`         | Editar Tipo de Documento          |   Requerida   |
| **DELETE** | `/api/configurations/document_types/{id}/delete/`       | Eliminar Tipo de Documento        |   Requerida   |
---------------------------------------------------------------------------------------------------------------------------|
| **GET**    | `/api/configurations/payment_types/`                    | Listar Tipos de Pagos             |   Requerida   |
| **POST**   | `/api/configurations/payment_types/create/`             | Crear Tipo de Pago                |   Requerida   |
| **PUT**    | `/api/configurations/payment_types/{id}/edit/`          | Editar Tipo de Pago               |   Requerida   |
| **DELETE** | `/api/configurations/payment_types/{id}/delete/`        | Eliminar Tipo de Pago             |   Requerida   |
---------------------------------------------------------------------------------------------------------------------------|
| **GET**    | `/api/configurations/payment_status/`                   | Listar Estados de Pagos           |   Requerida   |
| **POST**   | `/api/configurations/payment_status/create/`            | Crear Estados de Pago             |   Requerida   |
| **PUT**    | `/api/configurations/payment_status/{id}/edit/`         | Editar Estados de Pago            |   Requerida   |
| **DELETE** | `/api/configurations/payment_status/{id}/delete/`       | Eliminar Estados de Pago          |   Requerida   |
---------------------------------------------------------------------------------------------------------------------------|
| **GET**    | `/api/configurations/predetermined_prices/`             | Listar Precios Predeterminados    |   Requerida   |
| **POST**   | `/api/configurations/predetermined_prices/create/`      | Crear Precio Predeterminado       |   Requerida   |
| **PUT**    | `/api/configurations/predetermined_prices/{id}/edit/`   | Editar Precio Predeterminado      |   Requerida   |
| **DELETE** | `/api/configurations/predetermined_prices/{id}/delete/` | Eliminar Precio Predeterminado    |   Requerida   |
---------------------------------------------------------------------------------------------------------------------------|
| **GET**    | `/api/configurations/histories/`                        | Listar Historias                  |   Requerida   |
| **POST**   | `/api/configurations/histories/create/`                 | Crear Historia                    |   Requerida   |
| **PUT**    | `/api/configurations/histories/{id}/edit/`              | Editar Historia                   |   Requerida   |
| **DELETE** | `/api/configurations/histories/{id}/delete/`            | Eliminar Historia                 |   Requerida   |
| **GET**    | `/api/configurations/histories/{id}/`                   | Ver Historia Especifica           |   Requerida   |
| **GET**    | `/api/configurations/histories/patient/{patient_id}/`   | Ver Historia de un Paciente       |   Requerida   |
---------------------------------------------------------------------------------------------------------------------------|

#### Ejemplos de Tipos de Documentos

**Crear Tipo de Documento:**
- **Método:** POST
- **URL:** `http://127.0.0.1:8000/api/configurations/document_types/create/`
- **Auth:** Basic Auth
  - Crear usuario con 'python manage.py createsuperuser' desde el codigo fuente.
- **Headers:**
  ```
  Content-Type: application/json
  ```
- **Body (raw JSON):**
```json
{
  "name": "Carne de Extranjeria",
  "description": "Carne de Extranjeria"
}
```

**Respuesta Exitosa:**
```json
{
  "id": 4,
  "name": "Carne de Extranjeria",
  "description": "Carne de Extranjeria"
}
```

---------------------------------------------------------------------------------------------------------------------------

**Listar Tipos de Documentos:**
- **Método:** GET
- **URL:** `http://127.0.0.1:8000/api/configurations/document_types/`
- **Auth:** Basic Auth
  - Crear usuario con 'python manage.py createsuperuser' desde el codigo fuente.
- **Headers:**
  ```
  Content-Type: application/json
  ```
- **Body (raw JSON):**
  ```json
  **vacio**
  ```

**Respuesta Exitosa:**
```json
{
    "document_types": [
        {
            "id": 4,
            "name": "Carne de Extranjeria",
            "description": "Carne de Extranjeria"
        },
        {
            "id": 3,
            "name": "Pasaporte",
            "description": "Pasaporteee"
        }
    ]
}
```

---------------------------------------------------------------------------------------------------------------------------

**Editar Tipo de Documento:**
- **Método:** PUT
- **URL:** `http://127.0.0.1:8000/api/configurations/document_types/id/edit`
- **Auth:** Basic Auth
  - Crear usuario con 'python manage.py createsuperuser' desde el codigo fuente.
- **Headers:**
  ```
  Content-Type: application/json
  ```
- **Body (raw JSON):**
```json
{
  "name": "Pasaporteeee",
  "description": "Pasaporte"
}
```

**Respuesta Exitosa:**
```json
{
    "id": 3,
    "name": "Pasaporteeee",
    "description": "Pasaporte"
}
```

---------------------------------------------------------------------------------------------------------------------------

**Eliminar Tipo de Documento:**
- **Método:** DELETE
- **URL:** `http://127.0.0.1:8000/api/configurations/document_types/id/delete`
- **Auth:** Basic Auth
  - Crear usuario con 'python manage.py createsuperuser' desde el codigo fuente.
- **Headers:**
  ```
  Content-Type: application/json
  ```
- **Body (raw JSON):**
```json
**vacio**
```

**Respuesta Exitosa:**
```json
{
    "status": "deleted",
    "id": 3
}
```

---------------------------------------------------------------------------------------------------------------------------

#### Ejemplos de Tipos de Pagos

**Crear Tipo de Pago:**
- **Método:** POST
- **URL:** `http://127.0.0.1:8000/api/configurations/payment_types/create/`
- **Auth:** Basic Auth
  - Crear usuario con 'python manage.py createsuperuser' desde el codigo fuente.
- **Headers:**
  ```
  Content-Type: application/json
  ```
- **Body (raw JSON):**
```json
{
    "name": "Yape",
    "description": "Metodo de Pago con Yape"
}
```

**Respuesta Exitosa:**
```json
{
    "id": 5,
    "name": "Yape",
    "description": "Metodo de Pago con Yape"
}
```

---------------------------------------------------------------------------------------------------------------------------

**Listar Tipos de Pagos:**
- **Método:** GET
- **URL:** `http://127.0.0.1:8000/api/configurations/payment_types/`
- **Auth:** Basic Auth
  - Crear usuario con 'python manage.py createsuperuser' desde el codigo fuente.
- **Headers:**
  ```
  Content-Type: application/json
  ```
- **Body (raw JSON):**
```json
**vacio**
```

**Respuesta Exitosa:**
```json
{
    "payment_types": [
        {
            "id": 2,
            "name": "Tarjeta",
            "description": "Metodo de Pago con POS"
        },
        {
            "id": 5,
            "name": "Yape",
            "description": "Metodo de Pago con Yape"
        }
    ]
}
```

---------------------------------------------------------------------------------------------------------------------------

**Editar Tipo de Pago:**
- **Método:** PUT
- **URL:** `http://127.0.0.1:8000/api/configurations/payment_types/id/edit/`
- **Auth:** Basic Auth
  - Crear usuario con 'python manage.py createsuperuser' desde el codigo fuente.
- **Headers:**
  ```
  Content-Type: application/json
  ```
- **Body (raw JSON):**
```json
{
    "name": "Yapeee",
    "description": "Metodo de Pago con Yapeeee"
}
```

**Respuesta Exitosa:**
```json
{
    "id": 5,
    "name": "Yapeee",
    "description": "Metodo de Pago con Yapeeee"
}
```

---------------------------------------------------------------------------------------------------------------------------

**Eliminar Tipo de Pago:**
- **Método:** DELETE
- **URL:** `http://127.0.0.1:8000/api/configurations/payment_types/id/delete/`
- **Auth:** Basic Auth
  - Crear usuario con 'python manage.py createsuperuser' desde el codigo fuente.
- **Headers:**
  ```
  Content-Type: application/json
  ```
- **Body (raw JSON):**
```json
**vacio**
```

**Respuesta Exitosa:**
```json
{
    "status": "deleted",
    "id": 5
}
```

---------------------------------------------------------------------------------------------------------------------------

#### Ejemplos de Estados de Pago

**Crear Estado de Pago:**
- **Método:** POST
- **URL:** `http://127.0.0.1:8000/api/configurations/payment_status/create/`
- **Auth:** Basic Auth
  - Crear usuario con 'python manage.py createsuperuser' desde el codigo fuente.
- **Headers:**
  ```
  Content-Type: application/json
  ```
- **Body (raw JSON):**
```json
{
    "name": "Activo",
    "description": "Metodo de Pago Activo"
}
```

**Respuesta Exitosa:**
```json
{
    "id": 5,
    "name": "Activo",
    "description": "Metodo de Pago Activo"
}
```

---------------------------------------------------------------------------------------------------------------------------

**Listar Estados de Pagos:**
- **Método:** GET
- **URL:** `http://127.0.0.1:8000/api/configurations/payment_status/`
- **Auth:** Basic Auth
  - Crear usuario con 'python manage.py createsuperuser' desde el codigo fuente.
- **Headers:**
  ```
  Content-Type: application/json
  ```
- **Body (raw JSON):**
```json
**vacio**
```

**Respuesta Exitosa:**
```json
{
    "payment_status": [
        {
            "id": 5,
            "name": "Activo",
            "description": "Metodo de Pago Activo"
        },
        {
            "id": 4,
            "name": "Inactivoooo",
            "description": "Metodo de pago Inactivo"
        }
    ]
}
```

---------------------------------------------------------------------------------------------------------------------------

**Editar Estado de Pago:**
- **Método:** PUT
- **URL:** `http://127.0.0.1:8000/api/configurations/payment_status/id/edit/`
- **Auth:** Basic Auth
  - Crear usuario con 'python manage.py createsuperuser' desde el codigo fuente.
- **Headers:**
  ```
  Content-Type: application/json
  ```
- **Body (raw JSON):**
```json
{
    "name": "Activooo",
    "description": "Metodo de Pago Activooo"
}
```

**Respuesta Exitosa:**
```json
{
    "id": 5,
    "name": "Activooo",
    "description": "Metodo de Pago Activooo"
}
```

---------------------------------------------------------------------------------------------------------------------------

**Eliminar Estado de Pago:**
- **Método:** DELETE
- **URL:** `http://127.0.0.1:8000/api/configurations/payment_status/id/delete/`
- **Auth:** Basic Auth
  - Crear usuario con 'python manage.py createsuperuser' desde el codigo fuente.
- **Headers:**
  ```
  Content-Type: application/json
  ```
- **Body (raw JSON):**
```json
**vacio**
```

**Respuesta Exitosa:**
```json
{
    "status": "deleted",
    "id": 5
}
```

---------------------------------------------------------------------------------------------------------------------------

#### Ejemplos de Precios Predeterminados

**Crear Precio Predeterminado:**
- **Método:** POST
- **URL:** `http://127.0.0.1:8000/api/configurations/predetermined_prices/create/`
- **Auth:** Basic Auth
  - Crear usuario con 'python manage.py createsuperuser' desde el codigo fuente.
- **Headers:**
  ```
  Content-Type: application/json
  ```
- **Body (raw JSON):**
```json
{
    "name": "Cupon sin Costooo",
    "price": 100.00
}
```

**Respuesta Exitosa:**
```json
{
    "id": 4,
    "name": "Cupon sin Costooo",
    "price": 100.0
}
```

---------------------------------------------------------------------------------------------------------------------------

**Listar Precios Predeterminados:**
- **Método:** GET
- **URL:** `http://127.0.0.1:8000/api/configurations/predetermined_prices/`
- **Auth:** Basic Auth
  - Crear usuario con 'python manage.py createsuperuser' desde el codigo fuente.
- **Headers:**
  ```
  Content-Type: application/json
  ```
- **Body (raw JSON):**
```json
**vacio**
```

**Respuesta Exitosa:**
```json
{
    "predetermined_prices": [
        {
            "id": 2,
            "name": "coima",
            "price": "150.00"
        },
        {
            "id": 3,
            "name": "Cupon sin Costo",
            "price": "50.00"
        },
        {
            "id": 4,
            "name": "Cupon sin Costooo",
            "price": "100.00"
        }
    ]
}
```

---------------------------------------------------------------------------------------------------------------------------

**Editar Precio Predeterminado:**
- **Método:** PUT
- **URL:** `http://127.0.0.1:8000/api/configurations/predetermined_prices/id/edit/`
- **Auth:** Basic Auth
  - Crear usuario con 'python manage.py createsuperuser' desde el codigo fuente.
- **Headers:**
  ```
  Content-Type: application/json
  ```
- **Body (raw JSON):**
```json
{
    "name": "Cupon sin Costooo",
    "price": 150.00
}
```

**Respuesta Exitosa:**
```json
{
    "id": 4,
    "name": "Cupon sin Costooo",
    "price": "150.0"
}
```

---------------------------------------------------------------------------------------------------------------------------

**Eliminar Precio Predeterminado:**
- **Método:** DELETE
- **URL:** `http://127.0.0.1:8000/api/configurations/predetermined_prices/id/delete/`
- **Auth:** Basic Auth
  - Crear usuario con 'python manage.py createsuperuser' desde el codigo fuente.
- **Headers:**
  ```
  Content-Type: application/json
  ```
- **Body (raw JSON):**
```json
**vacio**
```

**Respuesta Exitosa:**
```json
{
    "status": "deleted",
    "id": 5
}
```

---------------------------------------------------------------------------------------------------------------------------

**Crear Historia:**
- **Método:** POST
- **URL:** `http://localhost:8000/api/configurations/histories/create/`
- **Auth:** Basic Auth
  - Crear usuario con 'python manage.py createsuperuser' desde el codigo fuente.
- **Headers:**
  ```
  Content-Type: application/json
  ```
- **Body (raw JSON):**
```json
{
    "patient": 9,
    "history_date": "2024-03-21",
    "testimony": true,
    "private_observation": "Observacionnn privada del paciente",
    "observation": "Observacionmmm general del historial",
    "height": 175.5,
    "weight": 70.2,
    "last_weight": 68.5,
    "menstruation": true,
    "diu_type": "Tipo A",
    "gestation": false
}
```

**Respuesta Exitosa:**
```json
{
    "message": "Historial creado exitosamente",
    "history": {
        "id": 11,
        "patient": {
            "id": 9,
            "name": "Roberto Carlos",
            "paternal_lastname": "Lópezz",
            "maternal_lastname": "Moralesss",
            "full_name": "Roberto Carlos Lópezz Moralesss",
            "document_number": "24017561",
            "email": "chris124@ejemplo.com",
            "phone1": "+51 423 000 333",
            "phone2": "+51 902 000 412"
        },
        "history_date": "2024-03-21",
        "testimony": true,
        "private_observation": "Observacionnn privada del paciente",
        "observation": "Observacionmmm general del historial",
        "height": 175.5,
        "weight": 70.2,
        "last_weight": 68.5,
        "menstruation": true,
        "diu_type": "Tipo A",
        "gestation": false,
        "created_at": "2025-09-26T19:43:15.639101+00:00",
        "updated_at": "2025-09-26T19:43:15.639115+00:00",
        "deleted_at": null
    }
}
```

---------------------------------------------------------------------------------------------------------------------------

**Listar Historias:**
- **Método:** GET
- **URL:** `http://localhost:8000/api/configurations/histories/`
- **Auth:** Basic Auth
  - Crear usuario con 'python manage.py createsuperuser' desde el codigo fuente.
- **Headers:**
  ```
  Content-Type: application/json
  ```
- **Body (raw JSON):**
```json
**vacio**
```

**Respuesta Exitosa:**
```json
{
    "histories": [
        {
            "id": 11,
            "patient": {
                "id": 9,
                "name": "Roberto Carlos",
                "paternal_lastname": "Lópezz",
                "maternal_lastname": "Moralesss",
                "full_name": "Roberto Carlos Lópezz Moralesss",
                "document_number": "24017561",
                "email": "chris124@ejemplo.com",
                "phone1": "+51 423 000 333",
                "phone2": "+51 902 000 412"
            },
            "history_date": "2024-03-21",
            "testimony": true,
            "private_observation": "Observacionnn privada del paciente",
            "observation": "Observacionmmm general del historial",
            "height": 175.5,
            "weight": 70.2,
            "last_weight": 68.5,
            "menstruation": true,
            "diu_type": "Tipo A",
            "gestation": false,
            "created_at": "2025-09-26T19:43:15.639101+00:00",
            "updated_at": "2025-09-26T19:43:15.639115+00:00",
            "deleted_at": null
        },
        {
            "id": 10,
            "patient": {
                "id": 9,
                "name": "Roberto Carlos",
                "paternal_lastname": "Lópezz",
                "maternal_lastname": "Moralesss",
                "full_name": "Roberto Carlos Lópezz Moralesss",
                "document_number": "24017561",
                "email": "chris124@ejemplo.com",
                "phone1": "+51 423 000 333",
                "phone2": "+51 902 000 412"
            },
            "history_date": "2024-03-19",
            "testimony": true,
            "private_observation": "Observacion privada del paciente",
            "observation": "Observacion general del historial",
            "height": 175.5,
            "weight": 70.2,
            "last_weight": 68.5,
            "menstruation": true,
            "diu_type": "Tipo A",
            "gestation": false,
            "created_at": "2025-09-26T19:38:15.969320+00:00",
            "updated_at": "2025-09-26T19:38:15.969335+00:00",
            "deleted_at": null
        },
        {
            "id": 9,
            "patient": {
                "id": 9,
                "name": "Roberto Carlos",
                "paternal_lastname": "Lópezz",
                "maternal_lastname": "Moralesss",
                "full_name": "Roberto Carlos Lópezz Moralesss",
                "document_number": "24017561",
                "email": "chris124@ejemplo.com",
                "phone1": "+51 423 000 333",
                "phone2": "+51 902 000 412"
            },
            "history_date": "2024-03-18",
            "testimony": true,
            "private_observation": "Observacion privada del paciente",
            "observation": "Observacion general del historial",
            "height": 175.5,
            "weight": 70.2,
            "last_weight": 68.5,
            "menstruation": true,
            "diu_type": "Tipo A",
            "gestation": false,
            "created_at": "2025-09-26T19:38:07.285820+00:00",
            "updated_at": "2025-09-26T19:38:07.285834+00:00",
            "deleted_at": null
        },
        {
            "id": 8,
            "patient": {
                "id": 9,
                "name": "Roberto Carlos",
                "paternal_lastname": "Lópezz",
                "maternal_lastname": "Moralesss",
                "full_name": "Roberto Carlos Lópezz Moralesss",
                "document_number": "24017561",
                "email": "chris124@ejemplo.com",
                "phone1": "+51 423 000 333",
                "phone2": "+51 902 000 412"
            },
            "history_date": "2024-03-17",
            "testimony": true,
            "private_observation": "Observacion privada del paciente",
            "observation": "Observacion general del historial",
            "height": 175.5,
            "weight": 70.2,
            "last_weight": 68.5,
            "menstruation": true,
            "diu_type": "Tipo A",
            "gestation": false,
            "created_at": "2025-09-26T19:38:01.967597+00:00",
            "updated_at": "2025-09-26T19:38:01.967618+00:00",
            "deleted_at": null
        },
        {
            "id": 7,
            "patient": {
                "id": 9,
                "name": "Roberto Carlos",
                "paternal_lastname": "Lópezz",
                "maternal_lastname": "Moralesss",
                "full_name": "Roberto Carlos Lópezz Moralesss",
                "document_number": "24017561",
                "email": "chris124@ejemplo.com",
                "phone1": "+51 423 000 333",
                "phone2": "+51 902 000 412"
            },
            "history_date": "2024-03-16",
            "testimony": true,
            "private_observation": "Observacion privada del paciente",
            "observation": "Observacion general del historial",
            "height": 175.5,
            "weight": 70.2,
            "last_weight": 68.5,
            "menstruation": true,
            "diu_type": "Tipo A",
            "gestation": false,
            "created_at": "2025-09-26T19:37:18.999591+00:00",
            "updated_at": "2025-09-26T19:37:18.999604+00:00",
            "deleted_at": null
        },
        {
            "id": 6,
            "patient": {
                "id": 9,
                "name": "Roberto Carlos",
                "paternal_lastname": "Lópezz",
                "maternal_lastname": "Moralesss",
                "full_name": "Roberto Carlos Lópezz Moralesss",
                "document_number": "24017561",
                "email": "chris124@ejemplo.com",
                "phone1": "+51 423 000 333",
                "phone2": "+51 902 000 412"
            },
            "history_date": "2024-02-17",
            "testimony": true,
            "private_observation": "Observacion privada del paciente",
            "observation": "Observacion general del historial",
            "height": 175.5,
            "weight": 70.2,
            "last_weight": 68.5,
            "menstruation": true,
            "diu_type": "Tipo A",
            "gestation": false,
            "created_at": "2025-09-26T19:37:01.054435+00:00",
            "updated_at": "2025-09-26T19:37:01.054457+00:00",
            "deleted_at": null
        },
        {
            "id": 5,
            "patient": {
                "id": 9,
                "name": "Roberto Carlos",
                "paternal_lastname": "Lópezz",
                "maternal_lastname": "Moralesss",
                "full_name": "Roberto Carlos Lópezz Moralesss",
                "document_number": "24017561",
                "email": "chris124@ejemplo.com",
                "phone1": "+51 423 000 333",
                "phone2": "+51 902 000 412"
            },
            "history_date": "2024-02-16",
            "testimony": true,
            "private_observation": "Observacion privada del paciente",
            "observation": "Observacion general del historial",
            "height": 175.5,
            "weight": 70.2,
            "last_weight": 68.5,
            "menstruation": true,
            "diu_type": "Tipo A",
            "gestation": false,
            "created_at": "2025-09-26T19:36:14.500155+00:00",
            "updated_at": "2025-09-26T19:36:14.500173+00:00",
            "deleted_at": null
        },
        {
            "id": 4,
            "patient": {
                "id": 9,
                "name": "Roberto Carlos",
                "paternal_lastname": "Lópezz",
                "maternal_lastname": "Moralesss",
                "full_name": "Roberto Carlos Lópezz Moralesss",
                "document_number": "24017561",
                "email": "chris124@ejemplo.com",
                "phone1": "+51 423 000 333",
                "phone2": "+51 902 000 412"
            },
            "history_date": "2024-02-15",
            "testimony": true,
            "private_observation": "Observación privada del paciente",
            "observation": "Observación general del historial",
            "height": 175.5,
            "weight": 70.2,
            "last_weight": 68.5,
            "menstruation": true,
            "diu_type": "Tipo A",
            "gestation": false,
            "created_at": "2025-09-26T19:35:32.087129+00:00",
            "updated_at": "2025-09-26T19:35:32.087149+00:00",
            "deleted_at": null
        },
        {
            "id": 3,
            "patient": {
                "id": 9,
                "name": "Roberto Carlos",
                "paternal_lastname": "Lópezz",
                "maternal_lastname": "Moralesss",
                "full_name": "Roberto Carlos Lópezz Moralesss",
                "document_number": "24017561",
                "email": "chris124@ejemplo.com",
                "phone1": "+51 423 000 333",
                "phone2": "+51 902 000 412"
            },
            "history_date": "2024-01-16",
            "testimony": true,
            "private_observation": "Observación privada del paciente",
            "observation": "Observación general del historial",
            "height": 175.5,
            "weight": 70.2,
            "last_weight": 68.5,
            "menstruation": true,
            "diu_type": "Tipo A",
            "gestation": false,
            "created_at": "2025-09-26T19:35:21.881098+00:00",
            "updated_at": "2025-09-26T19:35:21.881123+00:00",
            "deleted_at": null
        },
        {
            "id": 2,
            "patient": {
                "id": 9,
                "name": "Roberto Carlos",
                "paternal_lastname": "Lópezz",
                "maternal_lastname": "Moralesss",
                "full_name": "Roberto Carlos Lópezz Moralesss",
                "document_number": "24017561",
                "email": "chris124@ejemplo.com",
                "phone1": "+51 423 000 333",
                "phone2": "+51 902 000 412"
            },
            "history_date": "2024-01-15",
            "testimony": true,
            "private_observation": null,
            "observation": null,
            "height": null,
            "weight": null,
            "last_weight": null,
            "menstruation": true,
            "diu_type": null,
            "gestation": true,
            "created_at": "2025-09-26T19:33:55.344081+00:00",
            "updated_at": "2025-09-26T19:33:55.344108+00:00",
            "deleted_at": null
        }
    ]
}
```

---------------------------------------------------------------------------------------------------------------------------

**Editar Historia:**
- **Método:** PUT
- **URL:** `http://localhost:8000/api/configurations/histories/id/editar/`
- **Auth:** Basic Auth
  - Crear usuario con 'python manage.py createsuperuser' desde el codigo fuente.
- **Headers:**
  ```
  Content-Type: application/json
  ```
- **Body (raw JSON):**
```json
{
    "history_date": "2024-03-21",
    "testimony": true,
    "private_observation": "Observacion privada del paciente",
    "observation": "Observacion general del historial",
    "height": 170.5,
    "weight": 71.2,
    "last_weight": 68.5,
    "menstruation": true,
    "diu_type": "Tipo A",
    "gestation": false
}
```

**Respuesta Exitosa:**
```json
{
    "message": "Historial actualizado exitosamente",
    "history": {
        "id": 11,
        "patient": 9,
        "history_date": "2024-03-21",
        "testimony": true,
        "private_observation": "Observacion privada del paciente",
        "observation": "Observacion general del historial",
        "height": 170.5,
        "weight": 71.2,
        "last_weight": 68.5,
        "menstruation": true,
        "diu_type": "Tipo A",
        "gestation": false,
        "updated_at": "2025-09-26T19:45:52.985987+00:00"
    }
}
```

---------------------------------------------------------------------------------------------------------------------------

**Eliminar Historia:**
- **Método:** DELETE
- **URL:** `http://localhost:8000/api/configurations/histories/id/delete/`
- **Auth:** Basic Auth
  - Crear usuario con 'python manage.py createsuperuser' desde el codigo fuente.
- **Headers:**
  ```
  Content-Type: application/json
  ```
- **Body (raw JSON):**
```json
**vacio**
```

**Respuesta Exitosa:**
```json
{
    "status": "deleted"
}
```

---------------------------------------------------------------------------------------------------------------------------

**Ver Historia Especifica:**
- **Método:** GET
- **URL:** `http://localhost:8000/api/configurations/histories/id/`
- **Auth:** Basic Auth
  - Crear usuario con 'python manage.py createsuperuser' desde el codigo fuente.
- **Headers:**
  ```
  Content-Type: application/json
  ```
- **Body (raw JSON):**
```json
**vacio**
```

**Respuesta Exitosa:**
```json
{
    "id": 10,
    "patient": {
        "id": 9,
        "name": "Roberto Carlos",
        "paternal_lastname": "Lópezz",
        "maternal_lastname": "Moralesss",
        "full_name": "Roberto Carlos Lópezz Moralesss",
        "document_number": "24017561",
        "email": "chris124@ejemplo.com",
        "phone1": "+51 423 000 333",
        "phone2": "+51 902 000 412"
    },
    "history_date": "2024-03-19",
    "testimony": true,
    "private_observation": "Observacion privada del paciente",
    "observation": "Observacion general del historial",
    "height": 175.5,
    "weight": 70.2,
    "last_weight": 68.5,
    "menstruation": true,
    "diu_type": "Tipo A",
    "gestation": false,
    "created_at": "2025-09-26T19:38:15.969320+00:00",
    "updated_at": "2025-09-26T19:38:15.969335+00:00",
    "deleted_at": null
}
```

---------------------------------------------------------------------------------------------------------------------------

**Ver Historia de un Paciente Especifico:**
- **Método:** GET
- **URL:** `http://localhost:8000/api/configurations/histories/patient/{patient_id}/`
- **Auth:** Basic Auth
  - Crear usuario con 'python manage.py createsuperuser' desde el codigo fuente.
- **Headers:**
  ```
  Content-Type: application/json
  ```
- **Body (raw JSON):**
```json
**vacio**
```

**Respuesta Exitosa:**
```json
{
    "id": 10,
    "patient": {
        "id": 9,
        "name": "Roberto Carlos",
        "paternal_lastname": "Lópezz",
        "maternal_lastname": "Moralesss",
        "full_name": "Roberto Carlos Lópezz Moralesss",
        "document_number": "24017561",
        "email": "chris124@ejemplo.com",
        "phone1": "+51 423 000 333",
        "phone2": "+51 902 000 412"
    },
    "history_date": "2024-03-19",
    "testimony": true,
    "private_observation": "Observacion privada del paciente",
    "observation": "Observacion general del historial",
    "height": 175.5,
    "weight": 70.2,
    "last_weight": 68.5,
    "menstruation": true,
    "diu_type": "Tipo A",
    "gestation": false,
    "created_at": "2025-09-26T19:38:15.969320+00:00",
    "updated_at": "2025-09-26T19:38:15.969335+00:00",
    "deleted_at": null
}
```

---------------------------------------------------------------------------------------------------------------------------

---
## ⚙️ Módulo 8: Empresa y reportes (`/api/company/`)
### Empresa

| Método     | Endpoint                                                | Descripción                       | Autenticación |
|------------|---------------------------------------------------------|-----------------------------------|---------------|
| **GET**    | `/api/company/company/`                                 | Listar Empresas                   |   Requerida   |
| **POST**   | `/api/company/company/`                                 | Crear Empresa                     |   Requerida   |
| **PUT**    | `/api/company/company/{id}/`                            | Editar Empresa                    |   Requerida   |
| **DELETE** | `/api/company/company/{id}/`                            | Eliminar Empresa                  |   Requerida   |
| **GET**    | `/api/company/company/{id}/`                            | Ver Empresa Especifica            |   Requerida   |
| **POST**   | `/api/company/company/{id}/upload_logo/`                | Subir Logo de Empresa             |   Requerida   |
| **PUT**    | `/api/company/company/{id}/upload_logo/`                | Actualizar Logo de Empresa        |   Requerida   |
| **DELETE** | `/api/company/company/{id}/delete_logo/`                | Eliminar Logo de Empresa          |   Requerida   |
---------------------------------------------------------------------------------------------------------------------------|

### Ejemplo de Empresas

**Crear Empresa:**
- **Método:** POST
- **URL:** `http://127.0.0.1:8000/api/company/company/`
- **Auth:** Basic Auth
  - Crear usuario con 'python manage.py createsuperuser' desde el codigo fuente.
- **Headers:**
  ```
  Content-Type: application/json
  ```
- **Body (raw JSON):**
```json
{
    "name": "Reflexo-V4"
}
```

**Respuesta Exitosa:**
```json
{
    "message": "Empresa creada exitosamente",
    "company": {
        "id": 3,
        "name": "Reflexo-V4",
        "logo": null,
        "logo_url": null,
        "has_logo": false,
        "created_at": "2025-09-26T20:03:01.961988Z",
        "updated_at": "2025-09-26T20:03:01.962013Z"
    }
}
```

---------------------------------------------------------------------------------------------------------------------------

**Listar Empresas:**
- **Método:** GET
- **URL:** `http://127.0.0.1:8000/api/company/company/`
- **Auth:** Basic Auth
  - Crear usuario con 'python manage.py createsuperuser' desde el codigo fuente.
- **Headers:**
  ```
  Content-Type: application/json
  ```
- **Body (raw JSON):**
```json
**vacio**
```

**Respuesta Exitosa:**
```json
{
    "status": "success",
    "data": [
        {
            "id": 1,
            "name": "Reflexo-V3",
            "logo": "http://localhost:8000/media/company/reflexo_v3_logo.png",
            "logo_url": "http://localhost:8000/media/company/reflexo_v3_logo.png",
            "has_logo": true,
            "created_at": "2025-09-26T19:50:26.241129Z",
            "updated_at": "2025-09-26T19:55:26.946365Z"
        },
        {
            "id": 3,
            "name": "Reflexo-V4",
            "logo": null,
            "logo_url": null,
            "has_logo": false,
            "created_at": "2025-09-26T20:03:01.961988Z",
            "updated_at": "2025-09-26T20:03:01.962013Z"
        }
    ]
}
```

---------------------------------------------------------------------------------------------------------------------------

**Editar Empresa:**
- **Método:** PUT
- **URL:** `http://127.0.0.1:8000/api/company/company/id/`
- **Auth:** Basic Auth
  - Crear usuario con 'python manage.py createsuperuser' desde el codigo fuente.
- **Headers:**
  ```
  Content-Type: application/json
  ```
- **Body (raw JSON):**
```json
{
    "name": "Reflexo-V5"
}
```

**Respuesta Exitosa:**
```json
{
    "message": "Empresa actualizada exitosamente",
    "company": {
        "id": 3,
        "name": "Reflexo-V5",
        "logo": null,
        "logo_url": null,
        "has_logo": false,
        "created_at": "2025-09-26T20:03:01.961988Z",
        "updated_at": "2025-09-26T20:04:30.327329Z"
    }
}
```

---------------------------------------------------------------------------------------------------------------------------

**Eliminar Empresa:**
- **Método:** DELETE
- **URL:** `http://127.0.0.1:8000/api/company/company/id/`
- **Auth:** Basic Auth
  - Crear usuario con 'python manage.py createsuperuser' desde el codigo fuente.
- **Headers:**
  ```
  Content-Type: application/json
  ```
- **Body (raw JSON):**
```json
**vacio**
```

**Respuesta Exitosa:**
```json
{
    "status": "success",
    "message": "Empresa \"Reflexo-V5\" eliminada correctamente"
}
```

---------------------------------------------------------------------------------------------------------------------------

**Ver Empresa Especifica:**
- **Método:** GET
- **URL:** `http://127.0.0.1:8000/api/company/company/id/`
- **Auth:** Basic Auth
  - Crear usuario con 'python manage.py createsuperuser' desde el codigo fuente.
- **Headers:**
  ```
  Content-Type: application/json
  ```
- **Body (raw JSON):**
```json
**vacio**
```

**Respuesta Exitosa:**
```json
{
    "id": 1,
    "name": "Reflexo-V3",
    "logo": "http://localhost:8000/media/company/reflexo_v3_logo.png",
    "logo_url": "http://localhost:8000/media/company/reflexo_v3_logo.png",
    "has_logo": true,
    "created_at": "2025-09-26T19:50:26.241129Z",
    "updated_at": "2025-09-26T19:55:26.946365Z"
}
```

---------------------------------------------------------------------------------------------------------------------------

**Subir Logo de Empresa:**
- **Método:** POST
- **URL:** `http://localhost:8000/api/company/company/id/upload_logo/`
- **Auth:** Basic Auth
  - Crear usuario con 'python manage.py createsuperuser' desde el codigo fuente.
- **Headers:**
  ```
  Content-Type: application/json
  ```
- **Body (form-data):**
```json
  - Key: Logo --- File
  - Value: Elegir foto desde su PC
```

**Respuesta Exitosa:**
```json
{
    "message": "Logo subido correctamente",
    "company": {
        "id": 4,
        "name": "Reflexo-V5",
        "logo": "http://localhost:8000/media/company/reflexo_v5_logo.png",
        "logo_url": "http://localhost:8000/media/company/reflexo_v5_logo.png",
        "has_logo": true,
        "created_at": "2025-09-26T20:07:16.654571Z",
        "updated_at": "2025-09-26T20:08:09.219338Z"
    }
}
```

---------------------------------------------------------------------------------------------------------------------------

**Actualizar Logo de Empresa:**
- **Método:** PUT
- **URL:** `http://localhost:8000/api/company/company/id/upload_logo/`
- **Auth:** Basic Auth
  - Crear usuario con 'python manage.py createsuperuser' desde el codigo fuente.
- **Headers:**
  ```
  Content-Type: application/json
  ```
- **Body (form-data):**
```json
  - Key: Logo --- File
  - Value: Elegir foto desde su PC
```

**Respuesta Exitosa:**
```json
{
    "message": "Logo actualizado correctamente",
    "company": {
        "id": 4,
        "name": "Reflexo-V5",
        "logo": "http://localhost:8000/media/company/reflexo_v5_logo_dmpcrBg.png",
        "logo_url": "http://localhost:8000/media/company/reflexo_v5_logo_dmpcrBg.png",
        "has_logo": true,
        "created_at": "2025-09-26T20:07:16.654571Z",
        "updated_at": "2025-09-26T20:09:19.645471Z"
    }
}
```

---------------------------------------------------------------------------------------------------------------------------

**Eliminar Logo de Empresa:**
- **Método:** DELETE
- **URL:** `http://localhost:8000/api/company/company/id/delete_logo/`
- **Auth:** Basic Auth
  - Crear usuario con 'python manage.py createsuperuser' desde el codigo fuente.
- **Headers:**
  ```
  Content-Type: application/json
  ```
- **Body (form-data):**
```json
**vacio**
```

**Respuesta Exitosa:**
```json
{
    "message": "Logo eliminado correctamente",
    "company": {
        "id": 1,
        "name": "Reflexo-V3",
        "logo": null,
        "logo_url": null,
        "has_logo": false,
        "created_at": "2025-09-26T19:50:26.241129Z",
        "updated_at": "2025-09-26T19:55:26.946365Z"
    }
}
```

---------------------------------------------------------------------------------------------------------------------------

### Reportes
### Cuando generen la cita pongan payment, payment_type, ,payment_type_name para que se muestre bien los reports:
| Método  | Endpoint                                                                                    | Descripción            | Autenticación |
|---------|---------------------------------------------------------------------------------------------|------------------------|---------------|
| **GET** | `/api/company/reports/appointments-per-therapist/?date=2025-09-27`                          | Reporte por Terapeuta  |   Requerida   |
| **GET** | `/api/company/reports/daily-cash/?date=2025-08-25`                                          | Caja Diaria            |   Requerida   |
| **GET** | `/api/company/reports/patients-by-therapist/?date=2025-08-25`                               | Pacientes por Terapeuta|   Requerida   |
| **GET** | `/api/company/reports/appointments-between-dates/?start_date=2025-08-25&end_date=2025-08-28`| Citas entre Fechas     |   Requerida   |
| **GET** | `/api/company/exports/excel/citas-rango/?start_date=2025-08-25&end_date=2025-08-28`         | Reporte en Excel       |   Requerida   |
|------------------------------------------------------------------------------------------------------------------------------------------------|

### Ejemplos de Reportes

**Reporte por Terapeuta:**
- **Método:** GET
- **URL:** `http://127.0.0.1:8000/api/company/reports/appointments-per-therapist/?date=2025-09-27`
- **Auth:** Basic Auth
  - Crear usuario con 'python manage.py createsuperuser' desde el codigo fuente.
- **Headers:**
  ```
  Content-Type: application/json
  ```
- **Body (raw JSON):**
```json
**vacio**
```

**Respuesta Exitosa:**
```json
{
    "date": "2025-09-27",
    "therapists_appointments": [
        {
            "id": 1,
            "name": "Juan Carlos Pérez García",
            "last_name_paternal": "Pérez",
            "last_name_maternal": "García",
            "appointments_count": 1,
            "percentage": 100.0
        }
    ],
    "total_appointments_count": 1
}
```

---------------------------------------------------------------------------------------------------------------------------

**Caja Diaria:**
- **Método:** GET
- **URL:** `http://127.0.0.1:8000/api/company/reports/daily-cash/?date=2025-09-27`
- **Auth:** Basic Auth
  - Crear usuario con 'python manage.py createsuperuser' desde el codigo fuente.
- **Headers:**
  ```
  Content-Type: application/json
  ```
- **Body (raw JSON):**
```json
**vacio**
```

**Respuesta Exitosa:**
```json
[
    {
        "id_cita": 5,
        "payment": "150.00",
        "payment_type": 2,
        "payment_type_name": "Tarjeta"
    },
    {
        "id_cita": 6,
        "payment": "150.00",
        "payment_type": 2,
        "payment_type_name": "Tarjeta"
    }
]
```

---------------------------------------------------------------------------------------------------------------------------

**Pacientes por Terapeuta:**
- **Método:** GET
- **URL:** `http://127.0.0.1:8000/api/company/reports/patients-by-therapist/?date=2025-09-27`
- **Auth:** Basic Auth
  - Crear usuario con 'python manage.py createsuperuser' desde el codigo fuente.
- **Headers:**
  ```
  Content-Type: application/json
  ```
- **Body (raw JSON):**
```json
**vacio**
```

**Respuesta Exitosa:**
```json
[
    {
        "therapist_id": "1",
        "therapist": "Pérez García Juan Carlos",
        "patients": [
            {
                "patient_id": 8,
                "patient": "Lópezz Moralesss Roberto Carlos",
                "appointments": 1
            }
        ]
    }
]
```

---------------------------------------------------------------------------------------------------------------------------

**Cita entre Fechas:**
- **Método:** GET
- **URL:** `http://127.0.0.1:8000/api/company/reports/appointments-between-dates/?start_date=2025-08-25&end_date=2025-10-01`
- **Auth:** Basic Auth
  - Crear usuario con 'python manage.py createsuperuser' desde el codigo fuente.
- **Headers:**
  ```
  Content-Type: application/json
  ```
- **Body (raw JSON):**
```json
**vacio**
```

**Respuesta Exitosa:**
```json
[
    {
        "appointment_id": 5,
        "patient_id": 8,
        "document_number_patient": "24117561",
        "patient": "Lópezz Moralesss Roberto Carlos",
        "phone1_patient": "+51 423 000 333",
        "appointment_date": "2025-09-27",
        "hour": "12:00"
    },
    {
        "appointment_id": 1,
        "patient_id": 9,
        "document_number_patient": "24017561",
        "patient": "Lópezz Moralesss Roberto Carlos",
        "phone1_patient": "+51 423 000 333",
        "appointment_date": "2025-09-28",
        "hour": "10:00"
    },
    {
        "appointment_id": 2,
        "patient_id": 9,
        "document_number_patient": "24017561",
        "patient": "Lópezz Moralesss Roberto Carlos",
        "phone1_patient": "+51 423 000 333",
        "appointment_date": "2025-09-28",
        "hour": "10:00"
    },
    {
        "appointment_id": 3,
        "patient_id": 9,
        "document_number_patient": "24017561",
        "patient": "Lópezz Moralesss Roberto Carlos",
        "phone1_patient": "+51 423 000 333",
        "appointment_date": "2025-09-28",
        "hour": "10:00"
    }
]
```

---------------------------------------------------------------------------------------------------------------------------

**Reporte en Excel:**
- **Método:** GET
- **URL:** `http://127.0.0.1:8000/api/company/exports/excel/citas-rango/?start_date=2025-08-25&end_date=2025-09-27`
- **Auth:** Basic Auth
  - Crear usuario con 'python manage.py createsuperuser' desde el codigo fuente.
- **Headers:**
  ```
  Content-Type: application/json
  ```
- **Body (raw JSON):**
```json
  - Poner el link en una pesteña de un navegador
  - Si usas POSTMAN, hacer la peticion de la API y al costado de "send" va a salir una opcion de Descargar
```

**Respuesta Exitosa:**
```json
 - Se le descarga un excel en su computadora
```

---------------------------------------------------------------------------------------------------------------------------