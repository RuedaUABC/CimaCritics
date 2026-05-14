# Pendientes - CimaCritics

Este documento resume las implementaciones que siguen pendientes después de los avances recientes en testing, reseñas sociales, seguimiento, comentarios, moderación, biblioteca personal y edición de perfil.

## Alta prioridad

- [ ] **Guardar listas personalizadas**
  - Actualmente existe una biblioteca simple de cómics guardados.
  - Falta permitir listas separadas como "Leyendo", "Por leer", "Favoritos" o listas creadas por el usuario.

- [ ] **Seguridad de producción**
  - Reemplazar el `SECRET_KEY` por una variable obligatoria en producción.
  - Añadir rate limiting para login, registro y reportes.
  - Revisar expiración de sesión, cookies seguras y configuración por entorno.

- [ ] **Limpieza técnica SQLAlchemy**
  - Migrar usos de `Query.get()` a `db.session.get()`.
  - Cambiar `datetime.utcnow()` por fechas timezone-aware.
  - Reducir warnings actuales de la suite de pruebas.

- [ ] **Gestión avanzada de usuarios**
  - Panel admin para listar usuarios.
  - Cambiar roles: usuario, moderador, admin.
  - Desactivar o reactivar cuentas.

- [ ] **Acciones de moderación sobre contenido**
  - El panel ya permite resolver/rechazar reportes.
  - Falta permitir desde moderación eliminar directamente reseñas o comentarios reportados.
  - Falta registrar historial de acciones de moderador.

## Prioridad media

- [ ] **Notificaciones**
  - Notificar respuestas a comentarios.
  - Notificar nuevas reseñas de usuarios seguidos.
  - Mostrar alertas in-app y, opcionalmente, email.

- [ ] **Recomendaciones**
  - Recomendaciones por género, autor, editorial y calificaciones.
  - Recomendaciones basadas en usuarios seguidos.
  - Página dedicada de sugerencias.

- [ ] **Estadísticas avanzadas**
  - Gráficas por género, autor y editorial.
  - Actividad del usuario por periodo.
  - Cómics más guardados, más reseñados y mejor valorados.

- [ ] **API REST pública**
  - Endpoints JSON para cómics, reseñas, usuarios y autenticación.
  - Versionado `/api/v1`.
  - Documentación OpenAPI/Swagger si sigue siendo parte del alcance.

- [ ] **Búsqueda avanzada**
  - Filtro por calificación promedio.
  - Filtro por año/fecha de publicación.
  - Orden por popularidad, cantidad de reseñas o cantidad de guardados.

## Prioridad baja

- [ ] **Mejoras de perfil**
  - Cambiar contraseña.
  - Subida local de avatar en vez de solo URL.
  - Perfil público más completo: cómics favoritos, géneros preferidos, usuarios seguidos.

- [ ] **Likes/dislikes en comentarios**
  - El modelo `Comentario` tiene contadores.
  - Falta flujo de voto para comentarios similar al de reseñas.

- [ ] **Frontend y accesibilidad**
  - Revisar textos mojibake/encoding visibles en algunas plantillas y docs.
  - Probar responsive en vistas nuevas: moderación, edición de perfil y biblioteca.
  - Revisar navegación por teclado y estados focus.

- [ ] **Datos y despliegue**
  - Separar configuración local, testing y producción.
  - Documentar comandos de inicialización de base: `flask db upgrade` y `python utils/seed.py`.
  - Preparar checklist de despliegue con PostgreSQL.

## Mantenimiento

- [ ] **Actualizar documentación**
  - README con funcionalidades ya implementadas.
  - Docs de backend para reportes, biblioteca y edición de perfil.
  - Test plan con la suite actual de pytest.

- [ ] **Aumentar cobertura de tests**
  - Tests para edición/eliminación de cómics admin.
  - Tests para permisos de moderadores.
  - Tests para render de templates críticos.
  - Tests para migraciones básicas.
