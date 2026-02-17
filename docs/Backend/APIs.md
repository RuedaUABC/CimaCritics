# 🔌 Documentación de APIs - Backend

## 1. Autenticación

### POST /api/auth/register
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

### POST /api/auth/login
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