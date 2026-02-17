# 🧪 Estrategia de Testing - Backend

## 1. Tipos de Tests

### 1.1 Unit Tests
Pruebas de funciones individuales y métodos de clase.

**Ejemplos:**
- Validación de modelos
- Funciones utilitarias
- Lógica de negocio pura

### 1.2 Integration Tests
Pruebas de interacción entre componentes.

**Ejemplos:**
- Endpoints de API
- Conexión a base de datos
- Autenticación completa

### 1.3 End-to-End Tests
Pruebas de flujos completos de usuario.

**Ejemplos:**
- Registro → Login → Crear reseña
- Búsqueda y filtrado de cómics

## 2. Herramientas
- **pytest**: Framework principal de testing
- **pytest-cov**: Cobertura de código
- **pytest-flask**: Utilidades para testing de Flask
- **factory-boy**: Creación de datos de prueba

## 3. Estructura de Tests
```
tests/
├── __init__.py
├── conftest.py              # Configuración global
├── test_models.py           # Tests de modelos
├── test_routes_auth.py      # Tests de rutas de auth
├── test_routes_comics.py    # Tests de rutas de cómics
├── test_routes_reviews.py   # Tests de rutas de reseñas
├── test_utils.py            # Tests de utilidades
└── factories/               # Factories para datos de prueba
    ├── __init__.py
    ├── user_factory.py
    ├── comic_factory.py
    └── review_factory.py
```

## 4. Configuración de Base de Datos de Test
```python
# conftest.py
@pytest.fixture(scope='session')
def app():
    app = create_app('testing')
    return app

@pytest.fixture(scope='session')
def db(app):
    with app.app_context():
        db.create_all()
        yield db
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()
```

## 5. Ejemplos de Tests

### Test de Modelo Usuario
```python
def test_usuario_creation(db):
    usuario = Usuario(
        nombre='Test User',
        email='test@example.com',
        contraseña_hash='hashed_password'
    )
    db.session.add(usuario)
    db.session.commit()
    
    assert usuario.id is not None
    assert usuario.nombre == 'Test User'
    assert usuario.es_admin == False
```

### Test de Endpoint de Login
```python
def test_login_success(client, db):
    # Crear usuario de prueba
    usuario = Usuario(
        nombre='Test User',
        email='test@example.com',
        contraseña_hash=generate_password_hash('password123')
    )
    db.session.add(usuario)
    db.session.commit()
    
    # Hacer request de login
    response = client.post('/api/auth/login', json={
        'email': 'test@example.com',
        'password': 'password123'
    })
    
    assert response.status_code == 200
    data = response.get_json()
    assert 'access_token' in data
    assert data['usuario']['email'] == 'test@example.com'
```

## 6. Cobertura de Código
**Objetivo:** Mínimo 80% de cobertura

Comando para ejecutar tests con cobertura:
```bash
pytest --cov=app --cov-report=html
```

## 7. CI/CD
- Tests automáticos en GitHub Actions
- Cobertura reportada en Codecov
- Tests deben pasar antes de merge

## 8. Buenas Prácticas
- Tests independientes y repetibles
- Usar fixtures para datos comunes
- Nombrado descriptivo: `test_should_return_404_when_comic_not_found`
- Un assert por test cuando sea posible
- Mock de servicios externos