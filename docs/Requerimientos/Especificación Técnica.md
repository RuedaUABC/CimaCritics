# ⚙️ Especificación Técnica - CimaCritics

## 1. Arquitectura del Sistema
```
Frontend (HTML/CSS/JS) ←→ API REST (Flask) ←→ Base de Datos (SQLAlchemy)
```

## 2. Tecnologías
- **Backend Framework**: Flask 2.x
- **ORM**: SQLAlchemy 2.x
- **Base de Datos**: PostgreSQL (producción) / SQLite (desarrollo)
- **Autenticación**: JWT (JSON Web Tokens)
- **Frontend**: Vanilla JavaScript + HTML5 + CSS3
- **Testing**: pytest + coverage
- **Documentación API**: Flask-RESTX o similar

## 3. Estructura de Datos

### Modelo Comic
```python
{
    id: Integer (PK),
    titulo: String(200),
    autor: String(100),
    año: Integer,
    editorial: String(100),
    genero: String(50),
    descripcion: Text,
    imagen_url: String(500),
    fecha_creacion: DateTime,
    promedio_calificacion: Float
}
```

### Modelo Review
```python
{
    id: Integer (PK),
    comic_id: Integer (FK),
    usuario_id: Integer (FK),
    calificacion: Integer (1-5),
    texto: Text,
    fecha_creacion: DateTime,
    likes: Integer,
    dislikes: Integer
}
```

### Modelo Usuario
```python
{
    id: Integer (PK),
    nombre: String(100),
    email: String(150) UNIQUE,
    contraseña_hash: String(256),
    fecha_registro: DateTime,
    es_admin: Boolean,
    es_moderador: Boolean,
    bio: Text,
    avatar_url: String(500),
    seguidores_count: Integer,
    siguiendo_count: Integer
}
```

### Modelo Seguimiento
```python
{
    id: Integer (PK),
    seguidor_id: Integer (FK -> Usuario),
    seguido_id: Integer (FK -> Usuario),
    fecha_seguimiento: DateTime
}
```

### Modelo Reporte
```python
{
    id: Integer (PK),
    usuario_id: Integer (FK -> Usuario),
    contenido_tipo: String (comic/review/comment),
    contenido_id: Integer,
    motivo: String(200),
    descripcion: Text,
    fecha_reporte: DateTime,
    estado: String (pendiente/aprobado/rechazado)
}
```

### Modelo Comentario
```python
{
    id: Integer (PK),
    review_id: Integer (FK -> Review),
    usuario_id: Integer (FK -> Usuario),
    texto: Text,
    fecha_creacion: DateTime,
    likes: Integer,
    dislikes: Integer
}
```

## 3.5 Sistema de Recomendaciones
- **Algoritmos**:
  - **Filtrado Colaborativo**: Usar librerías como Surprise o scikit-learn para calcular similitudes entre usuarios o ítems basados en calificaciones.
  - **Basado en Contenido**: Análisis de texto en descripciones y metadatos usando TF-IDF o embeddings (e.g., con spaCy o transformers).
  - **Híbrido**: Combinar ambos enfoques para mayor precisión.
- **Datos de Entrada**: Calificaciones de reseñas, metadatos de cómics (género, autor), interacciones (seguidores, likes).
- **Procesamiento**: Tareas en background (e.g., con Celery) para recalcular recomendaciones diariamente o tras cambios significativos.
- **Almacenamiento**: Tabla de recomendaciones precomputadas en BD para rendimiento.
- **Librerías Sugeridas**: Pandas para análisis, NumPy para cálculos, Flask-Caching para cachear resultados.

## 4. Endpoints de la API
- `GET /api/comics` - Listar cómics (con paginación, filtros)
- `GET /api/comics/{id}` - Detalles de cómic
- `POST /api/comics` - Crear cómic (admin)
- `PUT /api/comics/{id}` - Actualizar cómic (admin)
- `DELETE /api/comics/{id}` - Eliminar cómic (admin)
- `GET /api/reviews` - Listar reseñas
- `GET /api/reviews/{id}` - Detalles de reseña
- `POST /api/reviews` - Crear reseña
- `PUT /api/reviews/{id}` - Actualizar reseña (propia)
- `DELETE /api/reviews/{id}` - Eliminar reseña (propia o admin)
- `POST /api/reviews/{id}/comments` - Crear comentario en reseña
- `POST /api/auth/login` - Login
- `POST /api/auth/register` - Registro
- `GET /api/users/{id}` - Perfil de usuario
- `POST /api/users/{id}/follow` - Seguir usuario
- `DELETE /api/users/{id}/follow` - Dejar de seguir
- `GET /api/recommendations` - Recomendaciones personalizadas
- `GET /api/stats` - Estadísticas globales
- `POST /api/reports` - Reportar contenido
- `GET /api/admin/reports` - Listar reportes (admin/moderador)

## 5. Requisitos de Seguridad
- Hashing de contraseñas con bcrypt o Argon2
- Validación de entrada con sanitización
- Protección CSRF en formularios
- Rate limiting en endpoints de autenticación
- Sanitización de HTML en reseñas y comentarios
- Logs de seguridad para auditoría
- Encriptación de datos en tránsito (HTTPS obligatorio)

## 6. Requisitos de Despliegue
- Python 3.8+
- Dependencias en requirements.txt (pinned versions)
- Variables de entorno para configuración (SECRET_KEY, DB_URL, etc.)
- Base de datos PostgreSQL en producción con backups automáticos
- Servidor web: Gunicorn + Nginx
- Contenedorización: Docker para desarrollo y producción
- CI/CD: GitHub Actions para tests y despliegue automático