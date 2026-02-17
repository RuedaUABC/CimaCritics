# 📋 Modelos de Datos - Backend

## 1. Modelo Usuario
```python
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    contraseña_hash = Column(String(256), nullable=False)
    fecha_registro = Column(DateTime, default=func.now())
    es_admin = Column(Boolean, default=False)
    
    # Relaciones
    reviews = db.relationship('Review', backref='usuario', lazy=True)
```

## 2. Modelo Comic
```python
class Comic(db.Model):
    __tablename__ = 'comics'
    
    id = Column(Integer, primary_key=True)
    titulo = Column(String(200), nullable=False)
    autor = Column(String(100), nullable=False)
    año = Column(Integer, nullable=False)
    editorial = Column(String(100), nullable=False)
    genero = Column(String(50), nullable=False)
    descripcion = Column(Text, nullable=True)
    imagen_url = Column(String(500), nullable=True)
    fecha_creacion = Column(DateTime, default=func.now())
    promedio_calificacion = Column(Float, default=0.0)
    
    # Relaciones
    reviews = db.relationship('Review', backref='comic', lazy=True)
```

## 3. Modelo Review
```python
class Review(db.Model):
    __tablename__ = 'reviews'
    
    id = Column(Integer, primary_key=True)
    usuario_id = Column(Integer, db.ForeignKey('usuarios.id'), nullable=False)
    comic_id = Column(Integer, db.ForeignKey('comics.id'), nullable=False)
    calificacion = Column(Integer, nullable=False)  # 1-5
    texto = Column(Text, nullable=True)
    fecha_creacion = Column(DateTime, default=func.now())
    likes = Column(Integer, default=0)
    dislikes = Column(Integer, default=0)
    
    # Restricciones
    __table_args__ = (
        db.CheckConstraint('calificacion >= 1 AND calificacion <= 5'),
    )
```

## 4. Serializers (para API)
```python
from marshmallow import Schema, fields, validate

class UsuarioSchema(Schema):
    id = fields.Int(dump_only=True)
    nombre = fields.Str(required=True, validate=validate.Length(min=2, max=100))
    email = fields.Email(required=True)
    fecha_registro = fields.DateTime(dump_only=True)
    es_admin = fields.Bool(dump_only=True)

class ComicSchema(Schema):
    id = fields.Int(dump_only=True)
    titulo = fields.Str(required=True, validate=validate.Length(max=200))
    autor = fields.Str(required=True, validate=validate.Length(max=100))
    año = fields.Int(required=True, validate=validate.Range(min=1900, max=2100))
    editorial = fields.Str(required=True, validate=validate.Length(max=100))
    genero = fields.Str(required=True, validate=validate.Length(max=50))
    descripcion = fields.Str()
    imagen_url = fields.URL()
    fecha_creacion = fields.DateTime(dump_only=True)
    promedio_calificacion = fields.Float(dump_only=True)

class ReviewSchema(Schema):
    id = fields.Int(dump_only=True)
    usuario_id = fields.Int(dump_only=True)
    comic_id = fields.Int(required=True)
    calificacion = fields.Int(required=True, validate=validate.Range(min=1, max=5))
    texto = fields.Str(validate=validate.Length(max=2000))
    fecha_creacion = fields.DateTime(dump_only=True)
    likes = fields.Int(dump_only=True)
    dislikes = fields.Int(dump_only=True)
```