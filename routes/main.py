from functools import wraps
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app import app, db, login
from models import Usuario, Comic, Review, Genero
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo, Length, NumberRange

# User loader para Flask-Login
@login.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

# Create Admin decorator
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.es_admin:
            flash('No tienes permisos de administrador.', 'error')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

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

class ComicForm(FlaskForm):
    titulo = StringField('Título', validators=[DataRequired(), Length(max=128)])
    escritor = StringField('Escritor', validators=[DataRequired(), Length(max=64)])
    dibujante = StringField('Dibujante', validators=[DataRequired(), Length(max=64)])
    lanzamiento = StringField('Lanzamiento', validators=[Length(max=32)])
    editorial = StringField('Editorial', validators=[Length(max=64)])
    descripcion = TextAreaField('Sinopsis')
    imagen_url = StringField('URL de la Portada', validators=[Length(max=256)])
    generos = StringField('Géneros (separados por comas)', validators=[DataRequired()])
    submit = SubmitField('Guardar Cómic')

# Rutas principales
@app.route('/')
@app.route('/index')
def index():
    """Página principal"""
    comics = Comic.query.order_by(Comic.fecha_creacion.desc()).limit(6).all()
    return render_template('index.html', title='Inicio', comics=comics)

@app.route('/comics')
def comics():
    """Listado de cómics con búsqueda y filtros"""
    page = request.args.get('page', 1, type=int)
    q = request.args.get('q', '')
    genero_id = request.args.get('genero', type=int)
    autor = request.args.get('autor', '')
    editorial = request.args.get('editorial', '')
    sort = request.args.get('sort', 'recent')
    
    per_page = 12
    query = Comic.query
    
    # Búsqueda global (Normal)
    if q:
        query = query.filter(
            db.or_(
                Comic.titulo.ilike(f'%{q}%'),
                Comic.escritor.ilike(f'%{q}%'),
                Comic.dibujante.ilike(f'%{q}%'),
                Comic.editorial.ilike(f'%{q}%'),
                Comic.descripcion.ilike(f'%{q}%')
            )
        )
    
    # Filtros avanzados
    if genero_id:
        query = query.join(Comic.generos).filter(Genero.id == genero_id)
    
    if autor:
        query = query.filter(
            db.or_(
                Comic.escritor.ilike(f'%{autor}%'),
                Comic.dibujante.ilike(f'%{autor}%')
            )
        )
        
    if editorial:
        query = query.filter(Comic.editorial.ilike(f'%{editorial}%'))
        
    # Ordenamiento
    if sort == 'rating':
        query = query.order_by(Comic.promedio_calificacion.desc())
    elif sort == 'title':
        query = query.order_by(Comic.titulo.asc())
    else:  # 'recent'
        query = query.order_by(Comic.fecha_creacion.desc())
        
    comics_paginated = query.paginate(page=page, per_page=per_page, error_out=False)
    generos = Genero.query.order_by(Genero.nombre.asc()).all()

    return render_template('comics.html', title='Cómics',
                         comics=comics_paginated.items,
                         pagination=comics_paginated,
                         generos=generos,
                         filters={
                             'q': q,
                             'genero': genero_id,
                             'autor': autor,
                             'editorial': editorial,
                             'sort': sort
                         })

@app.route('/comics/<int:comic_id>')
def comic_detail(comic_id):
    """Detalle de un cómic"""
    comic = Comic.query.get_or_404(comic_id)
    reviews = Review.query.filter_by(comic_id=comic_id).order_by(Review.fecha_creacion.desc()).all()

    # Calcular promedio si hay reseñas
    if reviews:
        promedio = sum(r.calificacion for r in reviews) / len(reviews)
        comic.promedio_calificacion = round(promedio, 1)

    form = ReviewForm()
    user_has_reviewed = False
    if current_user.is_authenticated:
        user_has_reviewed = Review.query.filter_by(usuario_id=current_user.id, comic_id=comic_id).first() is not None

    return render_template('comic_detail.html', title=comic.titulo,
                         comic=comic, reviews=reviews, form=form, user_has_reviewed=user_has_reviewed)

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

    form = ReviewForm()
    return render_template('perfil.html', title=f'Perfil de {user.nombre}',
                         user=user, reviews=reviews, form=form)

@app.route('/comics/<int:comic_id>/review', methods=['POST'])
@login_required
def add_review(comic_id):
    """Agregar reseña a un cómic (POST-only from Modal)"""
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
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"{getattr(form, field).label.text}: {error}", 'error')

    return redirect(url_for('comic_detail', comic_id=comic_id))

@app.route('/review/<int:review_id>/edit', methods=['POST'])
@login_required
def edit_review(review_id):
    """Editar una reseña existente"""
    review = Review.query.get_or_404(review_id)
    
    # Verificar propiedad
    if review.usuario_id != current_user.id:
        flash('No tienes permiso para editar esta reseña.', 'error')
        return redirect(request.referrer or url_for('comic_detail', comic_id=review.comic_id))
        
    form = ReviewForm()
    if form.validate_on_submit():
        review.calificacion = form.calificacion.data
        review.texto = form.texto.data
        db.session.commit()
        
        # Actualizar promedio del cómic
        comic = Comic.query.get(review.comic_id)
        reviews = Review.query.filter_by(comic_id=comic.id).all()
        if reviews:
            promedio = sum(r.calificacion for r in reviews) / len(reviews)
            comic.promedio_calificacion = round(promedio, 1)
            db.session.commit()
            
        flash('Reseña actualizada correctamente.', 'success')
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"{getattr(form, field).label.text}: {error}", 'error')
                
    return redirect(request.referrer or url_for('comic_detail', comic_id=review.comic_id))

@app.route('/review/<int:review_id>/delete', methods=['POST'])
@login_required
def delete_review(review_id):
    """Eliminar una reseña"""
    review = Review.query.get_or_404(review_id)
    comic_id = review.comic_id
    
    # Verificar propiedad (o si es admin)
    if review.usuario_id != current_user.id and not current_user.es_admin:
        flash('No tienes permiso para eliminar esta reseña.', 'error')
        return redirect(request.referrer or url_for('comic_detail', comic_id=comic_id))
        
    db.session.delete(review)
    db.session.commit()
    
    # Actualizar promedio del cómic
    comic = Comic.query.get(comic_id)
    reviews = Review.query.filter_by(comic_id=comic_id).all()
    if reviews:
        promedio = sum(r.calificacion for r in reviews) / len(reviews)
        comic.promedio_calificacion = round(promedio, 1)
    else:
        comic.promedio_calificacion = 0.0
    db.session.commit()
    
    flash('Reseña eliminada correctamente.', 'success')
    return redirect(request.referrer or url_for('comic_detail', comic_id=comic_id))

# Rutas Admin
@app.route('/admin')
@login_required
@admin_required
def admin_dashboard():
    """Admin Dashboard"""
    # Estadísticas básicas
    total_usuarios = Usuario.query.count()
    total_comics = Comic.query.count()
    total_reviews = Review.query.count()

    # Cómics para listar en la tabla de recientes
    comics_recientes = Comic.query.order_by(Comic.fecha_creacion.desc()).limit(10).all()

    return render_template('admin/dashboard.html', 
                         title='Admin Dashboard',
                         total_usuarios=total_usuarios,
                         total_comics=total_comics,
                         total_reviews=total_reviews,
                         comics_recientes=comics_recientes)

@app.route('/admin/comic/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_comic():
    """Añadir un nuevo cómic al catálogo"""
    form = ComicForm()
    if form.validate_on_submit():
        comic = Comic(
            titulo=form.titulo.data,
            escritor=form.escritor.data,
            dibujante=form.dibujante.data,
            lanzamiento=form.lanzamiento.data,
            editorial=form.editorial.data,
            descripcion=form.descripcion.data,
            imagen_url=form.imagen_url.data
        )
        
        # Procesar géneros (separados por coma)
        generos_nombres = [g.strip() for g in form.generos.data.split(',') if g.strip()]
        for nombre in generos_nombres:
            # Buscar si el género ya existe (case-insensitive)
            genero = Genero.query.filter(db.func.lower(Genero.nombre) == db.func.lower(nombre)).first()
            if not genero:
                # Capitalizar la primera letra del nuevo género si no existe
                nuevo_nombre = nombre.capitalize()
                genero = Genero(nombre=nuevo_nombre)
                db.session.add(genero)
            comic.generos.append(genero)
            
        db.session.add(comic)
        db.session.commit()
        
        flash(f'El cómic "{comic.titulo}" ha sido añadido correctamente al catálogo.', 'success')
        return redirect(url_for('comics'))
        
    return render_template('admin/add_comic.html', title='Añadir Cómic', form=form)