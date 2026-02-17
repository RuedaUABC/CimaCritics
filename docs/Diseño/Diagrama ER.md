# 📊 Diagrama Entidad-Relación - CimaCritics

## Modelo de Datos

```
┌─────────────────┐       ┌─────────────────┐
│    Usuario      │       │     Comic       │
├─────────────────┤       ├─────────────────┤
│ id (PK)         │       │ id (PK)         │
│ nombre          │       │ titulo          │
│ email           │       │ autor           │
│ contraseña_hash │       │ año             │
│ fecha_registro  │       │ editorial       │
│ es_admin        │       │ genero          │
└─────────────────┘       │ descripcion     │
          │               │ imagen_url      │
          │               │ fecha_creacion  │
          │               │ promedio_rating │
          ▼               └─────────────────┘
┌─────────────────┐               │
│    Review       │               │
├─────────────────┤               │
│ id (PK)         │◄──────────────┘
│ usuario_id (FK) │
│ comic_id (FK)   │
│ calificacion    │
│ texto           │
│ fecha_creacion  │
│ likes           │
│ dislikes        │
└─────────────────┘
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