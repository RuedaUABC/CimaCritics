from app import db
from models import Comentario, Reporte, Review
from tests.conftest import login


def create_review(user, comic, text='Contenido reportable.'):
    review = Review(usuario_id=user.id, comic_id=comic.id, calificacion=3, texto=text)
    db.session.add(review)
    db.session.commit()
    return review


def test_user_can_report_review(client, sample_user, another_user, sample_comic):
    review = create_review(another_user, sample_comic)
    login(client)

    response = client.post(
        f'/report/review/{review.id}',
        data={'motivo': 'spam', 'descripcion': 'Parece publicidad.'},
        follow_redirects=True,
    )

    report = Reporte.query.filter_by(
        usuario_id=sample_user.id,
        contenido_tipo='review',
        contenido_id=review.id,
    ).first()
    assert response.status_code == 200
    assert report is not None
    assert report.estado == 'pendiente'
    assert report.motivo == 'spam'


def test_duplicate_pending_report_is_not_created(client, sample_user, another_user, sample_comic):
    review = create_review(another_user, sample_comic)
    login(client)
    data = {'motivo': 'ofensivo', 'descripcion': 'Texto agresivo.'}

    client.post(f'/report/review/{review.id}', data=data, follow_redirects=True)
    client.post(f'/report/review/{review.id}', data=data, follow_redirects=True)

    assert Reporte.query.filter_by(
        usuario_id=sample_user.id,
        contenido_tipo='review',
        contenido_id=review.id,
        estado='pendiente',
    ).count() == 1


def test_user_can_report_comment(client, sample_user, another_user, sample_comic):
    review = create_review(another_user, sample_comic)
    comment = Comentario(review_id=review.id, usuario_id=another_user.id, texto='Comentario reportable.')
    db.session.add(comment)
    db.session.commit()
    login(client)

    response = client.post(
        f'/report/comentario/{comment.id}',
        data={'motivo': 'acoso', 'descripcion': ''},
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert Reporte.query.filter_by(contenido_tipo='comentario', contenido_id=comment.id).count() == 1


def test_regular_user_cannot_open_reports_panel(client, sample_user):
    login(client)

    response = client.get('/admin/reports', follow_redirects=True)

    assert response.status_code == 200
    assert 'permisos de moderación'.encode('utf-8') in response.data


def test_moderator_can_open_reports_panel(client, moderator_user, another_user, sample_comic):
    review = create_review(another_user, sample_comic)
    report = Reporte(usuario_id=another_user.id, contenido_tipo='review', contenido_id=review.id, motivo='spam')
    db.session.add(report)
    db.session.commit()
    login(client, email=moderator_user.email, password='mod123')

    response = client.get('/admin/reports')

    assert response.status_code == 200
    assert b'Moderaci' in response.data
    assert b'spam' in response.data


def test_admin_can_resolve_report(client, admin_user, sample_user, another_user, sample_comic):
    review = create_review(another_user, sample_comic)
    report = Reporte(usuario_id=sample_user.id, contenido_tipo='review', contenido_id=review.id, motivo='spam')
    db.session.add(report)
    db.session.commit()
    login(client, email=admin_user.email, password='admin123')

    response = client.post(f'/admin/reports/{report.id}/resuelto', follow_redirects=True)
    db.session.refresh(report)

    assert response.status_code == 200
    assert report.estado == 'resuelto'
