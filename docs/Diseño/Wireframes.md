# 🎨 Wireframes - CimaCritics

Los wireframes se han convertido a archivos HTML interactivos con un sistema de diseño uniforme blanco/negro. Puedes abrir los siguientes archivos en un navegador:

## 📱 Flujo de Usuario

### Acceso
- [Login](Wireframes/login.html) - Inicio de sesión
- [Registro](Wireframes/registro.html) - Crear nueva cuenta

### Navegación Principal
- [Página de Inicio](Wireframes/pagina-inicio.html) - Bienvenida y cómics destacados
- [Búsqueda](Wireframes/busqueda.html) - Listado de resultados con filtros
- [Detalles de Cómic](Wireframes/detalles-comic.html) - Info completa y reseñas
- [Perfil de Usuario](Wireframes/perfil-usuario.html) - Mi perfil y mis reseñas

### Reseñas
- [Formulario de Reseña](Wireframes/formulario-resena.html) - Crear/editar reseña

## 🔐 Panel de Administración

- [Admin Dashboard](Wireframes/admin-dashboard.html) - Vista general, estadísticas
- [Admin Entry (Cómic)](Wireframes/admin-entry.html) - Agregar/editar cómic con escritores, dibujantes y editoriales

---

## 🎨 Sistema de Diseño

### Paleta de Colores
- **Fondo Principal**: `#2b2b2b` (Gris oscuro)
- **Tarjetas/Contenedor**: `#ffffff` (Blanco)
- **Bordes**: `#999999` (Gris medio)
- **Texto Primario**: `#111111` (Negro)
- **Texto Secundario**: `#444444` (Gris oscuro claro)

### Tipografía
- **Font family**: Arial, sans-serif
- **Headlines**: Font-weight 700
- **Body**: Font-weight 400, color texto primario

### Componentes

#### Placeholders de Portada
- **Aspect Ratio**: 8.5/11 (tamaño carta estándar)
- **Borde**: 2px dashed #999
- **Fondo**: #ffffff
- Centered placeholder text: "Portada (tamaño carta)"

#### Botones
- **Estilo**: Blanco con borde gris `#999`, sin color de fondo
- **Padding**: 6-10px
- **Border-radius**: 4-6px
- **Focus**: Outline visible para accesibilidad

#### Campos de Entrada
- **Borde**: 1px solid #999
- **Padding**: 10px
- **Border-radius**: 4-6px
- **Fondo**: Blanco
- **Color**: Negro

#### Tarjetas Cómic
- **Grid Layout**: auto-fill, minmax(200px, 1fr)
- **Borde**: 1px solid #999
- **Padding**: 12px
- **Display**: Flex column
- Contenido: Portada, título, autor, rating, reseñas-count

### Accesibilidad
- Atributos `aria-label` en puntos de entrada
- `aria-hidden` en elementos decorativos
- Focus styles visibles (3px outline #9fd3ff)
- Roles semánticos HTML5

### Responsividad
- **Mobile-first**: Min-width 140px para inputs
- **Grid automático**: Ajusta columnas según pantalla
- **Flex-wrap**: En headers y controles
- Media queries para pantallas ≤600px

### Formularios Admin

#### Multi-entry Fields
Campos que permiten múltiples entradas:
- **Escritor(es)**: Campo de entrada + botón "+" para agregar más
- **Dibujante(s)**: Campo de entrada + botón "+" para agregar más
- **Editorial(es)**: Campo de entrada + botón "+" para agregar más

Estructura HTML:
```html
<label>Escritor(es)</label>
<div class="multi-input">
    <input type="text" name="writers[]" placeholder="...">
    <button type="button" class="add-btn">+</button>
</div>
```

---

## 📐 Notas de Implementación

1. **HTML Prototipos**: Los wireframes son HTML5 interactivos para testing rápido
2. **CSS Embebido**: Estilos inline y `<style>` para portabilidad
3. **Sin JavaScript**: Wireframes estáticos; lógica será en producción
4. **Accesibilidad WCAG**: Cumplimiento básico de accessibilidad

---

## 🔄 Guía de Actualización

Al modificar wireframes:
1. Mantén la paleta B/N consistente
2. Usa aspect-ratio 8.5/11 para portadas
3. Aplica focus styles en interactivos
4. Test en mobile (≤600px ancho)
5. Verifica roles aria en nuevas secciones