# 📊 Diagrama Entidad-Relación - CimaCritics

# 📊 Diagrama Entidad-Relación - CimaCritics

## Modelo de Datos

```mermaid
erDiagram
    Usuario ||--o{ Review : "tiene"
    Comic ||--o{ Review : "tiene"
    
    Usuario {
        int id PK
        string nombre
        string email UK
        string contraseña_hash
        datetime fecha_registro
        boolean es_admin
        boolean es_moderador
        string bio
        string avatar_url
        int seguidores_count
        int siguiendo_count
    }
    
    Comic {
        int id PK
        string titulo
        string autor
        int año
        string editorial
        string genero
        text descripcion
        string imagen_url
        datetime fecha_creacion
        float promedio_calificacion
    }
    
    Review {
        int id PK
        int usuario_id FK
        int comic_id FK
        int calificacion
        text texto
        datetime fecha_creacion
        int likes
        int dislikes
    }
    
    Seguimiento {
        int id PK
        int seguidor_id FK
        int seguido_id FK
        datetime fecha_seguimiento
    }
    
    Reporte {
        int id PK
        int usuario_id FK
        string contenido_tipo
        int contenido_id
        string motivo
        text descripcion
        datetime fecha_reporte
        string estado
    }
    
    Comentario {
        int id PK
        int review_id FK
        int usuario_id FK
        text texto
        datetime fecha_creacion
        int likes
        int dislikes
    }
    
    Usuario ||--o{ Seguimiento : "sigue"
    Usuario ||--o{ Reporte : "reporta"
    Usuario ||--o{ Comentario : "escribe"
```

## Relaciones

### Usuario - Review
- **Tipo**: 1:N (Un usuario puede tener muchas reseñas)
- **Cardinalidad**: 1..1 → 0..N
- **Restricción**: Usuario debe existir para crear reseña

### Comic - Review
- **Tipo**: 1:N (Un cómic puede tener muchas reseñas)
- **Cardinalidad**: 1..1 → 0..N
- **Restricción**: Cómic debe existir para crear reseña

### Usuario - Seguimiento
- **Tipo**: 1:N (Un usuario puede seguir a muchos, y ser seguido por muchos)
- **Cardinalidad**: 0..N → 0..N

### Usuario - Reporte
- **Tipo**: 1:N (Un usuario puede reportar muchos contenidos)

### Review - Comentario
- **Tipo**: 1:N (Una reseña puede tener muchos comentarios)

## Atributos Derivados
- **Comic.promedio_rating**: Calculado como promedio de Review.calificacion
- **Review.likes/dislikes**: Contadores de votos positivos/negativos
- **Usuario.seguidores_count/siguiendo_count**: Contadores calculados

## Reglas de Integridad
1. Email único por usuario
2. Calificación entre 1-5
3. Usuario no puede reseñar el mismo cómic dos veces
4. Solo administradores pueden modificar ciertos campos

## Índices Recomendados
- Usuario.email (único)
- Comic.titulo, Comic.autor (búsqueda)
- Review.usuario_id, Review.comic_id (joins)
- Comic.genero, Comic.editorial (filtros)

## Relaciones

### Usuario - Review
- **Tipo**: 1:N (Un usuario puede tener muchas reseñas)
- **Cardinalidad**: 1..1 → 0..N
- **Restricción**: Usuario debe existir para crear reseña

### Comic - Review
- **Tipo**: 1:N (Un cómic puede tener muchas reseñas)
- **Cardinalidad**: 1..1 → 0..N
- **Restricción**: Cómic debe existir para crear reseña

## Atributos Derivados
- **Comic.promedio_rating**: Calculado como promedio de Review.calificacion
- **Review.likes/dislikes**: Contadores de votos positivos/negativos

## Reglas de Integridad
1. Email único por usuario
2. Calificación entre 1-5
3. Usuario no puede reseñar el mismo cómic dos veces
4. Solo administradores pueden modificar ciertos campos

## Índices Recomendados
- Usuario.email (único)
- Comic.titulo, Comic.autor (búsqueda)
- Review.usuario_id, Review.comic_id (joins)
- Comic.genero, Comic.editorial (filtros)