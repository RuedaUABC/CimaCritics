# 📝 Casos de Uso - CimaCritics

## 1. Caso de Uso: Registrar Usuario
**Actor**: Usuario potencial
**Descripción**: El usuario crea una cuenta nueva en la plataforma
**Precondiciones**: Usuario no registrado
**Postcondiciones**: Usuario registrado y logueado
**Flujo Principal**:
1. Usuario accede a página de registro
2. Ingresa nombre, email, contraseña
3. Sistema valida datos
4. Sistema crea cuenta y envía email de confirmación
5. Usuario queda logueado

## 2. Caso de Uso: Crear Reseña
**Actor**: Usuario registrado
**Descripción**: Usuario crea una reseña para un cómic
**Precondiciones**: Usuario logueado, cómic existe
**Postcondiciones**: Reseña creada y visible
**Flujo Principal**:
1. Usuario selecciona cómic
2. Hace clic en "Crear reseña"
3. Ingresa calificación (1-5 estrellas)
4. Escribe texto de reseña
5. Publica reseña
6. Sistema actualiza promedio del cómic

## 3. Caso de Uso: Buscar Cómics
**Actor**: Cualquier usuario
**Descripción**: Usuario busca cómics por criterios
**Precondiciones**: Ninguna
**Postcondiciones**: Lista de cómics filtrados
**Flujo Principal**:
1. Usuario ingresa término de búsqueda
2. Selecciona filtros (género, editorial, año)
3. Sistema busca en base de datos
4. Muestra resultados paginados

## 4. Caso de Uso: Ver Detalles de Cómic
**Actor**: Cualquier usuario
**Descripción**: Usuario ve información completa de un cómic
**Precondiciones**: Cómic existe
**Postcondiciones**: Información mostrada
**Flujo Principal**:
1. Usuario selecciona cómic de lista
2. Sistema muestra: título, autor, descripción, imagen
3. Muestra reseñas con paginación
4. Muestra calificación promedio

## 5. Caso de Uso: Administrar Contenido
**Actor**: Administrador
**Descripción**: Admin gestiona cómics y reseñas
**Precondiciones**: Usuario es administrador
**Postcondiciones**: Contenido modificado
**Flujo Principal**:
1. Admin accede a panel de administración
2. Selecciona acción (crear/editar/eliminar cómic)
3. Modifica datos
4. Guarda cambios

**Flujos Alternativos**:
- Si el cómic no existe, mostrar error
- Si hay reseñas asociadas, confirmar eliminación

**Excepciones**:
- Usuario no autorizado: Redirigir a login

## 6. Caso de Uso: Seguir Usuario
**Actor**: Usuario registrado
**Descripción**: Usuario sigue a otro usuario para ver sus reseñas
**Precondiciones**: Usuario logueado, usuario objetivo existe
**Postcondiciones**: Relación de seguimiento creada
**Flujo Principal**:
1. Usuario visita perfil de otro usuario
2. Hace clic en "Seguir"
3. Sistema actualiza lista de seguidores
4. Muestra notificación

## 7. Caso de Uso: Reportar Contenido
**Actor**: Usuario registrado
**Descripción**: Usuario reporta reseña o cómic inapropiado
**Precondiciones**: Usuario logueado, contenido existe
**Postcondiciones**: Reporte enviado a moderadores
**Flujo Principal**:
1. Usuario selecciona contenido
2. Hace clic en "Reportar"
3. Selecciona motivo (spam, contenido ofensivo, etc.)
4. Envía reporte
5. Sistema notifica a administradores

## 8. Caso de Uso: Moderar Reportes
**Actor**: Moderador/Administrador
**Descripción**: Revisar y gestionar reportes de contenido
**Precondiciones**: Usuario es moderador
**Postcondiciones**: Contenido moderado o aprobado
**Flujo Principal**:
1. Moderador accede a panel de moderación
2. Revisa lista de reportes
3. Selecciona reporte
4. Decide acción (aprobar, eliminar contenido, banear usuario)
5. Aplica acción

## 9. Caso de Uso: Ver Recomendaciones
**Actor**: Usuario registrado
**Descripción**: Usuario ve recomendaciones personalizadas de cómics
**Precondiciones**: Usuario logueado, suficientes datos de reseñas
**Postcondiciones**: Lista de recomendaciones mostrada
**Flujo Principal**:
1. Usuario accede a sección de recomendaciones
2. Sistema analiza reseñas del usuario
3. Genera lista basada en similitudes
4. Muestra cómics recomendados con razones

## 10. Caso de Uso: Ver Estadísticas
**Actor**: Cualquier usuario
**Descripción**: Usuario ve estadísticas globales o personales
**Precondiciones**: Ninguna
**Postcondiciones**: Estadísticas mostradas
**Flujo Principal**:
1. Usuario selecciona sección de estadísticas
2. Elige tipo (global, personal, por género)
3. Sistema calcula y muestra gráficos/datos