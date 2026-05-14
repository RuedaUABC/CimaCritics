from models import Comic, Review
from tests.conftest import login


def test_comics_page_lists_seeded_comic(client, sample_comic):
    response = client.get('/comics')

    assert response.status_code == 200
    assert b'Watchmen' in response.data


def test_comics_search_filters_by_title(client, app, sample_comic):
    other = Comic(titulo='Sandman', escritor='Neil Gaiman', dibujante='Sam Kieth')
    from app import db

    db.session.add(other)
    db.session.commit()

    response = client.get('/comics?q=Watchmen')

    assert response.status_code == 200
    assert b'Watchmen' in response.data
    assert b'Sandman' not in response.data


def test_authenticated_user_can_add_review(client, sample_user, sample_comic):
    login(client)

    response = client.post(
        f'/comics/{sample_comic.id}/review',
        data={'calificacion': 5, 'texto': 'Excelente lectura.'},
        follow_redirects=True,
    )

    review = Review.query.filter_by(usuario_id=sample_user.id, comic_id=sample_comic.id).first()
    assert response.status_code == 200
    assert review is not None
    assert sample_comic.promedio_calificacion == 5.0


def test_duplicate_review_is_rejected(client, sample_user, sample_comic):
    login(client)
    data = {'calificacion': 4, 'texto': 'Muy bueno.'}

    client.post(f'/comics/{sample_comic.id}/review', data=data, follow_redirects=True)
    response = client.post(f'/comics/{sample_comic.id}/review', data=data, follow_redirects=True)

    assert response.status_code == 200
    assert Review.query.filter_by(usuario_id=sample_user.id, comic_id=sample_comic.id).count() == 1


def test_admin_dashboard_requires_admin(client, sample_user):
    login(client)

    response = client.get('/admin', follow_redirects=True)

    assert response.status_code == 200
    assert 'permisos de administrador'.encode('utf-8') in response.data


def test_admin_dashboard_renders_for_admin(client, admin_user):
    login(client, email=admin_user.email, password='admin123')

    response = client.get('/admin')

    assert response.status_code == 200
    assert 'Dashboard de Control'.encode('utf-8') in response.data
