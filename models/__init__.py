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

class Seguimiento(db.Model):
    __tablename__ = 'seguimiento'
    id = db.Column(db.Integer, primary_key=True)
    seguidor_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    seguido_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    fecha_seguimiento = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Seguimiento {self.seguidor_id} -> {self.seguido_id}>'

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