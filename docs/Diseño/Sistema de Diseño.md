# 🎨 Sistema de Diseño - CimaCritics

## Visión General
El sistema de diseño de CimaCritics utiliza una **paleta monocromática (Blanco/Negro)** con wireframes HTML/CSS interactivos. El objetivo es proporcionar una interfaz clara, accesible y minimalista.

---

## 1. Paleta de Colores

| Uso | Color | Hex | RGB |
|-----|-------|-----|-----|
| Fondo principal | Gris Oscuro | #2b2b2b | rgb(43, 43, 43) |
| Fondo tarjetas | Blanco | #ffffff | rgb(255, 255, 255) |
| Bordes | Gris Medio | #999999 | rgb(153, 153, 153) |
| Texto primario | Negro | #111111 | rgb(17, 17, 17) |
| Texto secundario | Gris Claro | #444444 | rgb(68, 68, 68) |
| Focus states | Azul claro | #9fd3ff | rgb(159, 211, 255) |

### Uso Recomendado
- **#2b2b2b**: Container principal, backgrounds
- **#ffffff**: Tarjetas, modales, campos de entrada
- **#999999**: Bordes, separadores, disabled states
- **#111111**: Títulos, textos principales
- **#444444**: Descripciones, textos secundarios
- **#9fd3ff**: Focus outline (accesibilidad)

---

## 2. Tipografía

### Font Stack
```css
font-family: Arial, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
```

### Escala de Tamaños
- **h1**: 32px, font-weight: 700
- **h2**: 24px, font-weight: 700
- **h3**: 20px, font-weight: 600
- **h4**: 16px, font-weight: 700
- **body**: 14-16px, font-weight: 400
- **small**: 12px, font-weight: 400

### Líneas
- **Line-height**: 1.5 (cuerpo), 1.2 (títulos)
- **Letter-spacing**: normal o ligeramente aumentado en títulos

---

## 3. Espaciado

### Escala de Espacios
```
8px   - Muy pequeño (gaps en multi-inputs)
12px  - Pequeño (padding en elementos)
16px  - Medio (padding estándar)
20px  - Grande (gap entre secciones)
24px  - Extra grande (top/bottom principales)
```

### Aplicación
- **Padding botones**: 6-10px
- **Padding inputs**: 10px
- **Padding tarjetas**: 12px
- **Gap grid**: 16px
- **Margin secciones**: 24px arriba/abajo

---

## 4. Componentes

### 4.1 Botones
```css
background: #ffffff;
color: #111111;
border: 1px solid #999999;
padding: 10px 16px;
border-radius: 4px;
cursor: pointer;
font-weight: 500;
```

**Estados:**
- **Default**: Blanco fondo, borde gris
- **Hover**: Fondo gris muy claro
- **Disabled**: Color text #999999, cursor not-allowed
- **Focus**: Outline 3px #9fd3ff

### 4.2 Campos de Entrada
```css
background: #ffffff;
color: #111111;
border: 1px solid #999999;
padding: 10px;
border-radius: 4px;
font-family: inherit;
```

**Variantes:**
- Input tipo text
- Input type number
- Select/dropdown
- Textarea

**Focus**: Outline 3px #9fd3ff

### 4.3 Tarjetas Cómić
```css
background: #ffffff;
border: 1px solid #999999;
border-radius: 8px;
padding: 12px;
display: flex;
flex-direction: column;
gap: 8px;
```

**Contenido interno:**
- Placeholder portada (aspect 8.5/11)
- Título (h4)
- Autor/info (small)
- Rating (con estrellas)
- Contador de reseñas

### 4.4 Placeholders de Portada
```css
width: 100%;
background: #ffffff;
border: 2px dashed #999999;
border-radius: 6px;
aspect-ratio: 8.5 / 11;
display: flex;
align-items: center;
justify-content: center;
```

**Texto interior**: "Portada (tamaño carta)" en color #999999

---

## 5. Layouts

### 5.1 Grid Responsivo
```css
display: grid;
grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
gap: 16px;
```
Usado en: listados de cómics, resultados de búsqueda

### 5.2 Flexbox Horizontal
```css
display: flex;
flex-wrap: wrap;
gap: 12px;
align-items: center;
```
Usado en: headers, controles, filtros

### 5.3 Multi-input Fields
Estructura para campos con múltiples entradas:
```html
<div class="multi-input">
    <input type="text" name="items[]" placeholder="...">
    <button type="button" class="add-btn">+</button>
</div>
```

CSS:
```css
.multi-input {
    display: flex;
    gap: 4px;
    align-items: center;
    margin-bottom: 16px;
}
.multi-input input {
    flex: 1;
}
.add-btn {
    width: 32px;
    height: 32px;
    line-height: 20px;
}
```

---

## 6. Accesibilidad

### 6.1 ARIA Labels
```html
<!-- Ejemplo: Input de búsqueda -->
<input type="search" id="q" aria-label="Buscar cómics">

<!-- Ejemplo: Rating con estrellas -->
<div class="rating" aria-label="Puntuación 4.1 de 5">
    <span aria-hidden="true">★★★★☆</span>
    <span>4.1</span>
</div>
```

### 6.2 Focus States
Todos los elementos interactivos deben tener outline:
```css
a:focus, button:focus, input:focus, select:focus {
    outline: 3px solid #9fd3ff;
    outline-offset: 2px;
}
```

### 6.3 Roles HTML5
- `<nav>` para navegación
- `<main>` para contenido principal
- `<article>` para tarjetas de cómics
- `<section>` para secciones temáticas
- `role="search"` en forms de búsqueda
- `role="navigation"` en paginación

### 6.4 Texto Alternativo
- `alt` en todas las imágenes
- `aria-label` en botones sin texto
- `aria-hidden="true"` en decoraciones

---

## 7. Responsive & Mobile

### Breakpoints
- **Large**: 900px+ (escritorio)
- **Medium**: 600-900px (tablet)
- **Small**: <600px (móvil)

### Mobile-first Rules
```css
/* Base (móvil) */
.container { max-width: 100%; padding: 0 8px; }
.search input { min-width: 140px; }

/* @media (min-width: 600px) */
@media (min-width: 600px) {
    .container { max-width: 800px; }
    .filters { gap: 10px; }
}

/* @media (min-width: 900px) */
@media (min-width: 900px) {
    .container { max-width: 1200px; margin: 24px auto; }
}
```

---

## 8. Guía de Implementación

### Para Diseñadores
1. Mantén la paleta B/N consistente
2. Usa Grid responsive para listados
3. Aplica aspect-ratio 8.5/11 a portadas
4. Todos los botones = borde gris, sin color
5. Focus state = outline azul claro

### Para Desarrolladores
1. Importa estilos base desde wireframes existentes
2. Reutiliza clases `.multi-input`, `.comic-card`, etc.
3. Test en mobile (<600px)
4. Verifica ARIA labels en nuevos componentes
5. Asegura focus styles en todos los interactivos

### Checklist QA
- [ ] Paleta B/N consistente
- [ ] Responsive en móvil/tablet/desktop
- [ ] Focus visible en todos los inputs
- [ ] ARIA labels presentes
- [ ] Alt text en imágenes
- [ ] Bordes/padding consistentes
- [ ] Grid/flex sin overflow

---

## 9. Referencias

- **Wireframes**: `docs/Diseño/Wireframes/`
- **Especificación Técnica**: `docs/Requerimientos/Especificación Técnica.md`
- **Arquitectura**: `docs/Diseño/Arquitectura.md`
