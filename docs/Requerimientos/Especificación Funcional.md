# 📋 Especificación Funcional - CimaCritics

## 1. Introducción
Esta especificación define las funcionalidades principales que debe tener la plataforma CimaCritics.

## 2. Usuarios del Sistema
- **Usuario Anónimo**: Puede ver cómics y reseñas
- **Usuario Registrado**: Puede crear reseñas, calificar cómics, seguir otros usuarios
- **Administrador**: Gestiona contenido, usuarios y moderación

## 3. Funcionalidades Principales

### 3.1 Gestión de Cómics
- **Visualizar catálogo**: Lista paginada de cómics con filtros
- **Ver detalles**: Información completa del cómic, reseñas promedio
- **Buscar**: Búsqueda por título, autor, editorial, género

### 3.2 Sistema de Reseñas
- **Crear reseña**: Formulario con calificación (1-5 estrellas) y texto
- **Editar reseña**: Modificar reseña propia
- **Eliminar reseña**: Borrar reseña propia (administrador puede borrar cualquier)
- **Votar reseñas**: Sistema de likes/dislikes

### 3.3 Gestión de Usuarios
- **Registro**: Crear cuenta con email, nombre, contraseña
- **Login/Logout**: Autenticación segura
- **Perfil**: Ver reseñas propias, estadísticas
- **Seguir usuarios**: Sistema de seguimiento

### 3.4 Funcionalidades Adicionales
### 3.4 Funcionalidades Adicionales
- **Sistema de Recomendaciones**:
  - **Recomendaciones Personalizadas**: Basadas en el historial de reseñas del usuario, utilizando algoritmos de filtrado colaborativo (usuario-usuario o ítem-ítem) para sugerir cómics similares a los que ha calificado positivamente.
  - **Recomendaciones por Contenido**: Análisis de metadatos de cómics (género, autor, editorial) para sugerir obras relacionadas.
  - **Recomendaciones Populares**: Mostrar cómics con alta calificación promedio o más reseñas recientes.
  - **Recomendaciones por Seguidores**: Sugerir cómics basados en las reseñas de usuarios que el usuario sigue.
  - **Interfaz de Recomendaciones**: Página dedicada con lista de sugerencias, explicaciones breves (e.g., "Porque te gustó X"), opción de feedback (me gusta/no me gusta) para mejorar el algoritmo.
  - **Actualización en Tiempo Real**: Recomendaciones se actualizan periódicamente o tras nuevas reseñas.
- **Estadísticas**: Gráficos de reseñas por género, autor, editorial; estadísticas de usuario (reseñas escritas, promedio de calificaciones)
- **Comentarios**: Sistema de comentarios en reseñas con likes/dislikes
- **Notificaciones**: Alertas por email o en-app para nuevas reseñas de usuarios seguidos, respuestas a comentarios
- **Moderación**: Herramientas para administradores y moderadores para gestionar contenido reportado
- **Búsqueda Avanzada**: Filtros por calificación promedio, fecha de publicación, popularidad
- **Perfil de Usuario**: Página personal con reseñas, estadísticas, lista de seguidores/seguidores
- **API Pública**: Endpoints para integración con otras plataformas (opcional)
- **Estadísticas**: Gráficos de reseñas por género, autor, editorial; estadísticas de usuario (reseñas escritas, promedio de calificaciones)
- **Comentarios**: Sistema de comentarios en reseñas con likes/dislikes
- **Notificaciones**: Alertas por email o en-app para nuevas reseñas de usuarios seguidos, respuestas a comentarios
- **Moderación**: Herramientas para administradores y moderadores para gestionar contenido reportado
- **Búsqueda Avanzada**: Filtros por calificación promedio, fecha de publicación, popularidad
- **Perfil de Usuario**: Página personal con reseñas, estadísticas, lista de seguidores/seguidores
- **API Pública**: Endpoints para integración con otras plataformas (opcional)

## 5. Flujos de Usuario y Wireframes

### 5.1 Flujo de Acceso
1. Usuario anónimo llega a **Login** (login.html)
   - Ingresa email/usuario y contraseña
   - O puede crear cuenta en **Registro** (registro.html)
2. Nueva cuenta:
   - Usuario ingresa usuario, email, contraseña
   - Redirecciona a **Inicio** (pagina-inicio.html)

### 5.2 Flujo Principal (Usuario Autenticado)
1. **Inicio** (pagina-inicio.html) - Bienvenida con cómics destacados
2. **Búsqueda** (busqueda.html) - Buscar, filtrar, ver catálogo
3. **Detalles** (detalles-comic.html) - Ver info del cómic + reseñas
4. **Crear Reseña** (formulario-resena.html) - Calificar y escribir opinión
5. **Perfil** (perfil-usuario.html) - Ver mis reseñas y datos

### 5.3 Flujo Administrador
1. **Admin Dashboard** (admin-dashboard.html) - Vista general, estadísticas
2. **Admin Entry** (admin-entry.html) - Agregar/editar cómic con:
   - Múltiples escritores
   - Múltiples dibujantes
   - Múltiples editoriales
   - Descripción, año, género, portada

### 5.4 Diseño Visual
Todos los wireframes implementan un **sistema de diseño Blanco/Negro**:
- Fondo gris oscuro (#2b2b2b)
- Tarjetas en blanco (#ffffff)
- Bordes en gris (#999999)
- Accesibilidad WCAG (ARIA labels, focus visible)
- Responsive mobile-first

Documentación: `docs/Diseño/Sistema de Diseño.md`

## 4. Requisitos No Funcionales
- **Rendimiento**: Carga rápida (< 2s para páginas principales), soporte para al menos 1000 usuarios concurrentes
- **Seguridad**: Autenticación robusta, protección contra ataques comunes (SQL injection, XSS), encriptación de datos sensibles
- **Accesibilidad**: Cumplir estándares WCAG 2.1 AA
- **Escalabilidad**: Arquitectura que permita crecimiento horizontal (más servidores)
- **Disponibilidad**: 99% uptime, respaldo de datos diario
- **Mantenibilidad**: Código modular, documentación completa, tests automatizados con >80% cobertura
- **Compatibilidad**: Soporte para navegadores modernos (Chrome, Firefox, Safari, Edge)