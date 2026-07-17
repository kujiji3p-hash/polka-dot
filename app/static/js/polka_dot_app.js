/* ============================================
   POLKA DOT v1.0 — Application JavaScript
   ============================================ */

document.addEventListener('DOMContentLoaded', function() {
    initMobileMenu();
    initFlashMessages();
    initHeaderScroll();
    initSmoothScroll();
});

/* ============================================
   MOBILE MENU
   ============================================ */

function toggleMenu() {
    const menu = document.getElementById('mobileMenu');
    const toggle = document.querySelector('.pd-menu-toggle');

    if (menu) {
        menu.classList.toggle('active');
        toggle.classList.toggle('active');
        document.body.style.overflow = menu.classList.contains('active') ? 'hidden' : '';
    }
}

function initMobileMenu() {
    // Close menu when clicking on a link
    const menuLinks = document.querySelectorAll('.pd-mobile-menu a');
    menuLinks.forEach(link => {
        link.addEventListener('click', () => {
            toggleMenu();
        });
    });

    // Close menu on escape key
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            const menu = document.getElementById('mobileMenu');
            if (menu && menu.classList.contains('active')) {
                toggleMenu();
            }
            // Close any open modals
            closeAllModals();
        }
    });
}

/* ============================================
   FLASH MESSAGES
   ============================================ */

function initFlashMessages() {
    const flashes = document.querySelectorAll('.pd-flash');
    flashes.forEach(flash => {
        // Auto-remove after animation completes
        setTimeout(() => {
            flash.style.opacity = '0';
            flash.style.transform = 'translateX(100%)';
            setTimeout(() => flash.remove(), 400);
        }, 5000);
    });
}

/* ============================================
   HEADER SCROLL EFFECT
   ============================================ */

function initHeaderScroll() {
    const header = document.querySelector('.pd-header');
    let lastScroll = 0;

    window.addEventListener('scroll', () => {
        const currentScroll = window.pageYOffset;

        if (currentScroll > 100) {
            header.style.boxShadow = '0 2px 20px rgba(0,0,0,0.08)';
        } else {
            header.style.boxShadow = 'none';
        }

        lastScroll = currentScroll;
    });
}

/* ============================================
   SMOOTH SCROLL
   ============================================ */

function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                e.preventDefault();
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

/* ============================================
   MODALS
   ============================================ */

function openModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.add('active');
        document.body.style.overflow = 'hidden';
    }
}

function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.remove('active');
        document.body.style.overflow = '';
    }
}

function closeAllModals() {
    document.querySelectorAll('.pd-modal').forEach(modal => {
        modal.classList.remove('active');
    });
    document.body.style.overflow = '';
}

// Close modal on overlay click
document.querySelectorAll('.pd-modal-overlay').forEach(overlay => {
    overlay.addEventListener('click', function() {
        this.parentElement.classList.remove('active');
        document.body.style.overflow = '';
    });
});

/* ============================================
   PREORDER MODAL
   ============================================ */

function openPreorderModal(productId, name, price) {
    const modal = document.getElementById('preorderModal');
    if (!modal) return;

    const idInput = document.getElementById('preorderProductId');
    const nameEl = document.getElementById('preorderProductName');
    const priceEl = document.getElementById('preorderProductPrice');

    if (idInput) idInput.value = productId;
    if (nameEl) nameEl.textContent = name;
    if (priceEl) priceEl.textContent = price + ' ₽';

    modal.classList.add('active');
    document.body.style.overflow = 'hidden';
}

function closePreorderModal() {
    closeModal('preorderModal');
}

/* ============================================
   FORM VALIDATION
   ============================================ */

function validateForm(form) {
    const inputs = form.querySelectorAll('input[required], textarea[required]');
    let isValid = true;

    inputs.forEach(input => {
        if (!input.value.trim()) {
            isValid = false;
            input.style.borderColor = '#ff4444';
            input.style.boxShadow = '0 0 0 4px rgba(255,68,68,0.1)';
        } else {
            input.style.borderColor = '';
            input.style.boxShadow = '';
        }
    });

    return isValid;
}

// Auto-clear validation styles on input
document.querySelectorAll('input, textarea').forEach(input => {
    input.addEventListener('input', function() {
        this.style.borderColor = '';
        this.style.boxShadow = '';
    });
});

/* ============================================
   LAZY LOADING IMAGES
   ============================================ */

if ('IntersectionObserver' in window) {
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                if (img.dataset.src) {
                    img.src = img.dataset.src;
                    img.removeAttribute('data-src');
                }
                observer.unobserve(img);
            }
        });
    });

    document.querySelectorAll('img[data-src]').forEach(img => {
        imageObserver.observe(img);
    });
}

/* ============================================
   INTERSECTION ANIMATIONS
   ============================================ */

const animateOnScroll = () => {
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, { threshold: 0.1 });

    document.querySelectorAll('.pd-product-card, .pd-timeline-item, .pd-feature-card').forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(20px)';
        el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(el);
    });
};

if ('IntersectionObserver' in window) {
    animateOnScroll();
}

/* ============================================
   COPY TO CLIPBOARD (for SKU, etc.)
   ============================================ */

function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        // Show temporary toast
        const toast = document.createElement('div');
        toast.textContent = 'Скопировано!';
        toast.style.cssText = `
            position: fixed;
            bottom: 24px; left: 50%;
            transform: translateX(-50%);
            background: #0a0a0a; color: white;
            padding: 12px 24px;
            border-radius: 12px;
            font-size: 14px; font-weight: 500;
            z-index: 9999;
            animation: slideUp 0.3s ease;
        `;
        document.body.appendChild(toast);
        setTimeout(() => {
            toast.style.animation = 'slideDown 0.3s ease forwards';
            setTimeout(() => toast.remove(), 300);
        }, 2000);
    });
}

/* ============================================
   PRODUCT FILTER (client-side fallback)
   ============================================ */

function filterProducts(category, btn) {
    // Update active tab
    document.querySelectorAll('.pd-tab').forEach(t => t.classList.remove('active'));
    if (btn) btn.classList.add('active');

    // Filter cards
    document.querySelectorAll('.pd-product-card').forEach(card => {
        const cardCategory = card.dataset.category;
        if (category === 'all' || cardCategory === category) {
            card.style.display = 'block';
            card.style.animation = 'fadeIn 0.4s ease';
        } else {
            card.style.display = 'none';
        }
    });
}

/* ============================================
   PRINT STYLES
   ============================================ */

window.addEventListener('beforeprint', () => {
    document.querySelectorAll('.pd-pattern, .pd-header, .pd-footer').forEach(el => {
        el.style.display = 'none';
    });
});
