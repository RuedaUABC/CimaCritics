# 🎨 Estilos CSS - Frontend

## 1. Template Base: HTML5 UP Phantom
Los estilos están basados en el template **Phantom** de HTML5 UP, adaptado para CimaCritics. Phantom utiliza:

- **Diseño oscuro** con gradientes sutiles
- **Tipografía moderna** (Sans-serif)
- **Efectos de parallax** en secciones
- **Animaciones suaves** y transiciones
- **Layout responsive** con breakpoints

## 2. Variables y Colores
```css
:root {
  /* Colores principales */
  --primary-color: #2563eb;
  --secondary-color: #64748b;
  --accent-color: #f59e0b;
  
  /* Colores de fondo */
  --bg-primary: #ffffff;
  --bg-secondary: #f8fafc;
  --bg-dark: #1e293b;
  
  /* Colores de texto */
  --text-primary: #1e293b;
  --text-secondary: #64748b;
  --text-light: #94a3b8;
  
  /* Espaciado */
  --spacing-xs: 0.25rem;
  --spacing-sm: 0.5rem;
  --spacing-md: 1rem;
  --spacing-lg: 1.5rem;
  --spacing-xl: 2rem;
  
  /* Bordes y sombras */
  --border-radius: 8px;
  --shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05);
  --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1);
  --shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1);
}
```

## 3. Reset y Base
```css
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
  line-height: 1.6;
  color: var(--text-primary);
  background-color: var(--bg-primary);
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 var(--spacing-md);
}
```

## 4. Header y Navegación
```css
.header {
  background-color: var(--bg-primary);
  border-bottom: 1px solid #e2e8f0;
  padding: var(--spacing-md) 0;
  position: sticky;
  top: 0;
  z-index: 100;
}

.header .container {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo h1 {
  font-size: 1.5rem;
  font-weight: 700;
}

.logo a {
  text-decoration: none;
  color: var(--primary-color);
}

.nav ul {
  display: flex;
  list-style: none;
  gap: var(--spacing-lg);
}

.nav a {
  text-decoration: none;
  color: var(--text-primary);
  font-weight: 500;
  transition: color 0.2s;
}

.nav a:hover {
  color: var(--primary-color);
}

.auth-buttons {
  display: flex;
  gap: var(--spacing-sm);
}

.btn {
  padding: var(--spacing-sm) var(--spacing-md);
  border: none;
  border-radius: var(--border-radius);
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.btn.primary {
  background-color: var(--primary-color);
  color: white;
}

.btn.primary:hover {
  background-color: #1d4ed8;
}

.btn.secondary {
  background-color: transparent;
  color: var(--text-primary);
  border: 1px solid #e2e8f0;
}

.btn.secondary:hover {
  background-color: var(--bg-secondary);
}
```

## 5. Grid de Cómics
```css
.comics-grid {
  padding: var(--spacing-xl) 0;
}

.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: var(--spacing-lg);
  margin-bottom: var(--spacing-xl);
}

.comic-card {
  background-color: var(--bg-primary);
  border-radius: var(--border-radius);
  box-shadow: var(--shadow-sm);
  overflow: hidden;
  transition: transform 0.2s, box-shadow 0.2s;
}

.comic-card:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
}

.comic-image img {
  width: 100%;
  height: 200px;
  object-fit: cover;
}

.comic-info {
  padding: var(--spacing-md);
}

.comic-info h3 {
  font-size: 1.1rem;
  margin-bottom: var(--spacing-sm);
  color: var(--text-primary);
}

.comic-info p {
  color: var(--text-secondary);
  font-size: 0.9rem;
  margin-bottom: var(--spacing-xs);
}

.rating {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  margin: var(--spacing-sm) 0;
}

.stars {
  color: var(--accent-color);
  font-size: 1.1rem;
}

.rating-value {
  color: var(--text-secondary);
  font-size: 0.9rem;
}
```

## 6. Formularios
```css
.form-group {
  margin-bottom: var(--spacing-md);
}

.form-group label {
  display: block;
  margin-bottom: var(--spacing-sm);
  font-weight: 500;
  color: var(--text-primary);
}

.form-group input,
.form-group textarea,
.form-group select {
  width: 100%;
  padding: var(--spacing-sm) var(--spacing-md);
  border: 1px solid #e2e8f0;
  border-radius: var(--border-radius);
  font-size: 1rem;
  transition: border-color 0.2s;
}

.form-group input:focus,
.form-group textarea:focus,
.form-group select:focus {
  outline: none;
  border-color: var(--primary-color);
  box-shadow: 0 0 0 3px rgb(37 99 235 / 0.1);
}

.form-group textarea {
  resize: vertical;
  min-height: 100px;
}
```

## 7. Sistema de Calificación con Estrellas
```css
.stars-input {
  display: flex;
  gap: var(--spacing-xs);
}

.stars-input input[type="radio"] {
  display: none;
}

.stars-input label {
  font-size: 2rem;
  color: #e2e8f0;
  cursor: pointer;
  transition: color 0.2s;
}

.stars-input input[type="radio"]:checked ~ label,
.stars-input label:hover,
.stars-input label:hover ~ label {
  color: var(--accent-color);
}
```

## 8. Responsive Design
```css
@media (max-width: 768px) {
  .header .container {
    flex-direction: column;
    gap: var(--spacing-md);
  }
  
  .nav ul {
    flex-wrap: wrap;
    justify-content: center;
  }
  
  .grid {
    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
    gap: var(--spacing-md);
  }
  
  .comic-info {
    padding: var(--spacing-sm);
  }
}

@media (max-width: 480px) {
  .container {
    padding: 0 var(--spacing-sm);
  }
  
  .grid {
    grid-template-columns: 1fr;
  }
  
  .auth-buttons {
    flex-direction: column;
    width: 100%;
  }
  
  .btn {
    width: 100%;
  }
}
```

## 9. Animaciones y Transiciones
```css
.fade-in {
  animation: fadeIn 0.3s ease-in;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.loading {
  display: inline-block;
  width: 20px;
  height: 20px;
  border: 3px solid #f3f3f3;
  border-top: 3px solid var(--primary-color);
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
```

## 10. Tema Oscuro (Futuro)
```css
/* Variables para tema oscuro */
[data-theme="dark"] {
  --bg-primary: #1e293b;
  --bg-secondary: #334155;
  --text-primary: #f1f5f9;
  --text-secondary: #cbd5e1;
}
```