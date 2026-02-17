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
    es_admin: Boolean
}
```

## 4. Endpoints de la API
- `GET /api/comics` - Listar cómics
- `GET /api/comics/{id}` - Detalles de cómic
- `POST /api/reviews` - Crear reseña
- `PUT /api/reviews/{id}` - Actualizar reseña
- `DELETE /api/reviews/{id}` - Eliminar reseña
- `POST /api/auth/login` - Login
- `POST /api/auth/register` - Registro

## 5. Requisitos de Seguridad
- Hashing de contraseñas con bcrypt
- Validación de entrada
- Protección CSRF
- Rate limiting
- Sanitización de datos

## 6. Requisitos de Despliegue
- Python 3.8+
- Dependencias en requirements.txt
- Variables de entorno para configuración
- Base de datos PostgreSQL en producción