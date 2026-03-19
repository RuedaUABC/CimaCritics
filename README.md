# CimaCritics

## 📖 Visión del Proyecto
CimaCritics es una plataforma web dedicada a críticas y reseñas de cómics, donde usuarios pueden explorar, calificar y compartir opiniones sobre sus cómics favoritos. El proyecto busca crear una comunidad apasionada por los cómics, facilitando el descubrimiento de nuevas obras y el intercambio de opiniones.

## 🎯 Objetivos
- Proporcionar una plataforma intuitiva para reseñas de cómics
- Cubrir cómics de Marvel, DC, independientes y editoriales mexicanas
- Construir una comunidad activa de lectores y críticos
- Ofrecer herramientas de búsqueda y filtrado avanzadas

## 🛠️ Stack Tecnológico
- **Backend**: Flask 3.0.0 + SQLAlchemy 2.0
- **Base de Datos**: SQLite (desarrollo) / PostgreSQL (producción)
- **Autenticación**: Flask-Login + Werkzeug
- **Formularios**: Flask-WTF
- **Migraciones**: Flask-Migrate (Alembic)
- **Frontend**: HTML5 + CSS3 + JavaScript (planeado)
- **Testing**: pytest (futuro)
- **Documentación**: Markdown (Obsidian-style)

## 📁 Estructura del Proyecto
```
CimaCritics/
├── app.py                 # Aplicación principal Flask
├── config.py              # Configuraciones de la app
├── requirements.txt       # Dependencias Python
├── .flaskenv              # Variables de entorno Flask
├── models/                # Modelos SQLAlchemy
│   └── __init__.py        # Definición de modelos
├── routes/                # Endpoints (futuro)
├── templates/             # Plantillas HTML (futuro)
├── static/                # Assets CSS/JS (futuro)
├── utils/                 # Utilidades
│   └── seed.py            # Datos iniciales
├── migrations/            # Migraciones de BD
├── instance/              # Archivos sensibles (BD)
├── tests/                 # Tests (futuro)
└── docs/                  # Documentación completa
    ├── Dashboard.md
    ├── Requerimientos/
    ├── Diseño/
    ├── Backend/
    ├── Frontend/
    ├── Testing/
    └── Deployment/
```

## 🚀 Instalación y Configuración

### Prerrequisitos
- Python 3.8+
- pip
- Virtualenv (recomendado)

### Instalación
```bash
# Clonar repositorio
git clone https://github.com/RuedaUABC/CimaCritics.git
cd CimaCritics

# Crear entorno virtual
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# o venv\Scripts\activate en Windows

# Instalar dependencias
pip install -r requirements.txt

# Configurar base de datos
flask db upgrade

# Poblar con datos iniciales
python utils/seed.py
```

### Ejecutar la aplicación
```bash
# Activar entorno virtual
source venv/bin/activate

# Ejecutar servidor de desarrollo
flask run

# La aplicación estará disponible en http://localhost:5000
```

## 🗄️ Base de Datos

### Modelos Implementados
- **Usuario**: Autenticación, perfiles, roles (admin/moderador)
- **Comic**: Información de cómics con metadatos
- **Review**: Reseñas con calificación 1-5 y likes/dislikes
- **Seguimiento**: Sistema de seguidores
- **Reporte**: Moderación de contenido
- **Comentario**: Comentarios en reseñas

### Migraciones
```bash
# Crear nueva migración
flask db migrate -m "Descripción del cambio"

# Aplicar migraciones
flask db upgrade

# Revertir migración
flask db downgrade
```

## 📚 Documentación
- **[Dashboard](docs/Dashboard.md)**: Resumen del proyecto
- **[Arquitectura](docs/Diseño/Arquitectura.md)**: Diseño técnico
- **[Modelos](docs/Backend/Modelos.md)**: Esquema de base de datos
- **[Autenticación](docs/Backend/Autenticación.md)**: Sistema de usuarios
- **[APIs](docs/Backend/APIs.md)**: Endpoints planificados
- **[Requerimientos](docs/Requerimientos/)**: Especificaciones funcionales

## 📞 Contacto
- **Email**: rueda.jorge@uabc.edu.mx
- **GitHub**: [https://github.com/RuedaUABC/CimaCritics](https://github.com/RuedaUABC/CimaCritics)
