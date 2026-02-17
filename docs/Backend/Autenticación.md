# 🔐 Sistema de Autenticación - Backend

## 1. Tecnologías Utilizadas
- **JWT (JSON Web Tokens)**: Para tokens de acceso
- **bcrypt**: Para hashing de contraseñas
- **Flask-JWT-Extended**: Extensión para manejo de JWT en Flask

## 2. Flujo de Autenticación

### 2.1 Registro
1. Usuario envía datos (nombre, email, password)
2. Validar que email no exista
3. Hash de contraseña con bcrypt
4. Crear usuario en base de datos
5. Generar token JWT
6. Retornar token y datos de usuario

### 2.2 Login
1. Usuario envía email y password
2. Buscar usuario por email
3. Verificar contraseña con bcrypt
4. Generar token JWT
5. Retornar token y datos de usuario

### 2.3 Verificación de Token
1. Extraer token del header Authorization
2. Decodificar y validar token
3. Obtener usuario de la base de datos
4. Adjuntar usuario al contexto de la request

## 3. Decoradores de Protección

### @jwt_required()
Requiere token válido para acceder al endpoint.

```python
@app.route('/api/protected')
@jwt_required()
def protected_route():
    current_user = get_jwt_identity()
    return {'message': f'Hola {current_user}'}
```

### @admin_required()
Requiere que el usuario sea administrador.

```python
def admin_required(fn):
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        user_id = get_jwt_identity()
        user = Usuario.query.get(user_id)
        if not user.es_admin:
            abort(403, 'Acceso denegado')
        return fn(*args, **kwargs)
    return wrapper
```

## 4. Configuración JWT
```python
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'dev-secret-key')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
```

## 5. Manejo de Errores de Autenticación
- **Token expirado**: 401 Unauthorized
- **Token inválido**: 401 Unauthorized
- **Usuario no encontrado**: 404 Not Found
- **Contraseña incorrecta**: 401 Unauthorized
- **Acceso denegado**: 403 Forbidden

## 6. Seguridad Adicional
- **Rate limiting**: Máximo 5 intentos de login por minuto por IP
- **Validación de entrada**: Email válido, contraseña mínima 8 caracteres
- **Sanitización**: Prevenir inyección SQL y XSS
- **Logs**: Registrar intentos de login fallidos

## 7. Refresh Tokens (Futuro)
Para mantener sesiones largas sin requerir re-login frecuente:
- Token de acceso (corto, 15 min)
- Token de refresh (largo, 7 días)
- Endpoint `/api/auth/refresh` para renovar tokens