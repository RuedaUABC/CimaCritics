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

### Seeders
Datos iniciales incluyen:
- 5 usuarios de ejemplo (uno administrador)
- 5 cómics clásicos
- Reseñas de ejemplo

## 🔐 Autenticación
- Sistema de login/registro con Flask-Login
- Hashing seguro de contraseñas (PBKDF2)
- Sesiones persistentes
- Roles de usuario (normal, moderador, admin)

## 📊 Estado del Desarrollo

### ✅ Completado
- **Configuración del proyecto**: Estructura, virtualenv, dependencias
- **Base de datos**: Modelos SQLAlchemy, migraciones, seeders
- **Autenticación**: Sistema de usuarios con Flask-Login
- **Documentación**: Arquitectura, modelos, APIs planificadas

### 🔄 En Progreso
- **Rutas básicas**: Endpoints para login/registro
- **Templates HTML**: Interfaz de usuario
- **Estilos CSS**: Diseño responsive

### 📋 Próximas Fases
- **Fase 2**: Interfaz de usuario y navegación
- **Fase 3**: Sistema de reseñas y calificaciones
- **Fase 4**: Funcionalidades sociales (seguidores, comentarios)
- **Fase 5**: Moderación y administración
- **Fase 6**: Testing y optimización

## 📚 Documentación
- **[Dashboard](docs/Dashboard.md)**: Resumen del proyecto
- **[Arquitectura](docs/Diseño/Arquitectura.md)**: Diseño técnico
- **[Modelos](docs/Backend/Modelos.md)**: Esquema de base de datos
- **[Autenticación](docs/Backend/Autenticación.md)**: Sistema de usuarios
- **[APIs](docs/Backend/APIs.md)**: Endpoints planificados
- **[Requerimientos](docs/Requerimientos/)**: Especificaciones funcionales

## 🤝 Contribución
1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📝 Licencia
Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

## 👥 Equipo
- **Desarrollador Principal**: [Tu Nombre]
- **Diseñador UX/UI**: [Nombre]
- **QA Tester**: [Nombre]

## 📞 Contacto
- **Email**: tu@email.com
- **GitHub**: [https://github.com/RuedaUABC/CimaCritics](https://github.com/RuedaUABC/CimaCritics)
- **Discord**: [Servidor del proyecto]

---
⭐ Si te gusta este proyecto, ¡dale una estrella en GitHub!