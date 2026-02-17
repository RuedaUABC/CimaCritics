from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app import app, db, login
from models import Usuario, Comic, Review
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo, Length, NumberRange

# User loader para Flask-Login
@login.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

# Formularios
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    remember_me = BooleanField('Recordarme')
    submit = SubmitField('Iniciar Sesión')

class RegistrationForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired(), Length(min=2, max=64)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators=[DataRequired(), Length(min=6)])
    password2 = PasswordField('Repetir Contraseña', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Registrarse')

class ReviewForm(FlaskForm):
    calificacion = IntegerField('Calificación (1-5)', validators=[DataRequired(), NumberRange(min=1, max=5)])
    texto = TextAreaField('Reseña', validators=[Length(max=1000)])
    submit = SubmitField('Publicar Reseña')

# Rutas principales
@app.route('/')
@app.route('/index')
def index():
    """Página principal"""
    comics = Comic.query.order_by(Comic.fecha_creacion.desc()).limit(6).all()
    return render_template('index.html', title='Inicio', comics=comics)

@app.route('/comics')
def comics():
    """Listado de cómics"""
    page = request.args.get('page', 1, type=int)
    per_page = 12
    comics_query = Comic.query.order_by(Comic.fecha_creacion.desc())
    comics_paginated = comics_query.paginate(page=page, per_page=per_page, error_out=False)

    return render_template('comics.html', title='Cómics',
                         comics=comics_paginated.items,
                         pagination=comics_paginated)

@app.route('/comics/<int:comic_id>')
def comic_detail(comic_id):
    """Detalle de un cómic"""
    comic = Comic.query.get_or_404(comic_id)
    reviews = Review.query.filter_by(comic_id=comic_id).order_by(Review.fecha_creacion.desc()).all()

    # Calcular promedio si hay reseñas
    if reviews:
        promedio = sum(r.calificacion for r in reviews) / len(reviews)
        comic.promedio_calificacion = round(promedio, 1)

    return render_template('comic_detail.html', title=comic.titulo,
                         comic=comic, reviews=reviews)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Página de login"""
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = Usuario.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('index'))
        else:
            flash('Email o contraseña inválidos', 'error')

    return render_template('login.html', title='Iniciar Sesión', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Página de registro"""
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegistrationForm()
    if form.validate_on_submit():
        if Usuario.query.filter_by(email=form.email.data).first():
            flash('Este email ya está registrado', 'error')
            return redirect(url_for('register'))

        user = Usuario(nombre=form.nombre.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()

        flash('¡Registro exitoso! Ahora puedes iniciar sesión.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html', title='Registrarse', form=form)

@app.route('/logout')
@login_required
def logout():
    """Cerrar sesión"""
    logout_user()
    return redirect(url_for('index'))

@app.route('/perfil/<int:user_id>')
def perfil(user_id):
    """Perfil de usuario"""
    user = Usuario.query.get_or_404(user_id)
    reviews = Review.query.filter_by(usuario_id=user_id).order_by(Review.fecha_creacion.desc()).all()

    return render_template('perfil.html', title=f'Perfil de {user.nombre}',
                         user=user, reviews=reviews)

@app.route('/comics/<int:comic_id>/review', methods=['GET', 'POST'])
@login_required
def add_review(comic_id):
    """Agregar reseña a un cómic"""
    comic = Comic.query.get_or_404(comic_id)

    # Verificar si el usuario ya reseñó este cómic
    existing_review = Review.query.filter_by(usuario_id=current_user.id, comic_id=comic_id).first()
    if existing_review:
        flash('Ya has reseñado este cómic', 'warning')
        return redirect(url_for('comic_detail', comic_id=comic_id))

    form = ReviewForm()
    if form.validate_on_submit():
        review = Review(
            usuario_id=current_user.id,
            comic_id=comic_id,
            calificacion=form.calificacion.data,
            texto=form.texto.data
        )
        db.session.add(review)
        db.session.commit()

        # Actualizar promedio del cómic
        reviews = Review.query.filter_by(comic_id=comic_id).all()
        if reviews:
            promedio = sum(r.calificacion for r in reviews) / len(reviews)
            comic.promedio_calificacion = round(promedio, 1)
            db.session.commit()

        flash('¡Reseña publicada exitosamente!', 'success')
        return redirect(url_for('comic_detail', comic_id=comic_id))

    return render_template('add_review.html', title=f'Reseñar {comic.titulo}',
                         form=form, comic=comic)