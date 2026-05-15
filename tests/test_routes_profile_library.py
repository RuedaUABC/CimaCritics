from app import db
from models import Comic, ComicGuardado, Usuario
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


def test_user_can_save_comic_in_separate_and_custom_lists(client, app, sample_user, sample_comic):
    """La biblioteca documentada como "Mis listas" permite listas separadas."""
    custom_comic = Comic(
        titulo='Saga',
        escritor='Brian K. Vaughan',
        dibujante='Fiona Staples',
        lanzamiento='2012',
        editorial='Image Comics',
        descripcion='Opera espacial familiar.',
    )
    db.session.add(custom_comic)
    db.session.commit()
    login(client)

    leyendo_response = client.post(
        f'/comics/{sample_comic.id}/save',
        data={'lista': 'Leyendo'},
        follow_redirects=True,
    )
    custom_response = client.post(
        f'/comics/{custom_comic.id}/save',
        data={'lista': 'Club del viernes'},
        follow_redirects=True,
    )

    assert leyendo_response.status_code == 200
    assert custom_response.status_code == 200
    assert ComicGuardado.query.filter_by(
        usuario_id=sample_user.id,
        comic_id=sample_comic.id,
        lista='Leyendo',
    ).count() == 1
    assert ComicGuardado.query.filter_by(
        usuario_id=sample_user.id,
        comic_id=custom_comic.id,
        lista='Club del viernes',
    ).count() == 1

    profile_response = client.get(f'/perfil/{sample_user.id}')

    assert b'Mis listas' in profile_response.data
    assert 'Leyendo'.encode('utf-8') in profile_response.data
    assert 'Club del viernes'.encode('utf-8') in profile_response.data
    assert sample_comic.titulo.encode('utf-8') in profile_response.data
    assert custom_comic.titulo.encode('utf-8') in profile_response.data


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
