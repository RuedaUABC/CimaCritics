// CimaCritics - JavaScript principal

document.addEventListener('DOMContentLoaded', function() {
    // Inicializar tooltips de Bootstrap
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Auto-ocultar alerts después de 5 segundos
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function(alert) {
        if (!alert.classList.contains('alert-permanent')) {
            setTimeout(function() {
                const bsAlert = new bootstrap.Alert(alert);
                bsAlert.close();
            }, 5000);
        }
    });

    // Confirmación para acciones destructivas
    const confirmButtons = document.querySelectorAll('[data-confirm]');
    confirmButtons.forEach(function(button) {
        button.addEventListener('click', function(e) {
            const message = this.getAttribute('data-confirm') || '¿Estás seguro?';
            if (!confirm(message)) {
                e.preventDefault();
            }
        });
    });

    // Loading states para formularios
    const forms = document.querySelectorAll('form');
    forms.forEach(function(form) {
        form.addEventListener('submit', function() {
            const submitBtn = form.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Procesando...';
            }
        });
    });

    // Lazy loading para imágenes
    const images = document.querySelectorAll('img[data-src]');
    const imageObserver = new IntersectionObserver(function(entries, observer) {
        entries.forEach(function(entry) {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.classList.remove('lazy');
                imageObserver.unobserve(img);
            }
        });
    });

    images.forEach(function(img) {
        imageObserver.observe(img);
    });

    // Búsqueda en tiempo real (futuro)
    const searchInputs = document.querySelectorAll('.search-input');
    searchInputs.forEach(function(input) {
        let timeout;
        input.addEventListener('input', function() {
            clearTimeout(timeout);
            timeout = setTimeout(function() {
                // Implementar búsqueda AJAX aquí
                console.log('Buscando:', input.value);
            }, 300);
        });
    });

    // Toggle para filtros móviles
    const filterToggle = document.querySelector('.filter-toggle');
    if (filterToggle) {
        filterToggle.addEventListener('click', function() {
            const filters = document.querySelector('.filters');
            filters.classList.toggle('show');
        });
    }

    // Animación de fade-in para elementos
    const fadeElements = document.querySelectorAll('.fade-in');
    const fadeObserver = new IntersectionObserver(function(entries) {
        entries.forEach(function(entry) {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, { threshold: 0.1 });

    fadeElements.forEach(function(el) {
        el.style.opacity = '0';
        el.style.transform = 'translateY(20px)';
        el.style.transition = 'opacity 0.5s, transform 0.5s';
        fadeObserver.observe(el);
    });

    // Contador de caracteres para textareas
    const textareas = document.querySelectorAll('textarea[maxlength]');
    textareas.forEach(function(textarea) {
        const maxLength = textarea.getAttribute('maxlength');
        const counter = document.createElement('small');
        counter.className = 'text-muted float-end';
        textarea.parentNode.appendChild(counter);

        function updateCounter() {
            const remaining = maxLength - textarea.value.length;
            counter.textContent = `${remaining} caracteres restantes`;
        }

        textarea.addEventListener('input', updateCounter);
        updateCounter();
    });

    console.log('CimaCritics JavaScript cargado correctamente');
});

// Funciones de utilidad
function showToast(message, type = 'info') {
    // Implementar sistema de toasts aquí
    console.log(`${type.toUpperCase()}: ${message}`);
}

function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(function() {
        showToast('Copiado al portapapeles', 'success');
    });
}

// Rating system helper
function setRating(rating) {
    const stars = document.querySelectorAll('.rating input[type="radio"]');
    stars.forEach(function(star, index) {
        if (index < rating) {
            star.checked = true;
        }
    });
}