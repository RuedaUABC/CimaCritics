# 🎨 Estilos CSS - Frontend (Phantom Theme)

## 1. Template Base: HTML5 UP Phantom
Los estilos están basados en el template **Phantom** de HTML5 UP, adaptado para CimaCritics. Phantom utiliza:

- **Diseño oscuro** con gradientes sutiles
- **Tipografía moderna** (Source Sans Pro + Raleway)
- **Efectos de parallax** en secciones
- **Animaciones suaves** y transiciones
- **Layout responsive** con breakpoints

## 2. Variables y Configuración Base
```css
/* Variables CSS */
:root {
  --font-family: 'Source Sans Pro', Helvetica, sans-serif;
  --font-family-alt: 'Raleway', Helvetica, sans-serif;
  
  /* Colores principales */
  --bg-color: #1b1f22;
  --bg-alt: #2e3235;
  --bg-light: #36393e;
  --text-color: rgba(255, 255, 255, 0.9);
  --text-color-alt: rgba(255, 255, 255, 0.6);
  --accent-color: #5c5c5c;
  --accent-color-hover: #7c7c7c;
  --comic-primary: #4acaa8;
  --comic-secondary: #5dd6b2;
  --comic-accent: #ffd700;
  
  /* Espaciado */
  --spacing-xs: 1rem;
  --spacing-sm: 2rem;
  --spacing-md: 3rem;
  --spacing-lg: 4rem;
  --spacing-xl: 6rem;
  
  /* Bordes y sombras */
  --border-radius: 4px;
  --box-shadow: 0 0 0 1px rgba(255, 255, 255, 0.1);
  --box-shadow-hover: 0 0 0 1px rgba(255, 255, 255, 0.2);
}

/* Reset y base */
* { box-sizing: border-box; }

body {
  background: var(--bg-color);
  color: var(--text-color);
  font-family: var(--font-family);
  font-size: 16pt;
  font-weight: 300;
  line-height: 1.75;
  margin: 0;
  overflow-x: hidden;
}

body.is-loading * {
  animation: none !important;
  transition: none !important;
}
```

## 3. Header y Navegación
```css
#header {
  background: var(--bg-color);
  color: var(--text-color);
  cursor: default;
  height: 3.25rem;
  left: 0;
  line-height: 3.25rem;
  position: fixed;
  top: 0;
  width: 100%;
  z-index: 10001;
}

#navPanelToggle {
  color: var(--text-color);
  cursor: pointer;
  display: none;
  height: 3.25rem;
  left: 0;
  position: fixed;
  text-decoration: none;
  top: 0;
  width: 4rem;
  z-index: 10002;
}

#menu {
  background: var(--bg-color);
  color: var(--text-color);
  display: none;
  left: 0;
  height: 100%;
  max-width: 80%;
  overflow-y: auto;
  padding: 3rem 2rem;
  position: fixed;
  top: 0;
  width: 20rem;
  z-index: 10002;
}

#menu .links li a:hover { color: var(--accent-color); }
```

## 4. Sección Banner (Hero)
```css
#banner {
  background-attachment: fixed;
  background-image: linear-gradient(rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.5)), url('../images/banner.jpg');
  background-position: center;
  background-repeat: no-repeat;
  background-size: cover;
  padding: 12rem 0 8rem 0;
  text-align: center;
}

#banner h1 {
  color: #ffffff;
  font-family: var(--font-family-alt);
  font-size: 3.5rem;
  font-weight: 900;
  letter-spacing: -0.025rem;
  line-height: 1;
  margin: 0 0 1rem 0;
}

#banner .button {
  background: rgba(255, 255, 255, 0.1);
  border: solid 2px rgba(255, 255, 255, 0.25);
  color: #ffffff;
  font-weight: 300;
  letter-spacing: 0.025rem;
  text-decoration: none;
  transition: all 0.2s ease-in-out;
}

#banner .button:hover {
  background: rgba(255, 255, 255, 0.15);
  border-color: rgba(255, 255, 255, 0.5);
}
```

## 5. Secciones Generales
```css
.wrapper {
  margin: 0 auto;
  max-width: 75rem;
  padding: var(--spacing-xl) var(--spacing-md);
  width: calc(100% - 3rem);
}

.wrapper.style1 { background: var(--bg-color); }
.wrapper.style2 { background: var(--bg-alt); }
.wrapper.style3 { background: var(--bg-light); }

.major h2 {
  color: var(--text-color);
  font-family: var(--font-family-alt);
  font-size: 2.5rem;
  font-weight: 900;
  letter-spacing: -0.025rem;
  line-height: 1;
  margin: 0 0 1rem 0;
}

.button {
  background: var(--accent-color);
  border: 0;
  border-radius: var(--border-radius);
  color: #ffffff;
  cursor: pointer;
  display: inline-block;
  font-family: var(--font-family);
  font-size: 0.8rem;
  font-weight: 300;
  height: 3rem;
  letter-spacing: 0.025rem;
  line-height: 2.8rem;
  padding: 0 2rem;
  text-align: center;
  text-decoration: none;
  text-transform: uppercase;
  transition: all 0.2s ease-in-out;
  white-space: nowrap;
}

.button:hover { background: var(--accent-color-hover); }
.button.special { background: var(--comic-primary); }
.button.special:hover { background: var(--comic-secondary); }
```

## 6. Grid y Tarjetas de Cómics
```css
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: var(--spacing-md);
  margin: var(--spacing-lg) 0;
}

.comic-card {
  background: var(--bg-light);
  border-radius: var(--border-radius);
  box-shadow: var(--box-shadow);
  overflow: hidden;
  transition: all 0.2s ease-in-out;
}

.comic-card:hover {
  box-shadow: var(--box-shadow-hover);
  transform: translateY(-2px);
}

.comic-card .image img {
  display: block;
  transition: transform 0.2s ease-in-out;
  width: 100%;
}

.comic-card:hover .image img { transform: scale(1.05); }

.comic-card h3 {
  color: var(--text-color);
  font-family: var(--font-family-alt);
  font-size: 1.25rem;
  font-weight: 600;
  margin: 0 0 0.5rem 0;
}

.comic-card .rating .stars { color: var(--comic-accent); }
```

## 7. Estadísticas
```css
.statistics {
  display: flex;
  justify-content: center;
  gap: var(--spacing-xl);
}

.statistic .value {
  color: var(--comic-primary);
  font-family: var(--font-family-alt);
  font-size: 3rem;
  font-weight: 900;
  line-height: 1;
  margin: 0 0 0.5rem 0;
}
```

## 8. Responsive Design
```css
@media screen and (max-width: 980px) {
  #banner { padding: 8rem 0 4rem 0; }
  #banner h1 { font-size: 2.5rem; }
  .grid { grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); }
  .statistics { flex-direction: column; gap: var(--spacing-md); }
}

@media screen and (max-width: 736px) {
  #navPanelToggle { display: block; }
  #banner { padding: 6rem 0 2rem 0; }
  #banner h1 { font-size: 2rem; }
  .wrapper { padding: var(--spacing-lg) var(--spacing-sm); }
  .grid { grid-template-columns: 1fr; }
}
```

## 9. Tema Personalizado para CimaCritics
```css
/* Estilos específicos para reseñas */
.review {
  background: var(--bg-light);
  border-radius: var(--border-radius);
  margin-bottom: var(--spacing-md);
  padding: var(--spacing-md);
}

.review-header {
  align-items: center;
  display: flex;
  justify-content: space-between;
  margin-bottom: var(--spacing-sm);
}

.username { color: var(--comic-primary); font-weight: 600; }

.like-btn, .dislike-btn {
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: var(--border-radius);
  color: var(--text-color);
  cursor: pointer;
  padding: 0.25rem 0.5rem;
  transition: all 0.2s ease-in-out;
}

.like-btn:hover { background: rgba(76, 175, 80, 0.2); }
.dislike-btn:hover { background: rgba(244, 67, 54, 0.2); }
```