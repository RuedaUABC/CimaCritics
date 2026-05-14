from functools import wraps
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app import app, db, login
from models import Usuario, Comic, Review, Genero, Seguimiento, Comentario, VotoReview, Reporte, ComicGuardado
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, IntegerField, SelectField
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

def moderator_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not (current_user.es_admin or current_user.es_moderador):
            flash('No tienes permisos de moderación.', 'error')
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

class ProfileForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired(), Length(min=2, max=64)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    bio = TextAreaField('Biografía', validators=[Length(max=500)])
    avatar_url = StringField('URL de avatar', validators=[Length(max=256)])
    submit = SubmitField('Guardar perfil')

class ReviewForm(FlaskForm):
    calificacion = IntegerField('Calificación (1-5)', validators=[DataRequired(), NumberRange(min=1, max=5)])
    texto = TextAreaField('Reseña', validators=[Length(max=1000)])
    submit = SubmitField('Publicar Reseña')

class CommentForm(FlaskForm):
    texto = TextAreaField('Comentario', validators=[DataRequired(), Length(min=2, max=500)])
    submit = SubmitField('Comentar')

class ReportForm(FlaskForm):
    motivo = SelectField('Motivo', choices=[
        ('spam', 'Spam'),
        ('ofensivo', 'Contenido ofensivo'),
        ('spoiler', 'Spoiler sin aviso'),
        ('acoso', 'Acoso'),
        ('otro', 'Otro'),
    ], validators=[DataRequired()])
    descripcion = TextAreaField('Descripción', validators=[Length(max=500)])
    submit = SubmitField('Enviar reporte')

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

def redirect_back(default_endpoint='index', **kwargs):
    return redirect(request.referrer or url_for(default_endpoint, **kwargs))

def refresh_follow_counts(*users):
    for user in users:
        user.seguidores_count = Seguimiento.query.filter_by(seguido_id=user.id).count()
        user.siguiendo_count = Seguimiento.query.filter_by(seguidor_id=user.id).count()

def recalculate_review_votes(review):
    review.likes = VotoReview.query.filter_by(review_id=review.id, tipo='like').count()
    review.dislikes = VotoReview.query.filter_by(review_id=review.id, tipo='dislike').count()

def get_reportable_content(content_type, content_id):
    if content_type == 'review':
        return Review.query.get_or_404(content_id)
    if content_type == 'comentario':
        return Comentario.query.get_or_404(content_id)
    return None

def get_content_redirect(content_type, content):
    if content_type == 'review':
        return url_for('comic_detail', comic_id=content.comic_id)
    if content_type == 'comentario':
        return url_for('comic_detail', comic_id=content.review.comic_id)
    return url_for('index')

def build_report_item(report):
    target = None
    target_author = None
    target_text = 'Contenido no disponible'
    target_url = url_for('index')

    if report.contenido_tipo == 'review':
        target = Review.query.get(report.contenido_id)
        if target:
            target_author = target.autor
            target_text = target.texto or f'Reseña con {target.calificacion} estrellas'
            target_url = url_for('comic_detail', comic_id=target.comic_id)
    elif report.contenido_tipo == 'comentario':
        target = Comentario.query.get(report.contenido_id)
        if target:
            target_author = target.autor
            target_text = target.texto
            target_url = url_for('comic_detail', comic_id=target.review.comic_id)

    return {
        'report': report,
        'target': target,
        'target_author': target_author,
        'target_text': target_text,
        'target_url': target_url,
    }

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
    comment_form = CommentForm()
    report_form = ReportForm()
    user_has_reviewed = False
    user_has_saved = False
    if current_user.is_authenticated:
        user_has_reviewed = Review.query.filter_by(usuario_id=current_user.id, comic_id=comic_id).first() is not None
        user_has_saved = ComicGuardado.query.filter_by(usuario_id=current_user.id, comic_id=comic_id).first() is not None

    return render_template('comic_detail.html', title=comic.titulo,
                         comic=comic, reviews=reviews, form=form, comment_form=comment_form,
                         report_form=report_form,
                         user_has_reviewed=user_has_reviewed, user_has_saved=user_has_saved)

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
    seguidores = Seguimiento.query.filter_by(seguido_id=user_id).all()
    siguiendo = Seguimiento.query.filter_by(seguidor_id=user_id).all()
    comics_guardados = ComicGuardado.query.filter_by(usuario_id=user_id).order_by(ComicGuardado.fecha_guardado.desc()).all()
    comment_count = Comentario.query.filter_by(usuario_id=user_id).count()
    is_following = False
    if current_user.is_authenticated and current_user.id != user_id:
        is_following = Seguimiento.query.filter_by(
            seguidor_id=current_user.id,
            seguido_id=user_id
        ).first() is not None

    form = ReviewForm()
    return render_template('perfil.html', title=f'Perfil de {user.nombre}',
                         user=user, reviews=reviews, form=form, comment_count=comment_count,
                         seguidores=seguidores, siguiendo=siguiendo, comics_guardados=comics_guardados,
                         is_following=is_following)

@app.route('/perfil/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    """Editar datos básicos del perfil del usuario actual."""
    form = ProfileForm()
    if form.validate_on_submit():
        existing_user = Usuario.query.filter(
            Usuario.email == form.email.data,
            Usuario.id != current_user.id
        ).first()
        if existing_user:
            flash('Ese email ya está registrado por otro usuario.', 'error')
            return redirect(url_for('edit_profile'))

        current_user.nombre = form.nombre.data.strip()
        current_user.email = form.email.data.strip().lower()
        current_user.bio = form.bio.data.strip() if form.bio.data else None
        current_user.avatar_url = form.avatar_url.data.strip() if form.avatar_url.data else None
        db.session.commit()
        flash('Perfil actualizado correctamente.', 'success')
        return redirect(url_for('perfil', user_id=current_user.id))

    if request.method == 'GET':
        form.nombre.data = current_user.nombre
        form.email.data = current_user.email
        form.bio.data = current_user.bio
        form.avatar_url.data = current_user.avatar_url

    return render_template('edit_profile.html', title='Editar Perfil', form=form)

@app.route('/comics/<int:comic_id>/save', methods=['POST'])
@login_required
def toggle_saved_comic(comic_id):
    """Guardar o retirar un cómic de la biblioteca personal."""
    comic = Comic.query.get_or_404(comic_id)
    saved = ComicGuardado.query.filter_by(usuario_id=current_user.id, comic_id=comic.id).first()

    if saved:
        db.session.delete(saved)
        flash(f'"{comic.titulo}" fue retirado de tu biblioteca.', 'info')
    else:
        db.session.add(ComicGuardado(usuario_id=current_user.id, comic_id=comic.id))
        flash(f'"{comic.titulo}" fue guardado en tu biblioteca.', 'success')

    db.session.commit()
    return redirect_back('comic_detail', comic_id=comic.id)

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
        
    Comentario.query.filter_by(review_id=review.id).delete()
    VotoReview.query.filter_by(review_id=review.id).delete()
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

@app.route('/review/<int:review_id>/vote/<vote_type>', methods=['POST'])
@login_required
def vote_review(review_id, vote_type):
    """Registrar, cambiar o retirar like/dislike de una reseña."""
    if vote_type not in ('like', 'dislike'):
        flash('Tipo de voto inválido.', 'error')
        return redirect_back('index')

    review = Review.query.get_or_404(review_id)
    existing_vote = VotoReview.query.filter_by(
        review_id=review.id,
        usuario_id=current_user.id
    ).first()

    if existing_vote and existing_vote.tipo == vote_type:
        db.session.delete(existing_vote)
        flash('Tu voto fue retirado.', 'info')
    elif existing_vote:
        existing_vote.tipo = vote_type
        flash('Tu voto fue actualizado.', 'success')
    else:
        db.session.add(VotoReview(review_id=review.id, usuario_id=current_user.id, tipo=vote_type))
        flash('Tu voto fue registrado.', 'success')

    db.session.flush()
    recalculate_review_votes(review)
    db.session.commit()
    return redirect_back('comic_detail', comic_id=review.comic_id)

@app.route('/review/<int:review_id>/comment', methods=['POST'])
@login_required
def add_comment(review_id):
    """Agregar un comentario a una reseña."""
    review = Review.query.get_or_404(review_id)
    form = CommentForm()

    if form.validate_on_submit():
        comment = Comentario(
            review_id=review.id,
            usuario_id=current_user.id,
            texto=form.texto.data.strip()
        )
        db.session.add(comment)
        db.session.commit()
        flash('Comentario publicado correctamente.', 'success')
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"{getattr(form, field).label.text}: {error}", 'error')

    return redirect_back('comic_detail', comic_id=review.comic_id)

@app.route('/comment/<int:comment_id>/delete', methods=['POST'])
@login_required
def delete_comment(comment_id):
    """Eliminar un comentario propio o como admin."""
    comment = Comentario.query.get_or_404(comment_id)
    comic_id = comment.review.comic_id

    if comment.usuario_id != current_user.id and not current_user.es_admin:
        flash('No tienes permiso para eliminar este comentario.', 'error')
        return redirect_back('comic_detail', comic_id=comic_id)

    db.session.delete(comment)
    db.session.commit()
    flash('Comentario eliminado correctamente.', 'success')
    return redirect_back('comic_detail', comic_id=comic_id)

@app.route('/report/<content_type>/<int:content_id>', methods=['POST'])
@login_required
def report_content(content_type, content_id):
    """Crear un reporte de una reseña o comentario."""
    content = get_reportable_content(content_type, content_id)
    if content is None:
        flash('No se puede reportar ese contenido.', 'error')
        return redirect(url_for('index'))

    form = ReportForm()
    if not form.validate_on_submit():
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"{getattr(form, field).label.text}: {error}", 'error')
        return redirect(get_content_redirect(content_type, content))

    existing_report = Reporte.query.filter_by(
        usuario_id=current_user.id,
        contenido_tipo=content_type,
        contenido_id=content_id,
        estado='pendiente'
    ).first()
    if existing_report:
        flash('Ya tienes un reporte pendiente para este contenido.', 'warning')
        return redirect(get_content_redirect(content_type, content))

    report = Reporte(
        usuario_id=current_user.id,
        contenido_tipo=content_type,
        contenido_id=content_id,
        motivo=form.motivo.data,
        descripcion=form.descripcion.data.strip() if form.descripcion.data else None,
    )
    db.session.add(report)
    db.session.commit()

    flash('Reporte enviado a moderación.', 'success')
    return redirect(get_content_redirect(content_type, content))

@app.route('/perfil/<int:user_id>/follow', methods=['POST'])
@login_required
def toggle_follow(user_id):
    """Seguir o dejar de seguir a un usuario."""
    user = Usuario.query.get_or_404(user_id)
    if user.id == current_user.id:
        flash('No puedes seguirte a ti mismo.', 'warning')
        return redirect(url_for('perfil', user_id=user_id))

    existing_follow = Seguimiento.query.filter_by(
        seguidor_id=current_user.id,
        seguido_id=user.id
    ).first()

    if existing_follow:
        db.session.delete(existing_follow)
        flash(f'Has dejado de seguir a {user.nombre}.', 'info')
    else:
        db.session.add(Seguimiento(seguidor_id=current_user.id, seguido_id=user.id))
        flash(f'Ahora sigues a {user.nombre}.', 'success')

    db.session.flush()
    refresh_follow_counts(current_user, user)
    db.session.commit()
    return redirect(url_for('perfil', user_id=user_id))

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
    total_reportes_pendientes = Reporte.query.filter_by(estado='pendiente').count()

    # Cómics para listar en la tabla de recientes
    comics_recientes = Comic.query.order_by(Comic.fecha_creacion.desc()).limit(10).all()
    reportes_recientes = Reporte.query.order_by(Reporte.fecha_reporte.desc()).limit(5).all()

    return render_template('admin/dashboard.html', 
                         title='Admin Dashboard',
                         total_usuarios=total_usuarios,
                         total_comics=total_comics,
                         total_reviews=total_reviews,
                         total_reportes_pendientes=total_reportes_pendientes,
                         comics_recientes=comics_recientes,
                         report_items=[build_report_item(report) for report in reportes_recientes])

@app.route('/admin/reports')
@login_required
@moderator_required
def admin_reports():
    """Panel de moderación de reportes."""
    estado = request.args.get('estado', 'pendiente')
    query = Reporte.query
    if estado != 'todos':
        query = query.filter_by(estado=estado)
    reportes = query.order_by(Reporte.fecha_reporte.desc()).all()
    return render_template('admin/reports.html',
                         title='Reportes',
                         estado=estado,
                         report_items=[build_report_item(report) for report in reportes])

@app.route('/admin/reports/<int:report_id>/<action>', methods=['POST'])
@login_required
@moderator_required
def update_report(report_id, action):
    """Actualizar estado de un reporte."""
    if action not in ('resuelto', 'rechazado', 'pendiente'):
        flash('Acción de moderación inválida.', 'error')
        return redirect(url_for('admin_reports'))

    report = Reporte.query.get_or_404(report_id)
    report.estado = action
    db.session.commit()
    flash(f'Reporte marcado como {action}.', 'success')
    return redirect(request.referrer or url_for('admin_reports'))

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

@app.route('/admin/comic/edit/<int:comic_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_comic(comic_id):
    """Editar un cómic existente"""
    comic = Comic.query.get_or_404(comic_id)
    form = ComicForm()
    
    if form.validate_on_submit():
        comic.titulo = form.titulo.data
        comic.escritor = form.escritor.data
        comic.dibujante = form.dibujante.data
        comic.lanzamiento = form.lanzamiento.data
        comic.editorial = form.editorial.data
        comic.descripcion = form.descripcion.data
        comic.imagen_url = form.imagen_url.data
        
        # Procesar géneros
        generos_nombres = [g.strip() for g in form.generos.data.split(',') if g.strip()]
        comic.generos.clear()  # Limpiar géneros existentes
        for nombre in generos_nombres:
            genero = Genero.query.filter(db.func.lower(Genero.nombre) == db.func.lower(nombre)).first()
            if not genero:
                nuevo_nombre = nombre.capitalize()
                genero = Genero(nombre=nuevo_nombre)
                db.session.add(genero)
            comic.generos.append(genero)
        
        db.session.commit()
        flash(f'El cómic "{comic.titulo}" ha sido actualizado correctamente.', 'success')
        return redirect(url_for('admin_dashboard'))
    
    # Prellenar el formulario con datos existentes
    if request.method == 'GET':
        form.titulo.data = comic.titulo
        form.escritor.data = comic.escritor
        form.dibujante.data = comic.dibujante
        form.lanzamiento.data = comic.lanzamiento
        form.editorial.data = comic.editorial
        form.descripcion.data = comic.descripcion
        form.imagen_url.data = comic.imagen_url
        form.generos.data = ', '.join([g.nombre for g in comic.generos])
    
    form.submit.label.text = 'Actualizar Cómic'
    return render_template('admin/edit_comic.html', title='Editar Cómic', form=form, comic=comic)

@app.route('/admin/comic/delete/<int:comic_id>', methods=['POST'])
@login_required
@admin_required
def delete_comic(comic_id):
    """Eliminar un cómic"""
    comic = Comic.query.get_or_404(comic_id)
    titulo = comic.titulo
    
    # Eliminar dependencias asociadas primero (por integridad referencial)
    review_ids = [review.id for review in Review.query.filter_by(comic_id=comic_id).all()]
    if review_ids:
        Comentario.query.filter(Comentario.review_id.in_(review_ids)).delete(synchronize_session=False)
        VotoReview.query.filter(VotoReview.review_id.in_(review_ids)).delete(synchronize_session=False)
        Review.query.filter(Review.id.in_(review_ids)).delete(synchronize_session=False)
    ComicGuardado.query.filter_by(comic_id=comic_id).delete()
    
    db.session.delete(comic)
    db.session.commit()
    
    flash(f'El cómic "{titulo}" y sus reseñas asociadas han sido eliminados.', 'success')
    return redirect(url_for('admin_dashboard'))
