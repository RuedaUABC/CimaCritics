# 📋 Modelos de Datos - Backend

## Implementación Actual

Los modelos han sido implementados usando SQLAlchemy con Flask-SQLAlchemy. A continuación se detalla cada modelo con sus campos, relaciones y métodos.

## 1. Modelo Usuario

```python
from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class Usuario(UserMixin, db.Model):
    __tablename__ = 'usuario'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    contraseña_hash = db.Column(db.String(128), nullable=False)
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)
    es_admin = db.Column(db.Boolean, default=False)
    es_moderador = db.Column(db.Boolean, default=False)
    bio = db.Column(db.Text)
    avatar_url = db.Column(db.String(256))
    seguidores_count = db.Column(db.Integer, default=0)
    siguiendo_count = db.Column(db.Integer, default=0)

    # Relaciones
    reviews = db.relationship('Review', backref='autor', lazy='dynamic')
    comentarios = db.relationship('Comentario', backref='autor', lazy='dynamic')
    reportes = db.relationship('Reporte', backref='reportador', lazy='dynamic')
    seguidores = db.relationship('Seguimiento', foreign_keys='Seguimiento.seguido_id', backref='seguido', lazy='dynamic')
    siguiendo = db.relationship('Seguimiento', foreign_keys='Seguimiento.seguidor_id', backref='seguidor', lazy='dynamic')

    def set_password(self, password):
        self.contraseña_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.contraseña_hash, password)

    def __repr__(self):
        return f'<Usuario {self.nombre}>'
```

**Campos principales:**
- `id`: Clave primaria
- `nombre`: Nombre del usuario (64 chars)
- `email`: Email único (120 chars)
- `contraseña_hash`: Hash de contraseña (128 chars)
- `fecha_registro`: Timestamp de registro
- `es_admin/es_moderador`: Roles booleanos
- `bio`: Biografía (texto largo)
- `avatar_url`: URL de avatar (256 chars)
- `seguidores_count/siguiendo_count`: Contadores calculados

**Métodos:**
- `set_password()`: Hashea contraseña
- `check_password()`: Verifica contraseña

## 2. Modelo Comic

```python
class Comic(db.Model):
    __tablename__ = 'comic'
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(128), nullable=False)
    autor = db.Column(db.String(64), nullable=False)
    año = db.Column(db.Integer)
    editorial = db.Column(db.String(64))
    genero = db.Column(db.String(32))
    descripcion = db.Column(db.Text)
    imagen_url = db.Column(db.String(256))
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    promedio_calificacion = db.Column(db.Float, default=0.0)

    # Relaciones
    reviews = db.relationship('Review', backref='comic', lazy='dynamic')

    def __repr__(self):
        return f'<Comic {self.titulo}>'
```

**Campos principales:**
- `id`: Clave primaria
- `titulo`: Título del cómic (128 chars)
- `autor`: Autor (64 chars)
- `año`: Año de publicación
- `editorial`: Editorial (64 chars)
- `genero`: Género (32 chars)
- `descripcion`: Descripción (texto largo)
- `imagen_url`: URL de imagen (256 chars)
- `fecha_creacion`: Timestamp
- `promedio_calificacion`: Promedio calculado (float)

## 3. Modelo Review

```python
class Review(db.Model):
    __tablename__ = 'review'
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    comic_id = db.Column(db.Integer, db.ForeignKey('comic.id'), nullable=False)
    calificacion = db.Column(db.Integer, nullable=False)  # 1-5
    texto = db.Column(db.Text)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    likes = db.Column(db.Integer, default=0)
    dislikes = db.Column(db.Integer, default=0)

    # Relaciones
    comentarios = db.relationship('Comentario', backref='review', lazy='dynamic')

    def __repr__(self):
        return f'<Review {self.id} - {self.calificacion} estrellas>'
```

**Campos principales:**
- `id`: Clave primaria
- `usuario_id`: FK a Usuario
- `comic_id`: FK a Comic
- `calificacion`: Entero 1-5
- `texto`: Texto de la reseña
- `fecha_creacion`: Timestamp
- `likes/dislikes`: Contadores de votos

## 4. Modelo Seguimiento

```python
class Seguimiento(db.Model):
    __tablename__ = 'seguimiento'
    id = db.Column(db.Integer, primary_key=True)
    seguidor_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    seguido_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    fecha_seguimiento = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Seguimiento {self.seguidor_id} -> {self.seguido_id}>'
```

**Campos principales:**
- `id`: Clave primaria
- `seguidor_id`: FK al usuario que sigue
- `seguido_id`: FK al usuario seguido
- `fecha_seguimiento`: Timestamp

## 5. Modelo Reporte

```python
class Reporte(db.Model):
    __tablename__ = 'reporte'
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    contenido_tipo = db.Column(db.String(32), nullable=False)  # 'review', 'comentario', etc.
    contenido_id = db.Column(db.Integer, nullable=False)
    motivo = db.Column(db.String(64), nullable=False)
    descripcion = db.Column(db.Text)
    fecha_reporte = db.Column(db.DateTime, default=datetime.utcnow)
    estado = db.Column(db.String(32), default='pendiente')  # pendiente, resuelto, rechazado

    def __repr__(self):
        return f'<Reporte {self.id} - {self.motivo}>'
```

**Campos principales:**
- `id`: Clave primaria
- `usuario_id`: FK al reportador
- `contenido_tipo`: Tipo de contenido reportado
- `contenido_id`: ID del contenido
- `motivo`: Motivo del reporte
- `descripcion`: Descripción detallada
- `fecha_reporte`: Timestamp
- `estado`: Estado del reporte

## 6. Modelo Comentario

```python
class Comentario(db.Model):
    __tablename__ = 'comentario'
    id = db.Column(db.Integer, primary_key=True)
    review_id = db.Column(db.Integer, db.ForeignKey('review.id'), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    texto = db.Column(db.Text, nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    likes = db.Column(db.Integer, default=0)
    dislikes = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f'<Comentario {self.id}>'
```

**Campos principales:**
- `id`: Clave primaria
- `review_id`: FK a Review
- `usuario_id`: FK a Usuario
- `texto`: Texto del comentario
- `fecha_creacion`: Timestamp
- `likes/dislikes`: Contadores de votos

## Configuración de Base de Datos

### Archivo `config.py`
```python
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'tu_clave_secreta_aqui'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///cima_critics.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
```

### Inicialización en `app.py`
```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'

from models import Usuario, Comic, Review, Seguimiento, Reporte, Comentario
```

## Migraciones

- **Inicializar**: `flask db init`
- **Crear migración**: `flask db migrate -m "Descripción"`
- **Aplicar**: `flask db upgrade`
- **Revertir**: `flask db downgrade`

## Seeders (Datos Iniciales)

Script `utils/seed.py` incluye:
- 5 usuarios de ejemplo (uno administrador)
- 5 cómics clásicos
- Reseñas de ejemplo

Ejecutar: `python utils/seed.py`

## Relaciones y Restricciones

### Relaciones Principales
- Usuario → Review (1:N)
- Comic → Review (1:N)
- Review → Comentario (1:N)
- Usuario → Seguimiento (1:N como seguidor, 1:N como seguido)
- Usuario → Reporte (1:N)

### Restricciones de Integridad
- Email único por usuario
- Calificación entre 1-5 en reviews
- FKs no nulas donde corresponde
- Usuario no puede seguirse a sí mismo (implementar en lógica de aplicación)

### Índices Recomendados
- Usuario.email (único)
- Comic.titulo, Comic.autor (búsqueda)
- Review.usuario_id, Review.comic_id (joins)
- Comic.genero, Comic.editorial (filtros)