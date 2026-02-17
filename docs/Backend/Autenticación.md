# 🔐 Sistema de Autenticación - Backend

## Implementación Actual

Se utiliza **Flask-Login** para el manejo de sesiones de usuario, con almacenamiento de contraseñas hasheadas usando Werkzeug.

## 1. Tecnologías Utilizadas
- **Flask-Login**: Manejo de sesiones de usuario
- **Werkzeug**: Hashing de contraseñas (generate_password_hash, check_password_hash)
- **Flask-WTF**: Formularios seguros con CSRF protection

## 2. Modelo Usuario (UserMixin)

```python
from flask_login import UserMixin

class Usuario(UserMixin, db.Model):
    # ... campos definidos en modelos ...

    def set_password(self, password):
        self.contraseña_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.contraseña_hash, password)

    def get_id(self):
        return str(self.id)
```

## 3. Configuración en app.py

```python
from flask_login import LoginManager

login = LoginManager(app)
login.login_view = 'login'  # Nombre de la ruta de login
login.login_message = 'Por favor inicia sesión para acceder a esta página.'
login.login_message_category = 'info'
```

## 4. Funciones de Carga de Usuario

```python
@login.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))
```

## 5. Rutas de Autenticación

### Login
```python
from flask import request, flash, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = Usuario.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user, remember=True)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('index'))
        else:
            flash('Email o contraseña inválidos', 'error')

    return render_template('login.html')
```

### Logout
```python
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))
```

### Registro
```python
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if request.method == 'POST':
        nombre = request.form.get('nombre')
        email = request.form.get('email')
        password = request.form.get('password')

        if Usuario.query.filter_by(email=email).first():
            flash('Email ya registrado', 'error')
            return redirect(url_for('register'))

        user = Usuario(nombre=nombre, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        flash('Registro exitoso. Ahora puedes iniciar sesión.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')
```

## 6. Decoradores de Protección

### @login_required
Requiere usuario autenticado:
```python
from flask_login import login_required

@app.route('/perfil')
@login_required
def perfil():
    return render_template('perfil.html', user=current_user)
```

### Verificación de Roles
```python
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.es_admin:
            flash('Acceso denegado. Se requieren permisos de administrador.', 'error')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/admin')
@login_required
@admin_required
def admin_panel():
    return render_template('admin.html')
```

## 7. Variables Globales en Templates

Flask-Login proporciona `current_user` en todos los templates:
```html
{% if current_user.is_authenticated %}
  <p>Hola, {{ current_user.nombre }}!</p>
  <a href="{{ url_for('logout') }}">Cerrar sesión</a>
{% else %}
  <a href="{{ url_for('login') }}">Iniciar sesión</a>
{% endif %}
```

## 8. Seguridad Implementada

### Hashing de Contraseñas
- Usa PBKDF2 con salt (Werkzeug)
- Longitud de hash: 128 caracteres
- Verificación segura contra timing attacks

### Sesiones
- Sesiones seguras con SECRET_KEY
- Opción "recordar" para sesiones persistentes
- Protección CSRF con Flask-WTF

### Validación
- Email único en registro
- Longitud mínima de contraseña (implementar en forms)
- Sanitización de inputs

## 9. Manejo de Errores

### Errores de Autenticación
- **Usuario no encontrado**: Flash message "Email o contraseña inválidos"
- **Contraseña incorrecta**: Flash message "Email o contraseña inválidos"
- **Acceso no autorizado**: Redirect con flash "Acceso denegado"

### Estados HTTP
- 200: Login/registro exitoso
- 302: Redirects apropiados
- 403: Acceso denegado (para APIs futuras)

## 10. Configuración de Seguridad

En `config.py`:
```python
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'tu_clave_secreta_aqui'
    # ... otras configs ...
```

## 11. Próximas Mejoras (Futuro)
- **Rate limiting**: Limitar intentos de login fallidos
- **Verificación de email**: Confirmación por email
- **2FA**: Autenticación de dos factores
- **OAuth**: Login con Google, GitHub, etc.
- **Sesiones inactivas**: Logout automático por inactividad