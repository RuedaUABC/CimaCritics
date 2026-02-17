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