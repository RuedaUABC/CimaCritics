# 🔌 APIs y Endpoints - Backend

## Estado Actual

Actualmente, la aplicación está implementada como una aplicación web Flask tradicional con templates del lado servidor, no como una API REST pura. Los endpoints están diseñados para renderizar HTML, pero están preparados para evolucionar hacia una arquitectura API-first.

## Arquitectura Actual

### Patrón Actual: Server-Side Rendering
- Endpoints retornan HTML (templates Jinja2)
- Sesiones manejadas con Flask-Login
- Formularios con Flask-WTF
- Navegación tradicional

### Transición Futura: API REST
- Endpoints JSON para datos
- JWT para autenticación (opcional)
- SPA con Vue.js/React
- Separación frontend/backend

## Endpoints Implementados (Actuales)

### Autenticación
- `GET/POST /login` - Página de login
- `GET/POST /register` - Página de registro
- `GET /logout` - Cerrar sesión

### Navegación General
- `GET /` - Página principal (futuro)
- `GET /comics` - Listado de cómics (futuro)
- `GET /comics/<id>` - Detalle de cómic (futuro)

## Endpoints Planificados (API REST Futura)

### Autenticación API

#### POST /api/auth/register
Registra un nuevo usuario.

**Request Body:**
```json
{
  "nombre": "Juan Pérez",
  "email": "juan@example.com",
  "password": "password123"
}
```

**Response (201):**
```json
{
  "message": "Usuario registrado exitosamente",
  "usuario": {
    "id": 1,
    "nombre": "Juan Pérez",
    "email": "juan@example.com"
  }
}
```

#### POST /api/auth/login
Inicia sesión de usuario.

**Request Body:**
```json
{
  "email": "juan@example.com",
  "password": "password123"
}
```

**Response (200):**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "usuario": {
    "id": 1,
    "nombre": "Juan Pérez",
    "email": "juan@example.com"
  }
}
```

#### GET /api/auth/me
Obtiene información del usuario actual.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200):**
```json
{
  "id": 1,
  "nombre": "Juan Pérez",
  "email": "juan@example.com",
  "es_admin": false,
  "fecha_registro": "2024-01-15T10:30:00Z"
}
```

### Cómics

#### GET /api/comics
Lista cómics con paginación y filtros.

**Query Parameters:**
- `page` (int): Página (default: 1)
- `per_page` (int): Items por página (default: 20)
- `genero` (str): Filtrar por género
- `autor` (str): Filtrar por autor
- `titulo` (str): Buscar en título

**Response (200):**
```json
{
  "comics": [
    {
      "id": 1,
      "titulo": "Watchmen",
      "autor": "Alan Moore",
      "año": 1986,
      "editorial": "DC Comics",
      "genero": "Superhéroes",
      "promedio_calificacion": 4.8,
      "imagen_url": "https://...",
      "fecha_creacion": "2024-01-15T10:30:00Z"
    }
  ],
  "total": 150,
  "page": 1,
  "per_page": 20,
  "pages": 8
}
```

#### GET /api/comics/{id}
Obtiene detalle de un cómic específico.

**Response (200):**
```json
{
  "id": 1,
  "titulo": "Watchmen",
  "autor": "Alan Moore",
  "año": 1986,
  "editorial": "DC Comics",
  "genero": "Superhéroes",
  "descripcion": "Historia compleja sobre superhéroes...",
  "imagen_url": "https://...",
  "promedio_calificacion": 4.8,
  "reviews_count": 25,
  "fecha_creacion": "2024-01-15T10:30:00Z"
}
```

#### POST /api/comics
Crea un nuevo cómic (solo admin).

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "titulo": "Nuevo Cómic",
  "autor": "Autor Ejemplo",
  "año": 2024,
  "editorial": "Editorial X",
  "genero": "Aventura",
  "descripcion": "Descripción del cómic...",
  "imagen_url": "https://..."
}
```

### Reseñas

#### GET /api/comics/{comic_id}/reviews
Lista reseñas de un cómic.

**Response (200):**
```json
{
  "reviews": [
    {
      "id": 1,
      "usuario": {
        "id": 1,
        "nombre": "Juan Pérez"
      },
      "calificacion": 5,
      "texto": "Excelente cómic...",
      "fecha_creacion": "2024-01-15T10:30:00Z",
      "likes": 12,
      "dislikes": 2
    }
  ],
  "promedio": 4.8,
  "total": 25
}
```

#### POST /api/comics/{comic_id}/reviews
Crea una reseña para un cómic.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "calificacion": 5,
  "texto": "Excelente cómic, lo recomiendo..."
}
```

### Usuarios

#### GET /api/users/{id}
Obtiene perfil de usuario.

**Response (200):**
```json
{
  "id": 1,
  "nombre": "Juan Pérez",
  "email": "juan@example.com",
  "bio": "Amante de los cómics...",
  "avatar_url": "https://...",
  "es_admin": false,
  "seguidores_count": 45,
  "siguiendo_count": 32,
  "fecha_registro": "2024-01-15T10:30:00Z"
}
```

#### GET /api/users/{id}/reviews
Obtiene reseñas de un usuario.

## Códigos de Estado HTTP

- **200 OK**: Solicitud exitosa
- **201 Created**: Recurso creado
- **400 Bad Request**: Datos inválidos
- **401 Unauthorized**: No autenticado
- **403 Forbidden**: No autorizado
- **404 Not Found**: Recurso no encontrado
- **409 Conflict**: Conflicto (ej: email duplicado)
- **422 Unprocessable Entity**: Validación fallida
- **500 Internal Server Error**: Error del servidor

## Autenticación API (Futuro)

### JWT Tokens
- **Access Token**: Expira en 15 minutos
- **Refresh Token**: Expira en 7 días
- Header: `Authorization: Bearer <token>`

### Refresh Token
```http
POST /api/auth/refresh
Authorization: Bearer <refresh_token>
```

## Rate Limiting

- **Login**: 5 intentos por minuto por IP
- **Registro**: 3 registros por hora por IP
- **API general**: 1000 requests por hora por usuario

## Versionado

- **v1**: `/api/v1/`
- Headers: `Accept: application/vnd.cimacritics.v1+json`

## Documentación Interactiva

- **Swagger UI**: `/api/docs`
- **ReDoc**: `/api/redoc`
- **OpenAPI 3.0**: `/api/openapi.json`

## 2. Cómics

### GET /api/comics
Obtiene lista de cómics con paginación y filtros.

**Query Parameters:**
- `page` (int): Página (default: 1)
- `per_page` (int): Elementos por página (default: 20)
- `titulo` (str): Filtrar por título
- `autor` (str): Filtrar por autor
- `genero` (str): Filtrar por género
- `editorial` (str): Filtrar por editorial

**Response (200):**
```json
{
  "comics": [
    {
      "id": 1,
      "titulo": "Batman: The Killing Joke",
      "autor": "Alan Moore",
      "año": 1988,
      "editorial": "DC Comics",
      "genero": "Drama",
      "promedio_calificacion": 4.5
    }
  ],
  "total": 150,
  "page": 1,
  "per_page": 20
}
```

### GET /api/comics/{id}
Obtiene detalles de un cómic específico.

**Response (200):**
```json
{
  "id": 1,
  "titulo": "Batman: The Killing Joke",
  "autor": "Alan Moore",
  "año": 1988,
  "editorial": "DC Comics",
  "genero": "Drama",
  "descripcion": "Descripción completa...",
  "imagen_url": "https://...",
  "promedio_calificacion": 4.5,
  "reviews_count": 25
}
```

## 3. Reseñas

### GET /api/comics/{comic_id}/reviews
Obtiene reseñas de un cómic.

**Response (200):**
```json
{
  "reviews": [
    {
      "id": 1,
      "usuario": {
        "id": 1,
        "nombre": "Juan Pérez"
      },
      "calificacion": 5,
      "texto": "Excelente cómic...",
      "fecha_creacion": "2024-01-15T10:30:00Z",
      "likes": 12,
      "dislikes": 2
    }
  ],
  "total": 25
}
```

### POST /api/reviews
Crea una nueva reseña. (Requiere autenticación)

**Request Body:**
```json
{
  "comic_id": 1,
  "calificacion": 5,
  "texto": "Excelente cómic, muy recomendado!"
}
```

**Response (201):**
```json
{
  "message": "Reseña creada exitosamente",
  "review": {
    "id": 1,
    "comic_id": 1,
    "calificacion": 5,
    "texto": "Excelente cómic...",
    "fecha_creacion": "2024-01-15T10:30:00Z"
  }
}
```

### PUT /api/reviews/{id}
Actualiza una reseña. (Solo el autor puede editar)

### DELETE /api/reviews/{id}
Elimina una reseña. (Solo el autor o admin puede eliminar)

## 4. Códigos de Error
- `400`: Datos inválidos
- `401`: No autorizado
- `403`: Prohibido
- `404`: Recurso no encontrado
- `409`: Conflicto (ej: reseña duplicada)
- `500`: Error interno del servidor

## 5. Autenticación
Todos los endpoints que requieren autenticación deben incluir el header:
```
Authorization: Bearer <access_token>
```