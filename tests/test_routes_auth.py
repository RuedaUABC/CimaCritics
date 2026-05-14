from models import Usuario


def test_register_creates_user(client):
    response = client.post(
        '/register',
        data={
            'nombre': 'Nuevo Usuario',
            'email': 'nuevo@example.com',
            'password': 'password123',
            'password2': 'password123',
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert Usuario.query.filter_by(email='nuevo@example.com').first() is not None
    assert 'Registro exitoso'.encode('utf-8') in response.data


def test_login_success(client, sample_user):
    response = client.post(
        '/login',
        data={'email': sample_user.email, 'password': 'password123'},
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert sample_user.nombre.encode('utf-8') in response.data


def test_login_rejects_invalid_password(client, sample_user):
    response = client.post(
        '/login',
        data={'email': sample_user.email, 'password': 'bad-password'},
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert 'inv'.encode('utf-8') in response.data
