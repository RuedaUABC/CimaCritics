# ⚡ JavaScript - Frontend (Phantom Theme)

## 1. Arquitectura JavaScript
- **Vanilla JavaScript**: Sin frameworks inicialmente
- **Módulos ES6**: Organización modular
- **Async/Await**: Operaciones asíncronas
- **Event Delegation**: Manejo eficiente de eventos
- **Compatible con Phantom**: Adaptado al template HTML5 UP

## 2. Estructura de Archivos
```
js/
├── app.js              # Archivo principal - Inicialización
├── api.js              # Cliente API REST
├── auth.js             # Gestión de autenticación
├── comics.js           # Gestión de cómics
├── reviews.js          # Gestión de reseñas
├── ui.js               # Utilidades de UI (Phantom-adapted)
├── navigation.js       # Navegación móvil (Phantom)
├── parallax.js         # Efectos parallax (Phantom)
├── config.js           # Configuración
└── custom.js           # Funcionalidades específicas CimaCritics
```

## 3. Configuración (config.js)
```javascript
const CONFIG = {
  API_BASE_URL: 'http://localhost:5000/api',
  ITEMS_PER_PAGE: 20,
  DEBOUNCE_DELAY: 300,
  TOKEN_KEY: 'cima_critics_token',
  USER_KEY: 'cima_critics_user',
  
  // Configuración Phantom
  BREAKPOINT_MOBILE: 736,
  BREAKPOINT_TABLET: 980,
  SCROLL_OFFSET: 100,
  
  // Selectores Phantom
  SELECTORS: {
    navToggle: '#navPanelToggle',
    navPanel: '#menu',
    main: '#main',
    banner: '#banner',
    wrappers: '.wrapper'
  }
};

export default CONFIG;
```

## 4. Cliente de API (api.js)
```javascript
import CONFIG from './config.js';

class ApiClient {
  constructor() {
    this.baseURL = CONFIG.API_BASE_URL;
  }

  async request(endpoint, options = {}) {
    const url = `${this.baseURL}${endpoint}`;
    const config = {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers
      },
      ...options
    };

    // Agregar token si existe
    const token = localStorage.getItem(CONFIG.TOKEN_KEY);
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }

    try {
      const response = await fetch(url, config);
      
      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.message || 'Error en la solicitud');
      }
      
      return await response.json();
    } catch (error) {
      console.error('API Error:', error);
      throw error;
    }
  }

  // Métodos específicos
  async getComics(params = {}) {
    const queryString = new URLSearchParams(params).toString();
    return this.request(`/comics?${queryString}`);
  }

  async getComic(id) {
    return this.request(`/comics/${id}`);
  }

  async createReview(reviewData) {
    return this.request('/reviews', {
      method: 'POST',
      body: JSON.stringify(reviewData)
    });
  }

  async login(credentials) {
    return this.request('/auth/login', {
      method: 'POST',
      body: JSON.stringify(credentials)
    });
  }

  async register(userData) {
    return this.request('/auth/register', {
      method: 'POST',
      body: JSON.stringify(userData)
    });
  }
}

export default new ApiClient();
```

## 5. Navegación Móvil (navigation.js)
```javascript
import CONFIG from './config.js';

class NavigationManager {
  constructor() {
    this.isOpen = false;
    this.init();
  }

  init() {
    this.bindEvents();
    this.handleResize();
  }

  bindEvents() {
    // Toggle del menú móvil
    const navToggle = document.querySelector(CONFIG.SELECTORS.navToggle);
    const navPanel = document.querySelector(CONFIG.SELECTORS.navPanel);
    
    if (navToggle) {
      navToggle.addEventListener('click', (e) => {
        e.preventDefault();
        this.toggleMenu();
      });
    }

    // Cerrar menú al hacer click en enlaces
    if (navPanel) {
      navPanel.querySelectorAll('a').forEach(link => {
        link.addEventListener('click', () => {
          this.closeMenu();
        });
      });

      // Cerrar menú al hacer click fuera
      navPanel.querySelector('.close').addEventListener('click', () => {
        this.closeMenu();
      });
    }

    // Manejar resize de ventana
    window.addEventListener('resize', () => this.handleResize());
  }

  toggleMenu() {
    this.isOpen ? this.closeMenu() : this.openMenu();
  }

  openMenu() {
    const navPanel = document.querySelector(CONFIG.SELECTORS.navPanel);
    if (navPanel) {
      navPanel.style.display = 'block';
      document.body.classList.add('is-menu-visible');
      this.isOpen = true;
    }
  }

  closeMenu() {
    const navPanel = document.querySelector(CONFIG.SELECTORS.navPanel);
    if (navPanel) {
      navPanel.style.display = 'none';
      document.body.classList.remove('is-menu-visible');
      this.isOpen = false;
    }
  }

  handleResize() {
    if (window.innerWidth > CONFIG.BREAKPOINT_MOBILE) {
      this.closeMenu();
    }
  }
}

export default new NavigationManager();
```

## 6. Efectos Parallax (parallax.js)
```javascript
import CONFIG from './config.js';

class ParallaxManager {
  constructor() {
    this.elements = [];
    this.init();
  }

  init() {
    this.findParallaxElements();
    this.bindEvents();
  }

  findParallaxElements() {
    // Banner con background-attachment: fixed
    const banner = document.querySelector(CONFIG.SELECTORS.banner);
    if (banner) {
      this.elements.push({
        element: banner,
        type: 'background'
      });
    }

    // Elementos con data-parallax
    document.querySelectorAll('[data-parallax]').forEach(el => {
      this.elements.push({
        element: el,
        type: 'transform',
        speed: parseFloat(el.dataset.parallax) || 0.5
      });
    });
  }

  bindEvents() {
    window.addEventListener('scroll', () => this.updateParallax());
    this.updateParallax(); // Inicial
  }

  updateParallax() {
    const scrolled = window.pageYOffset;
    
    this.elements.forEach(item => {
      if (this.isElementVisible(item.element)) {
        switch (item.type) {
          case 'transform':
            const yPos = -(scrolled * item.speed);
            item.element.style.transform = `translateY(${yPos}px)`;
            break;
          case 'background':
            // El background-attachment: fixed maneja esto automáticamente
            break;
        }
      }
    });
  }

  isElementVisible(element) {
    const rect = element.getBoundingClientRect();
    return rect.top < window.innerHeight && rect.bottom > 0;
  }
}

export default new ParallaxManager();
```

## 7. Gestión de Autenticación (auth.js)
```javascript
import CONFIG from './config.js';
import api from './api.js';

class AuthManager {
  constructor() {
    this.currentUser = null;
    this.modal = null;
    this.init();
  }

  init() {
    const token = localStorage.getItem(CONFIG.TOKEN_KEY);
    const user = localStorage.getItem(CONFIG.USER_KEY);
    
    if (token && user) {
      this.currentUser = JSON.parse(user);
      this.updateUI();
    }

    this.createAuthModal();
    this.bindEvents();
  }

  createAuthModal() {
    const modalHTML = `
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
    `;
    
    document.body.insertAdjacentHTML('beforeend', modalHTML);
    this.modal = document.getElementById('auth-modal');
  }

  bindEvents() {
    // Botones de login/register
    document.addEventListener('click', (e) => {
      if (e.target.matches('#login-btn, #register-btn')) {
        e.preventDefault();
        this.showModal(e.target.id === 'register-btn');
      }
    });

    // Logout
    document.addEventListener('click', (e) => {
      if (e.target.matches('#logout-btn')) {
        e.preventDefault();
        this.logout();
      }
    });

    // Modal events
    if (this.modal) {
      this.modal.addEventListener('click', (e) => {
        if (e.target.classList.contains('close-modal') || e.target.classList.contains('modal')) {
          this.hideModal();
        }
      });

      // Form submission
      const form = this.modal.querySelector('#auth-form');
      form.addEventListener('submit', (e) => {
        e.preventDefault();
        this.handleAuth();
      });

      // Toggle between login/register
      const toggleLink = this.modal.querySelector('#toggle-auth');
      toggleLink.addEventListener('click', (e) => {
        e.preventDefault();
        const isRegister = this.modal.querySelector('#modal-title').textContent === 'Registrarse';
        this.showModal(!isRegister);
      });
    }
  }

  async handleAuth() {
    const form = this.modal.querySelector('#auth-form');
    const formData = new FormData(form);
    
    const isRegister = this.modal.querySelector('#modal-title').textContent === 'Registrarse';
    
    const data = {
      nombre: formData.get('nombre') || '',
      email: formData.get('email'),
      password: formData.get('password')
    };

    try {
      const result = isRegister ? 
        await this.register(data) : 
        await this.login({ email: data.email, password: data.password });
      
      if (result.success) {
        this.hideModal();
        this.showNotification('¡Bienvenido!', 'success');
      } else {
        this.showNotification(result.error, 'error');
      }
    } catch (error) {
      this.showNotification('Error de conexión', 'error');
    }
  }

  async login(credentials) {
    try {
      const response = await api.login(credentials);
      
      localStorage.setItem(CONFIG.TOKEN_KEY, response.access_token);
      localStorage.setItem(CONFIG.USER_KEY, JSON.stringify(response.usuario));
      
      this.currentUser = response.usuario;
      this.updateUI();
      
      return { success: true };
    } catch (error) {
      return { success: false, error: error.message };
    }
  }

  async register(userData) {
    try {
      const response = await api.register(userData);
      return this.login({ email: userData.email, password: userData.password });
    } catch (error) {
      return { success: false, error: error.message };
    }
  }

  logout() {
    localStorage.removeItem(CONFIG.TOKEN_KEY);
    localStorage.removeItem(CONFIG.USER_KEY);
    this.currentUser = null;
    this.updateUI();
    window.location.href = '/';
  }

  showModal(isRegister = false) {
    if (!this.modal) return;
    
    const title = this.modal.querySelector('#modal-title');
    const confirmGroup = this.modal.querySelector('#confirm-password-group');
    const toggleLink = this.modal.querySelector('#toggle-auth');
    const submitBtn = this.modal.querySelector('button[type="submit"]');
    
    if (isRegister) {
      title.textContent = 'Registrarse';
      confirmGroup.style.display = 'block';
      toggleLink.textContent = '¿Ya tienes cuenta? Inicia sesión';
      submitBtn.textContent = 'Registrarse';
    } else {
      title.textContent = 'Iniciar Sesión';
      confirmGroup.style.display = 'none';
      toggleLink.textContent = '¿No tienes cuenta? Regístrate';
      submitBtn.textContent = 'Iniciar Sesión';
    }
    
    this.modal.classList.add('show');
  }

  hideModal() {
    if (this.modal) {
      this.modal.classList.remove('show');
    }
  }

  updateUI() {
    const navPanel = document.querySelector(CONFIG.SELECTORS.navPanel);
    if (!navPanel) return;
    
    const links = navPanel.querySelector('.links');
    
    if (this.isLoggedIn()) {
      // Cambiar "Iniciar Sesión" por "Perfil" y agregar "Cerrar Sesión"
      const loginLink = links.querySelector('a[href="/login"]');
      if (loginLink) {
        loginLink.textContent = 'Perfil';
        loginLink.href = '/profile';
      }
      
      // Agregar enlace de logout si no existe
      if (!links.querySelector('a[href="#logout"]')) {
        const logoutLi = document.createElement('li');
        logoutLi.innerHTML = '<a href="#logout" id="logout-link">Cerrar Sesión</a>';
        links.appendChild(logoutLi);
      }
    } else {
      // Restaurar enlace de login
      const profileLink = links.querySelector('a[href="/profile"]');
      if (profileLink) {
        profileLink.textContent = 'Iniciar Sesión';
        profileLink.href = '/login';
      }
      
      // Remover enlace de logout
      const logoutLink = links.querySelector('#logout-link');
      if (logoutLink) {
        logoutLink.parentElement.remove();
      }
    }
  }

  isLoggedIn() {
    return !!this.currentUser;
  }

  showNotification(message, type = 'info') {
    // Implementar sistema de notificaciones
    console.log(`${type}: ${message}`);
  }
}

export default new AuthManager();
```

## 8. Gestión de Cómics (comics.js)
```javascript
import api from './api.js';
import { createComicCard, showLoading, hideLoading } from './ui.js';

class ComicsManager {
  constructor() {
    this.currentPage = 1;
    this.filters = {};
    this.init();
  }

  init() {
    this.bindEvents();
    this.loadComics();
  }

  bindEvents() {
    // Búsqueda con debounce
    const searchInput = document.getElementById('search-input');
    if (searchInput) {
      searchInput.addEventListener('input', this.debounce(this.handleSearch.bind(this), CONFIG.DEBOUNCE_DELAY));
    }

    // Botón de búsqueda
    const searchBtn = document.getElementById('search-btn');
    if (searchBtn) {
      searchBtn.addEventListener('click', this.handleSearch.bind(this));
    }

    // Filtros
    ['genre', 'publisher'].forEach(filter => {
      const element = document.getElementById(`${filter}-filter`);
      if (element) {
        element.addEventListener('change', this.handleFilter.bind(this));
      }
    });

    // Scroll infinito (opcional)
    this.setupInfiniteScroll();
  }

  async loadComics(append = false) {
    try {
      showLoading();
      
      const params = {
        page: this.currentPage,
        per_page: CONFIG.ITEMS_PER_PAGE,
        ...this.filters
      };
      
      const response = await api.getComics(params);
      
      if (append) {
        this.appendComics(response.comics);
      } else {
        this.renderComics(response.comics);
      }
      
      this.updatePagination(response);
      
    } catch (error) {
      console.error('Error loading comics:', error);
      this.showError('Error al cargar los cómics');
    } finally {
      hideLoading();
    }
  }

  renderComics(comics) {
    const container = document.getElementById('comics-container');
    if (!container) return;
    
    container.innerHTML = '';
    
    if (comics.length === 0) {
      container.innerHTML = '<p class="no-results">No se encontraron cómics</p>';
      return;
    }
    
    comics.forEach(comic => {
      const card = createComicCard(comic);
      container.appendChild(card);
    });
  }

  appendComics(comics) {
    const container = document.getElementById('comics-container');
    if (!container) return;
    
    comics.forEach(comic => {
      const card = createComicCard(comic);
      container.appendChild(card);
    });
  }

  updatePagination(data) {
    // Para diseño Phantom, usamos botones simples
    const loadMoreBtn = document.getElementById('load-more-btn');
    if (loadMoreBtn) {
      const hasMore = this.currentPage * CONFIG.ITEMS_PER_PAGE < data.total;
      loadMoreBtn.style.display = hasMore ? 'block' : 'none';
    }
  }

  handleSearch() {
    const query = document.getElementById('search-input')?.value;
    this.filters.titulo = query || undefined;
    this.currentPage = 1;
    this.loadComics();
  }

  handleFilter(event) {
    const { id, value } = event.target;
    const filterKey = id.replace('-filter', '');
    this.filters[filterKey] = value || undefined;
    this.currentPage = 1;
    this.loadComics();
  }

  setupInfiniteScroll() {
    // Implementar scroll infinito para mejor UX
    let loading = false;
    
    window.addEventListener('scroll', () => {
      if (loading) return;
      
      const scrollTop = window.pageYOffset;
      const windowHeight = window.innerHeight;
      const documentHeight = document.documentElement.scrollHeight;
      
      if (scrollTop + windowHeight >= documentHeight - 1000) {
        loading = true;
        this.currentPage++;
        this.loadComics(true).finally(() => {
          loading = false;
        });
      }
    });
  }

  debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
      const later = () => {
        clearTimeout(timeout);
        func(...args);
      };
      clearTimeout(timeout);
      timeout = setTimeout(later, wait);
    };
  }

  showError(message) {
    const container = document.getElementById('comics-container');
    if (container) {
      container.innerHTML = `<p class="error">${message}</p>`;
    }
  }
}

export default new ComicsManager();
```

## 9. Utilidades de UI (ui.js)
```javascript
// Crear tarjeta de cómic (Phantom style)
export function createComicCard(comic) {
  const card = document.createElement('div');
  card.className = 'comic-card';
  
  card.innerHTML = `
    <div class="image">
      <img src="${comic.imagen_url || '/images/default-comic.jpg'}" 
           alt="${comic.titulo}" loading="lazy">
    </div>
    <div class="content">
      <h3>${comic.titulo}</h3>
      <p class="author">${comic.autor}</p>
      <div class="rating">
        <div class="stars">${generateStars(comic.promedio_calificacion)}</div>
        <span class="value">(${comic.promedio_calificacion.toFixed(1)})</span>
      </div>
      <a href="/comic/${comic.id}" class="button small">Ver Detalles</a>
    </div>
  `;
  
  return card;
}

// Generar estrellas
export function generateStars(rating) {
  const fullStars = Math.floor(rating);
  const hasHalfStar = rating % 1 >= 0.5;
  const emptyStars = 5 - fullStars - (hasHalfStar ? 1 : 0);
  
  return '★'.repeat(fullStars) + 
         (hasHalfStar ? '☆' : '') + 
         '☆'.repeat(emptyStars);
}

// Loading states
export function showLoading() {
  let loader = document.getElementById('global-loader');
  if (!loader) {
    loader = document.createElement('div');
    loader.id = 'global-loader';
    loader.innerHTML = '<div class="loading"></div>';
    document.body.appendChild(loader);
  }
  loader.style.display = 'flex';
}

export function hideLoading() {
  const loader = document.getElementById('global-loader');
  if (loader) {
    loader.style.display = 'none';
  }
}

// Notificaciones (Phantom style)
export function showNotification(message, type = 'info') {
  const notification = document.createElement('div');
  notification.className = `notification notification-${type}`;
  notification.innerHTML = `
    <div class="notification-content">
      <span>${message}</span>
      <button class="notification-close">&times;</button>
    </div>
  `;
  
  document.body.appendChild(notification);
  
  // Auto-remover después de 5 segundos
  setTimeout(() => {
    if (notification.parentElement) {
      notification.remove();
    }
  }, 5000);
  
  // Click para cerrar
  notification.querySelector('.notification-close').addEventListener('click', () => {
    notification.remove();
  });
}

// Scrolly effect para botones
export function initScrolly() {
  document.querySelectorAll('.scrolly').forEach(element => {
    element.addEventListener('click', function(e) {
      e.preventDefault();
      
      const target = this.getAttribute('href');
      const targetElement = document.querySelector(target);
      
      if (targetElement) {
        const offset = targetElement.offsetTop - CONFIG.SCROLL_OFFSET;
        window.scrollTo({
          top: offset,
          behavior: 'smooth'
        });
      }
    });
  });
}

// Animaciones de entrada
export function initFadeIn() {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('fade-in');
      }
    });
  }, { threshold: 0.1 });
  
  document.querySelectorAll(CONFIG.SELECTORS.wrappers).forEach(wrapper => {
    observer.observe(wrapper);
  });
}
```

## 10. Archivo Principal (app.js)
```javascript
import CONFIG from './config.js';
import navigation from './navigation.js';
import parallax from './parallax.js';
import auth from './auth.js';
import comics from './comics.js';
import { initScrolly, initFadeIn } from './ui.js';

// Inicializar la aplicación
document.addEventListener('DOMContentLoaded', () => {
  console.log('CimaCritics app initialized with Phantom theme');
  
  // Prevenir animaciones durante carga
  document.body.classList.add('is-loading');
  
  // Inicializar componentes
  navigation.init();
  parallax.init();
  auth.init();
  
  // Inicializar funcionalidades según la página
  if (document.getElementById('comics-container')) {
    comics.init();
  }
  
  // Inicializar efectos UI
  initScrolly();
  initFadeIn();
  
  // Remover clase de carga después de inicialización
  setTimeout(() => {
    document.body.classList.remove('is-loading');
  }, 100);
});

// Global error handler
window.addEventListener('error', (e) => {
  console.error('Global error:', e.error);
});

// Unhandled promise rejections
window.addEventListener('unhandledrejection', (e) => {
  console.error('Unhandled promise rejection:', e.reason);
});
```