# 🌐 Estructura HTML - Frontend

## 1. Template Base: HTML5 UP Phantom
El proyecto utiliza el template **Phantom** de HTML5 UP, adaptado para CimaCritics. Phantom es un template moderno con:

- **Diseño oscuro elegante**
- **Efectos de parallax sutiles**
- **Navegación minimalista**
- **Tipografía moderna**
- **Animaciones suaves**
- **Completamente responsive**

## 2. Estructura General
```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CimaCritics - Críticas de Cómics</title>
    <link rel="stylesheet" href="css/main.css">
    <link rel="stylesheet" href="css/custom.css">
</head>
<body>
    <!-- Header -->
    <header id="header">
        <div class="inner">
            <a href="#menu" class="navPanelToggle"><span class="fa fa-bars"></span></a>
        </div>
    </header>

    <!-- Menu -->
    <nav id="menu">
        <ul class="links">
            <li><a href="/">Inicio</a></li>
            <li><a href="/comics">Cómics</a></li>
            <li><a href="/search">Buscar</a></li>
            <li><a href="/login">Iniciar Sesión</a></li>
        </ul>
        <a href="#menu" class="close"></a>
    </nav>

    <!-- Main -->
    <div id="main">
        <!-- Secciones del sitio -->
    </div>

    <!-- Footer -->
    <footer id="footer">
        <div class="inner">
            <div class="copyright">
                &copy; CimaCritics. Design: <a href="https://html5up.net">HTML5 UP</a>.
            </div>
        </div>
    </footer>

    <!-- Scripts -->
    <script src="js/jquery.min.js"></script>
    <script src="js/skel.min.js"></script>
    <script src="js/util.js"></script>
    <script src="js/main.js"></script>
    <script src="js/custom.js"></script>
</body>
</html>
```

## 3. Secciones Principales

### 3.1 Sección Hero (Inicio)
```html
<section id="banner">
    <div class="inner">
        <h1>CimaCritics</h1>
        <p>Descubre y comparte reseñas de cómics</p>
        <ul class="actions">
            <li><a href="#comics" class="button big scrolly">Explorar Cómics</a></li>
        </ul>
    </div>
</section>
```

### 3.2 Sección de Cómics Destacados
```html
<section id="comics" class="wrapper style1 special">
    <div class="inner">
        <header class="major">
            <h2>Cómics Destacados</h2>
            <p>Los mejores cómics según nuestra comunidad</p>
        </header>
        <div class="grid" id="comics-container">
            <!-- Cómics se cargan dinámicamente -->
        </div>
        <ul class="actions">
            <li><a href="/comics" class="button">Ver Todos</a></li>
        </ul>
    </div>
</section>
```

### 3.3 Sección de Estadísticas
```html
<section id="stats" class="wrapper alt style2">
    <div class="inner">
        <div class="statistics">
            <div class="statistic">
                <div class="value" id="total-comics">0</div>
                <div class="label">Cómics</div>
            </div>
            <div class="statistic">
                <div class="value" id="total-reviews">0</div>
                <div class="label">Reseñas</div>
            </div>
            <div class="statistic">
                <div class="value" id="total-users">0</div>
                <div class="label">Usuarios</div>
            </div>
        </div>
    </div>
</section>
```

### 3.4 Sección de Búsqueda
```html
<section id="search" class="wrapper style3">
    <div class="inner">
        <header class="major">
            <h2>Buscar Cómics</h2>
        </header>
        <div class="search-box">
            <input type="text" id="search-input" placeholder="Buscar por título, autor...">
            <button id="search-btn" class="button special">Buscar</button>
        </div>
        <div class="filters">
            <select id="genre-filter">
                <option value="">Todos los géneros</option>
            </select>
            <select id="publisher-filter">
                <option value="">Todas las editoriales</option>
            </select>
        </div>
    </div>
</section>
```

## 4. Páginas Específicas

### 4.1 Página de Detalles de Cómic
```html
<section id="comic-detail" class="wrapper style1">
    <div class="inner">
        <div class="comic-header">
            <div class="comic-image">
                <img id="comic-cover" src="" alt="">
            </div>
            <div class="comic-info">
                <h1 id="comic-title"></h1>
                <div class="meta">
                    <span id="comic-author"></span> |
                    <span id="comic-publisher"></span> |
                    <span id="comic-year"></span>
                </div>
                <div class="rating">
                    <div class="stars" id="comic-rating"></div>
                    <span id="rating-count"></span>
                </div>
                <div class="actions">
                    <button id="write-review-btn" class="button special">Escribir Reseña</button>
                </div>
            </div>
        </div>

        <div class="comic-description">
            <h3>Descripción</h3>
            <p id="comic-description"></p>
        </div>

        <div class="reviews-section">
            <h3>Reseñas</h3>
            <div id="reviews-container"></div>
        </div>
    </div>
</section>
```

### 4.2 Modal de Autenticación
```html
<div id="auth-modal" class="modal">
    <div class="modal-content">
        <div class="modal-header">
            <h3 id="modal-title">Iniciar Sesión</h3>
            <span class="close-modal">&times;</span>
        </div>
        <div class="modal-body">
            <form id="auth-form">
                <div class="form-group">
                    <label for="email">Email</label>
                    <input type="email" id="email" required>
                </div>
                <div class="form-group">
                    <label for="password">Contraseña</label>
                    <input type="password" id="password" required>
                </div>
                <div class="form-group" id="confirm-password-group" style="display: none;">
                    <label for="confirm-password">Confirmar Contraseña</label>
                    <input type="password" id="confirm-password">
                </div>
                <button type="submit" class="button special">Iniciar Sesión</button>
            </form>
            <p class="auth-toggle">
                ¿No tienes cuenta? <a href="#" id="toggle-auth">Regístrate</a>
            </p>
        </div>
    </div>
</div>
```

## 5. Componentes Reutilizables

### 5.1 Tarjeta de Cómic
```html
<div class="comic-card">
    <div class="image">
        <img src="comic-image.jpg" alt="Título del cómic">
    </div>
    <div class="content">
        <h3>Título del Cómic</h3>
        <p class="author">Autor</p>
        <div class="rating">
            <div class="stars">★★★★☆</div>
            <span class="value">(4.2)</span>
        </div>
        <a href="/comic/1" class="button small">Ver Detalles</a>
    </div>
</div>
```

### 5.2 Reseña Individual
```html
<div class="review">
    <div class="review-header">
        <div class="user-info">
            <span class="username">Usuario123</span>
            <div class="rating">
                <div class="stars">★★★★★</div>
            </div>
        </div>
        <div class="review-date">Hace 2 días</div>
    </div>
    <div class="review-content">
        <p>Excelente cómic, muy recomendado...</p>
    </div>
    <div class="review-actions">
        <button class="like-btn">👍 12</button>
        <button class="dislike-btn">👎 2</button>
    </div>
</div>
```

## 6. Consideraciones de Accesibilidad
- Navegación por teclado completa
- Texto alternativo en imágenes
- Contraste de colores adecuado
- Etiquetas semánticas HTML5
- ARIA labels donde sea necesario

## 7. Responsive Design
- Breakpoints optimizados para móviles
- Navegación colapsable en móviles
- Grid adaptable
- Tipografía escalable

## 8. Integración con Backend
- Carga dinámica de contenido via JavaScript
- Estados de carga y error
- Actualización en tiempo real de ratings
- Sistema de autenticación integrado