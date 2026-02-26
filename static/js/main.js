/**
 * Django Portfolio - Main JavaScript
 * Modern interactions and animations
 */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize AOS Animation Library
    if (typeof AOS !== 'undefined') {
        AOS.init({
            duration: 800,
            easing: 'ease-out-cubic',
            once: true,
            offset: 100,
            disable: window.matchMedia('(prefers-reduced-motion: reduce)').matches
        });
    }
    
    // ========================================
    // Navbar Scroll Effect
    // ========================================
    const navbar = document.getElementById('mainNav');
    
    function handleNavbarScroll() {
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    }
    
    if (navbar) {
        window.addEventListener('scroll', handleNavbarScroll, { passive: true });
        handleNavbarScroll(); // Check on load
    }
    
    // ========================================
    // Theme Toggle (Dark/Light Mode)
    // ========================================
    const themeToggle = document.getElementById('themeToggle');
    const html = document.documentElement;
    
    // Check for saved theme preference
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme) {
        html.setAttribute('data-bs-theme', savedTheme);
    } else {
        // Check system preference
        const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
        html.setAttribute('data-bs-theme', prefersDark ? 'dark' : 'light');
    }
    
    if (themeToggle) {
        themeToggle.addEventListener('click', function() {
            const currentTheme = html.getAttribute('data-bs-theme');
            const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
            
            html.setAttribute('data-bs-theme', newTheme);
            localStorage.setItem('theme', newTheme);
            
            // Dispatch custom event for other components
            window.dispatchEvent(new CustomEvent('themechange', { 
                detail: { theme: newTheme } 
            }));
        });
    }
    
    // ========================================
    // Scroll to Top Button
    // ========================================
    const scrollToTopBtn = document.getElementById('scrollToTop');
    
    function handleScrollToTop() {
        if (window.scrollY > 500) {
            scrollToTopBtn.classList.add('visible');
        } else {
            scrollToTopBtn.classList.remove('visible');
        }
    }
    
    if (scrollToTopBtn) {
        window.addEventListener('scroll', handleScrollToTop, { passive: true });
        
        scrollToTopBtn.addEventListener('click', function() {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });
    }
    
    // ========================================
    // Smooth Scroll for Anchor Links
    // ========================================
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;
            
            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                e.preventDefault();
                
                const navbarHeight = navbar ? navbar.offsetHeight : 0;
                const targetPosition = targetElement.offsetTop - navbarHeight;
                
                window.scrollTo({
                    top: targetPosition,
                    behavior: 'smooth'
                });
                
                // Close mobile menu if open
                const navbarCollapse = document.querySelector('.navbar-collapse');
                if (navbarCollapse && navbarCollapse.classList.contains('show')) {
                    navbarCollapse.classList.remove('show');
                }
            }
        });
    });
    
    // ========================================
    // Skill Bars Animation
    // ========================================
    const skillBars = document.querySelectorAll('.skill-progress');
    
    function animateSkillBars() {
        skillBars.forEach(bar => {
            const rect = bar.getBoundingClientRect();
            const isVisible = rect.top < window.innerHeight && rect.bottom > 0;
            
            if (isVisible) {
                const width = bar.style.width;
                bar.style.width = '0';
                setTimeout(() => {
                    bar.style.width = width;
                }, 100);
            }
        });
    }
    
    // Animate on scroll
    let skillBarsAnimated = false;
    window.addEventListener('scroll', function() {
        if (!skillBarsAnimated) {
            animateSkillBars();
            skillBarsAnimated = true;
        }
    }, { passive: true });
    
    // ========================================
    // Form Validation Enhancement
    // ========================================
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!form.checkValidity()) {
                e.preventDefault();
                e.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    });
    
    // ========================================
    // Contact Form AJAX Submission - FIXED
    // ========================================
    const contactForm = document.getElementById('contactForm');
    
    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(contactForm);
            const submitBtn = contactForm.querySelector('button[type="submit"]');
            const originalText = submitBtn.innerHTML;
            
            // Get CSRF token from the form
            const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
            
            // Show loading state
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Sending...';
            
            fetch(contactForm.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': csrfToken
                },
                credentials: 'same-origin'
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                // Check if response is JSON
                const contentType = response.headers.get('content-type');
                if (contentType && contentType.includes('application/json')) {
                    return response.json();
                }
                // If not JSON, assume success and redirect
                window.location.href = '/contact/success/';
                return null;
            })
            .then(data => {
                if (data) {
                    if (data.success) {
                        showNotification('success', data.message || 'Message sent successfully!');
                        contactForm.reset();
                        contactForm.classList.remove('was-validated');
                        // Redirect after short delay
                        setTimeout(() => {
                            window.location.href = '/contact/success/';
                        }, 1500);
                    } else {
                        showNotification('error', data.message || 'Something went wrong. Please try again.');
                        submitBtn.disabled = false;
                        submitBtn.innerHTML = originalText;
                    }
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showNotification('error', 'Network error. Please try again or refresh the page.');
                submitBtn.disabled = false;
                submitBtn.innerHTML = originalText;
            });
        });
    }
    
    // ========================================
    // Newsletter Form AJAX - FIXED
    // ========================================
    const newsletterForm = document.getElementById('newsletterForm');
    
    if (newsletterForm) {
        newsletterForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(newsletterForm);
            const submitBtn = newsletterForm.querySelector('button[type="submit"]');
            const originalText = submitBtn.innerHTML;
            const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
            
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';
            
            fetch(newsletterForm.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': csrfToken
                },
                credentials: 'same-origin'
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.text();
            })
            .then(html => {
                // Replace form with response (usually success message)
                newsletterForm.innerHTML = html;
            })
            .catch(error => {
                console.error('Error:', error);
                showNotification('error', 'Failed to subscribe. Please try again.');
                submitBtn.disabled = false;
                submitBtn.innerHTML = originalText;
            });
        });
    }
    
    // ========================================
    // Notification System
    // ========================================
    function showNotification(type, message) {
        // Remove existing notifications
        const existingNotifications = document.querySelectorAll('.notification');
        existingNotifications.forEach(n => n.remove());
        
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.innerHTML = `
            <div class="notification-content">
                <i class="fas fa-${type === 'success' ? 'check-circle' : 'exclamation-circle'}"></i>
                <span>${message}</span>
            </div>
            <button class="notification-close">
                <i class="fas fa-times"></i>
            </button>
        `;
        
        document.body.appendChild(notification);
        
        // Animate in
        requestAnimationFrame(() => {
            notification.classList.add('show');
        });
        
        // Auto dismiss
        setTimeout(() => {
            dismissNotification(notification);
        }, 5000);
        
        // Close button
        notification.querySelector('.notification-close').addEventListener('click', () => {
            dismissNotification(notification);
        });
    }
    
    function dismissNotification(notification) {
        notification.classList.remove('show');
        setTimeout(() => {
            notification.remove();
        }, 300);
    }
    
    // ========================================
    // Project Filter (if on projects page)
    // ========================================
    const projectFilters = document.querySelectorAll('.project-filter');
    const projectCards = document.querySelectorAll('.project-card');
    
    if (projectFilters.length && projectCards.length) {
        projectFilters.forEach(filter => {
            filter.addEventListener('click', function() {
                const category = this.dataset.filter;
                
                // Update active state
                projectFilters.forEach(f => f.classList.remove('active'));
                this.classList.add('active');
                
                // Filter projects
                projectCards.forEach(card => {
                    if (category === 'all' || card.dataset.category === category) {
                        card.style.display = 'block';
                        card.classList.add('fade-in');
                    } else {
                        card.style.display = 'none';
                        card.classList.remove('fade-in');
                    }
                });
            });
        });
    }
    
    // ========================================
    // Lazy Loading Images
    // ========================================
    const lazyImages = document.querySelectorAll('img[data-src]');
    
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.removeAttribute('data-src');
                    observer.unobserve(img);
                }
            });
        });
        
        lazyImages.forEach(img => imageObserver.observe(img));
    } else {
        // Fallback for older browsers
        lazyImages.forEach(img => {
            img.src = img.dataset.src;
        });
    }
    
    // ========================================
    // Search Functionality
    // ========================================
    const searchInput = document.getElementById('searchInput');
    const searchResults = document.getElementById('searchResults');
    
    if (searchInput && searchResults) {
        let searchTimeout;
        
        searchInput.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            const query = this.value.trim();
            
            if (query.length < 2) {
                searchResults.innerHTML = '';
                searchResults.classList.remove('show');
                return;
            }
            
            searchTimeout = setTimeout(() => {
                fetch(`/search/?q=${encodeURIComponent(query)}`, {
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest'
                    },
                    credentials: 'same-origin'
                })
                .then(response => response.text())
                .then(html => {
                    searchResults.innerHTML = html;
                    searchResults.classList.add('show');
                })
                .catch(error => {
                    console.error('Search error:', error);
                });
            }, 300);
        });
        
        // Close search results when clicking outside
        document.addEventListener('click', function(e) {
            if (!searchInput.contains(e.target) && !searchResults.contains(e.target)) {
                searchResults.classList.remove('show');
            }
        });
    }
    
    // ========================================
    // Code Syntax Highlighting (if needed)
    // ========================================
    if (typeof hljs !== 'undefined') {
        document.querySelectorAll('pre code').forEach((block) => {
            hljs.highlightElement(block);
        });
    }
    
    // ========================================
    // Copy to Clipboard
    // ========================================
    const copyButtons = document.querySelectorAll('.copy-btn');
    
    copyButtons.forEach(btn => {
        btn.addEventListener('click', function() {
            const targetId = this.dataset.target;
            const targetElement = document.getElementById(targetId);
            
            if (targetElement) {
                navigator.clipboard.writeText(targetElement.textContent).then(() => {
                    const originalText = this.innerHTML;
                    this.innerHTML = '<i class="fas fa-check"></i> Copied!';
                    
                    setTimeout(() => {
                        this.innerHTML = originalText;
                    }, 2000);
                }).catch(err => {
                    console.error('Copy failed:', err);
                    showNotification('error', 'Failed to copy text');
                });
            }
        });
    });
    
    // ========================================
    // Reading Progress Bar (for blog posts)
    // ========================================
    const progressBar = document.getElementById('readingProgress');
    
    if (progressBar) {
        window.addEventListener('scroll', function() {
            const scrollTop = window.scrollY;
            const docHeight = document.documentElement.scrollHeight - window.innerHeight;
            const scrollPercent = (scrollTop / docHeight) * 100;
            
            progressBar.style.width = scrollPercent + '%';
        }, { passive: true });
    }
    
    // ========================================
    // Mobile Menu Close on Link Click
    // ========================================
    const navLinks = document.querySelectorAll('.navbar-nav .nav-link');
    const navbarCollapse = document.querySelector('.navbar-collapse');
    
    navLinks.forEach(link => {
        link.addEventListener('click', () => {
            if (navbarCollapse && navbarCollapse.classList.contains('show')) {
                navbarCollapse.classList.remove('show');
            }
        });
    });
    
    // ========================================
    // Preloader (if exists)
    // ========================================
    const preloader = document.getElementById('preloader');
    
    if (preloader) {
        window.addEventListener('load', () => {
            preloader.classList.add('fade-out');
            setTimeout(() => {
                preloader.remove();
            }, 500);
        });
    }
    
    // ========================================
    // Counter Animation
    // ========================================
    const counters = document.querySelectorAll('.counter');
    
    function animateCounter(counter) {
        const target = parseInt(counter.dataset.target);
        const duration = 2000;
        const step = target / (duration / 16);
        let current = 0;
        
        const updateCounter = () => {
            current += step;
            if (current < target) {
                counter.textContent = Math.floor(current);
                requestAnimationFrame(updateCounter);
            } else {
                counter.textContent = target;
            }
        };
        
        updateCounter();
    }
    
    if (counters.length > 0 && 'IntersectionObserver' in window) {
        const counterObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    animateCounter(entry.target);
                    counterObserver.unobserve(entry.target);
                }
            });
        });
        
        counters.forEach(counter => counterObserver.observe(counter));
    }
    
    // ========================================
    // Parallax Effect (optional)
    // ========================================
    const parallaxElements = document.querySelectorAll('.parallax');
    
    if (parallaxElements.length > 0 && !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
        window.addEventListener('scroll', () => {
            const scrolled = window.scrollY;
            
            parallaxElements.forEach(el => {
                const speed = el.dataset.speed || 0.5;
                el.style.transform = `translateY(${scrolled * speed}px)`;
            });
        }, { passive: true });
    }
});

// ========================================
// Utility Functions
// ========================================

/**
 * Debounce function
 */
function debounce(func, wait) {
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

/**
 * Throttle function
 */
function throttle(func, limit) {
    let inThrottle;
    return function(...args) {
        if (!inThrottle) {
            func.apply(this, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}

/**
 * Format date
 */
function formatDate(date, format = 'short') {
    const d = new Date(date);
    const options = format === 'short' 
        ? { month: 'short', day: 'numeric', year: 'numeric' }
        : { month: 'long', day: 'numeric', year: 'numeric' };
    return d.toLocaleDateString('en-US', options);
}

/**
 * Check if element is in viewport
 */
function isInViewport(element) {
    const rect = element.getBoundingClientRect();
    return (
        rect.top >= 0 &&
        rect.left >= 0 &&
        rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
        rect.right <= (window.innerWidth || document.documentElement.clientWidth)
    );
}