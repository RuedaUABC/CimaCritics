import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import db, app
from models import Usuario, Comic, Review
import random

def seed_database():
    with app.app_context():
        # Crear usuarios de ejemplo
        usuarios_data = [
            {'nombre': 'Alice Johnson', 'email': 'alice@example.com', 'password': 'password123'},
            {'nombre': 'Bob Smith', 'email': 'bob@example.com', 'password': 'password123'},
            {'nombre': 'Charlie Brown', 'email': 'charlie@example.com', 'password': 'password123'},
            {'nombre': 'Diana Prince', 'email': 'diana@example.com', 'password': 'password123'},
            {'nombre': 'Admin User', 'email': 'admin@cimacritics.com', 'password': 'admin123', 'es_admin': True}
        ]

        usuarios = []
        for data in usuarios_data:
            usuario = Usuario(
                nombre=data['nombre'],
                email=data['email'],
                es_admin=data.get('es_admin', False)
            )
            usuario.set_password(data['password'])
            usuarios.append(usuario)
            db.session.add(usuario)

        # Crear cómics de ejemplo
        comics_data = [
            {'titulo': 'Watchmen', 'autor': 'Alan Moore', 'año': 1986, 'editorial': 'DC Comics', 'genero': 'Superhéroes', 'descripcion': 'Una historia compleja sobre superhéroes retirados.'},
            {'titulo': 'The Dark Knight Returns', 'autor': 'Frank Miller', 'año': 1986, 'editorial': 'DC Comics', 'genero': 'Superhéroes', 'descripcion': 'Batman regresa en una Gotham distópica.'},
            {'titulo': 'Maus', 'autor': 'Art Spiegelman', 'año': 1991, 'editorial': 'Pantheon Books', 'genero': 'Autobiográfico', 'descripcion': 'Historia del Holocausto contada con animales.'},
            {'titulo': 'Sandman', 'autor': 'Neil Gaiman', 'año': 1989, 'editorial': 'DC Comics', 'genero': 'Fantasía', 'descripcion': 'Las aventuras del Señor de los Sueños.'},
            {'titulo': 'Persepolis', 'autor': 'Marjane Satrapi', 'año': 2000, 'editorial': 'Pantheon Books', 'genero': 'Autobiográfico', 'descripcion': 'Memorias de una niña en la Revolución Iraní.'}
        ]

        comics = []
        for data in comics_data:
            comic = Comic(**data)
            comics.append(comic)
            db.session.add(comic)

        db.session.commit()  # Commit para obtener IDs

        # Crear reseñas de ejemplo
        reviews_data = [
            {'usuario': usuarios[0], 'comic': comics[0], 'calificacion': 5, 'texto': '¡Una obra maestra!'},
            {'usuario': usuarios[1], 'comic': comics[0], 'calificacion': 4, 'texto': 'Muy bueno, pero complejo.'},
            {'usuario': usuarios[2], 'comic': comics[1], 'calificacion': 5, 'texto': 'Frank Miller en su mejor momento.'},
            {'usuario': usuarios[3], 'comic': comics[2], 'calificacion': 5, 'texto': 'Emocionante y educativo.'},
            {'usuario': usuarios[0], 'comic': comics[3], 'calificacion': 4, 'texto': 'Neil Gaiman es un genio.'},
            {'usuario': usuarios[1], 'comic': comics[4], 'calificacion': 5, 'texto': 'Una perspectiva única.'}
        ]

        for data in reviews_data:
            review = Review(
                usuario_id=data['usuario'].id,
                comic_id=data['comic'].id,
                calificacion=data['calificacion'],
                texto=data['texto']
            )
            db.session.add(review)

        db.session.commit()
        print("Base de datos sembrada con datos iniciales.")

if __name__ == '__main__':
    seed_database()