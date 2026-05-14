import os
import sys

import pytest

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

os.environ['DATABASE_URL'] = 'sqlite:///:memory:'
os.environ.setdefault('SECRET_KEY', 'test-secret-key')

from app import app as flask_app, db
from models import Comic, Genero, Usuario


@pytest.fixture
def app():
    flask_app.config.update(
        TESTING=True,
        WTF_CSRF_ENABLED=False,
        SQLALCHEMY_DATABASE_URI='sqlite:///:memory:',
    )

    with flask_app.app_context():
        db.drop_all()
        db.create_all()
        yield flask_app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def sample_user(app):
    user = Usuario(nombre='Test User', email='test@example.com')
    user.set_password('password123')
    db.session.add(user)
    db.session.commit()
    return user


@pytest.fixture
def admin_user(app):
    user = Usuario(nombre='Admin User', email='admin@example.com', es_admin=True)
    user.set_password('admin123')
    db.session.add(user)
    db.session.commit()
    return user


@pytest.fixture
def moderator_user(app):
    user = Usuario(nombre='Mod User', email='mod@example.com', es_moderador=True)
    user.set_password('mod123')
    db.session.add(user)
    db.session.commit()
    return user


@pytest.fixture
def another_user(app):
    user = Usuario(nombre='Reader Two', email='reader2@example.com')
    user.set_password('password123')
    db.session.add(user)
    db.session.commit()
    return user


@pytest.fixture
def sample_comic(app):
    genero = Genero(nombre='Drama')
    comic = Comic(
        titulo='Watchmen',
        escritor='Alan Moore',
        dibujante='Dave Gibbons',
        lanzamiento='1986',
        editorial='DC Comics',
        descripcion='Una historia compleja sobre superheroes retirados.',
    )
    comic.generos.append(genero)
    db.session.add(comic)
    db.session.commit()
    return comic


def login(client, email='test@example.com', password='password123'):
    return client.post(
        '/login',
        data={'email': email, 'password': password},
        follow_redirects=True,
    )
