from app import db
from models import Comentario, Review, Seguimiento, VotoReview
from tests.conftest import login


def create_review(user, comic, rating=4, text='Una reseña inicial.'):
    review = Review(
        usuario_id=user.id,
        comic_id=comic.id,
        calificacion=rating,
        texto=text,
    )
    db.session.add(review)
    db.session.commit()
    return review


def test_user_can_like_change_and_remove_vote(client, sample_user, another_user, sample_comic):
    review = create_review(another_user, sample_comic)
    login(client)

    response = client.post(f'/review/{review.id}/vote/like', follow_redirects=True)
    db.session.refresh(review)

    assert response.status_code == 200
    assert review.likes == 1
    assert review.dislikes == 0
    assert VotoReview.query.filter_by(review_id=review.id, usuario_id=sample_user.id).count() == 1

    client.post(f'/review/{review.id}/vote/dislike', follow_redirects=True)
    db.session.refresh(review)

    assert review.likes == 0
    assert review.dislikes == 1

    client.post(f'/review/{review.id}/vote/dislike', follow_redirects=True)
    db.session.refresh(review)

    assert review.likes == 0
    assert review.dislikes == 0
    assert VotoReview.query.filter_by(review_id=review.id, usuario_id=sample_user.id).count() == 0


def test_authenticated_user_can_comment_on_review(client, sample_user, another_user, sample_comic):
    review = create_review(another_user, sample_comic)
    login(client)

    response = client.post(
        f'/review/{review.id}/comment',
        data={'texto': 'Buen punto, no lo había pensado.'},
        follow_redirects=True,
    )

    comment = Comentario.query.filter_by(review_id=review.id, usuario_id=sample_user.id).first()
    assert response.status_code == 200
    assert comment is not None
    assert comment.texto == 'Buen punto, no lo había pensado.'


def test_comment_owner_can_delete_comment(client, sample_user, another_user, sample_comic):
    review = create_review(another_user, sample_comic)
    comment = Comentario(review_id=review.id, usuario_id=sample_user.id, texto='Comentario temporal.')
    db.session.add(comment)
    db.session.commit()
    login(client)

    response = client.post(f'/comment/{comment.id}/delete', follow_redirects=True)

    assert response.status_code == 200
    assert Comentario.query.get(comment.id) is None


def test_user_can_follow_and_unfollow_another_user(client, sample_user, another_user):
    login(client)

    response = client.post(f'/perfil/{another_user.id}/follow', follow_redirects=True)
    db.session.refresh(sample_user)
    db.session.refresh(another_user)

    assert response.status_code == 200
    assert Seguimiento.query.filter_by(seguidor_id=sample_user.id, seguido_id=another_user.id).count() == 1
    assert sample_user.siguiendo_count == 1
    assert another_user.seguidores_count == 1

    client.post(f'/perfil/{another_user.id}/follow', follow_redirects=True)
    db.session.refresh(sample_user)
    db.session.refresh(another_user)

    assert Seguimiento.query.filter_by(seguidor_id=sample_user.id, seguido_id=another_user.id).count() == 0
    assert sample_user.siguiendo_count == 0
    assert another_user.seguidores_count == 0


def test_user_cannot_follow_self(client, sample_user):
    login(client)

    response = client.post(f'/perfil/{sample_user.id}/follow', follow_redirects=True)

    assert response.status_code == 200
    assert Seguimiento.query.filter_by(seguidor_id=sample_user.id, seguido_id=sample_user.id).count() == 0
