from models import Comic, Genero, Review, Usuario


def test_usuario_password_hashing(app):
    user = Usuario(nombre='Ada', email='ada@example.com')
    user.set_password('secret123')

    assert user.contraseña_hash != 'secret123'
    assert user.check_password('secret123')
    assert not user.check_password('wrong-password')


def test_comic_can_have_multiple_generos(app):
    comic = Comic(titulo='Maus', escritor='Art Spiegelman', dibujante='Art Spiegelman')
    comic.generos.append(Genero(nombre='Historia'))
    comic.generos.append(Genero(nombre='Drama'))

    assert [genero.nombre for genero in comic.generos] == ['Historia', 'Drama']


def test_review_repr_includes_rating(app, sample_user, sample_comic):
    review = Review(usuario_id=sample_user.id, comic_id=sample_comic.id, calificacion=5)

    assert '5 estrellas' in repr(review)
