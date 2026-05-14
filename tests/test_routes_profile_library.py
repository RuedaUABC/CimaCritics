from app import db
from models import ComicGuardado, Usuario
from tests.conftest import login


def test_user_can_save_and_unsave_comic(client, sample_user, sample_comic):
    login(client)

    response = client.post(f'/comics/{sample_comic.id}/save', follow_redirects=True)

    assert response.status_code == 200
    assert ComicGuardado.query.filter_by(usuario_id=sample_user.id, comic_id=sample_comic.id).count() == 1

    client.post(f'/comics/{sample_comic.id}/save', follow_redirects=True)

    assert ComicGuardado.query.filter_by(usuario_id=sample_user.id, comic_id=sample_comic.id).count() == 0


def test_saved_comic_appears_in_profile_library(client, sample_user, sample_comic):
    saved = ComicGuardado(usuario_id=sample_user.id, comic_id=sample_comic.id)
    db.session.add(saved)
    db.session.commit()

    response = client.get(f'/perfil/{sample_user.id}')

    assert response.status_code == 200
    assert b'Biblioteca Guardada' in response.data
    assert sample_comic.titulo.encode('utf-8') in response.data


def test_user_can_edit_profile(client, sample_user):
    login(client)

    response = client.post(
        '/perfil/edit',
        data={
            'nombre': 'Nuevo Nombre',
            'email': 'nuevo@example.com',
            'bio': 'Lector de novelas gráficas.',
            'avatar_url': 'https://example.com/avatar.png',
        },
        follow_redirects=True,
    )
    db.session.refresh(sample_user)

    assert response.status_code == 200
    assert sample_user.nombre == 'Nuevo Nombre'
    assert sample_user.email == 'nuevo@example.com'
    assert sample_user.bio == 'Lector de novelas gráficas.'
    assert sample_user.avatar_url == 'https://example.com/avatar.png'


def test_profile_edit_rejects_duplicate_email(client, sample_user, another_user):
    login(client)

    response = client.post(
        '/perfil/edit',
        data={
            'nombre': 'Test User',
            'email': another_user.email,
            'bio': '',
            'avatar_url': '',
        },
        follow_redirects=True,
    )
    db.session.refresh(sample_user)

    assert response.status_code == 200
    assert sample_user.email == 'test@example.com'
    assert Usuario.query.filter_by(email=another_user.email).count() == 1
