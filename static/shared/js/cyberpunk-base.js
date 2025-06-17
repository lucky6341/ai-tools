// ===== TechyVia Base JavaScript ===== //

// Global variables
let particles = [];
let canvas, ctx;

// ===== Particle System ===== //
class Particle {
  constructor(x, y) {
    this.x = x;
    this.y = y;
    this.vx = (Math.random() - 0.5) * 0.5;
    this.vy = (Math.random() - 0.5) * 0.5;
    this.size = Math.random() * 2 + 1;
    this.life = 1.0;
    this.decay = Math.random() * 0.01 + 0.005;
    this.color = `hsl(${Math.random() * 60 + 180}, 70%, 60%)`;
  }

  update() {
    this.x += this.vx;
    this.y += this.vy;
    this.life -= this.decay;
    
    // Wrap around screen edges
    if (this.x < 0) this.x = canvas.width;
    if (this.x > canvas.width) this.x = 0;
    if (this.y < 0) this.y = canvas.height;
    if (this.y > canvas.height) this.y = 0;
  }

  draw() {
    ctx.globalAlpha = this.life * 0.6;
    ctx.fillStyle = this.color;
    ctx.beginPath();
    ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
    ctx.fill();
    
    // Add glow effect
    ctx.shadowBlur = 20;
    ctx.shadowColor = this.color;
    ctx.globalAlpha = this.life * 0.3;
    ctx.beginPath();
    ctx.arc(this.x, this.y, this.size * 2, 0, Math.PI * 2);
    ctx.fill();
    
    ctx.shadowBlur = 0;
    ctx.globalAlpha = 1;
  }

  isDead() {
    return this.life <= 0;
  }
}

function initParticles() {
  canvas = document.getElementById('particle-canvas');
  if (!canvas) return;
  
  ctx = canvas.getContext('2d');
  resizeCanvas();
  
  // Create initial particles
  for (let i = 0; i < 50; i++) {
    particles.push(new Particle(
      Math.random() * canvas.width,
      Math.random() * canvas.height
    ));
  }
  
  animateParticles();
}

function resizeCanvas() {
  if (!canvas) return;
  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;
}

function animateParticles() {
  if (!canvas || !ctx) return;
  
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  
  // Update and draw particles
  for (let i = particles.length - 1; i >= 0; i--) {
    particles[i].update();
    particles[i].draw();
    
    if (particles[i].isDead()) {
      particles.splice(i, 1);
    }
  }
  
  // Add new particles occasionally
  if (particles.length < 50 && Math.random() < 0.1) {
    particles.push(new Particle(
      Math.random() * canvas.width,
      Math.random() * canvas.height
    ));
  }
  
  requestAnimationFrame(animateParticles);
}

// ===== Navigation Functions ===== //
function initNavigation() {
  const navbar = document.getElementById('navbar');
  const navToggle = document.getElementById('nav-toggle');
  const navMenu = document.getElementById('nav-menu');
  
  // Navbar scroll effect
  window.addEventListener('scroll', () => {
    if (window.scrollY > 100) {
      navbar.classList.add('scrolled');
    } else {
      navbar.classList.remove('scrolled');
    }
    updateScrollProgress();
  });
  
  // Mobile menu toggle
  if (navToggle && navMenu) {
    navToggle.addEventListener('click', () => {
      navToggle.classList.toggle('active');
      navMenu.classList.toggle('active');
    });
    
    // Close mobile menu when clicking on links
    navMenu.addEventListener('click', (e) => {
      if (e.target.tagName === 'A') {
        navToggle.classList.remove('active');
        navMenu.classList.remove('active');
      }
    });
  }
}

function updateScrollProgress() {
  const scrollProgress = document.querySelector('.scroll-progress-bar');
  if (!scrollProgress) return;
  
  const windowHeight = window.innerHeight;
  const documentHeight = document.documentElement.scrollHeight - windowHeight;
  const scrolled = window.scrollY;
  const progress = (scrolled / documentHeight) * 100;
  
  scrollProgress.style.width = `${Math.min(progress, 100)}%`;
}

// ===== Smooth Scrolling ===== //
function scrollToSection(sectionId) {
  const element = document.getElementById(sectionId);
  if (element) {
    const navbarHeight = document.querySelector('.navbar').offsetHeight;
    const elementPosition = element.offsetTop - navbarHeight - 20;
    
    window.scrollTo({
      top: elementPosition,
      behavior: 'smooth'
    });
  }
}

// ===== Animation on Scroll ===== //
function initScrollAnimations() {
  const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
  };
  
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
      }
    });
  }, observerOptions);
  
  // Observe all elements with animate-on-scroll class
  document.querySelectorAll('.animate-on-scroll').forEach(el => {
    observer.observe(el);
  });
}

// ===== Back to Top Button ===== //
function initBackToTop() {
  const backToTopButton = document.getElementById('back-to-top');
  if (!backToTopButton) return;
  
  window.addEventListener('scroll', () => {
    if (window.scrollY > 300) {
      backToTopButton.classList.add('visible');
    } else {
      backToTopButton.classList.remove('visible');
    }
  });
  
  backToTopButton.addEventListener('click', () => {
    window.scrollTo({
      top: 0,
      behavior: 'smooth'
    });
  });
}

// ===== Notifications ===== //
function showNotification(message, type = 'success') {
  const notification = document.createElement('div');
  notification.className = `message message-${type}`;
  notification.innerHTML = `
    <i class="fas fa-${type === 'success' ? 'check-circle' : type === 'error' ? 'exclamation-circle' : type === 'warning' ? 'exclamation-triangle' : 'info-circle'}"></i>
    <span>${message}</span>
    <button class="message-close" onclick="this.parentElement.remove()">
      <i class="fas fa-times"></i>
    </button>
  `;
  
  // Add to messages container or create one
  let container = document.querySelector('.messages-container');
  if (!container) {
    container = document.createElement('div');
    container.className = 'messages-container';
    document.body.appendChild(container);
  }
  
  container.appendChild(notification);
  
  // Auto remove after 5 seconds
  setTimeout(() => {
    if (notification.parentElement) {
      notification.remove();
    }
  }, 5000);
}

// ===== Utility Functions ===== //
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

function throttle(func, limit) {
  let inThrottle;
  return function() {
    const args = arguments;
    const context = this;
    if (!inThrottle) {
      func.apply(context, args);
      inThrottle = true;
      setTimeout(() => inThrottle = false, limit);
    }
  }
}

// ===== Keyboard Navigation ===== //
function initKeyboardNavigation() {
  document.addEventListener('keydown', (e) => {
    // ESC key closes mobile menu
    if (e.key === 'Escape') {
      const navToggle = document.getElementById('nav-toggle');
      const navMenu = document.getElementById('nav-menu');
      
      if (navToggle && navMenu && navMenu.classList.contains('active')) {
        navToggle.classList.remove('active');
        navMenu.classList.remove('active');
      }
    }
  });
}

// ===== Performance Monitoring ===== //
function initPerformanceMonitoring() {
  // Monitor page load performance
  window.addEventListener('load', () => {
    if ('performance' in window) {
      const loadTime = performance.now();
      console.log(`TechyVia loaded in ${loadTime.toFixed(2)}ms`);
    }
  });
  
  // Monitor scroll performance
  const optimizedScroll = throttle(() => {
    updateScrollProgress();
  }, 16); // 60fps
  
  window.addEventListener('scroll', optimizedScroll);
}

// ===== Accessibility Enhancements ===== //
function initAccessibility() {
  // Add focus indicators for keyboard navigation
  const focusableElements = document.querySelectorAll('a, button, input, textarea, select');
  
  focusableElements.forEach(element => {
    element.addEventListener('focus', () => {
      element.style.outline = '2px solid var(--primary)';
      element.style.outlineOffset = '2px';
    });
    
    element.addEventListener('blur', () => {
      element.style.outline = '';
      element.style.outlineOffset = '';
    });
  });
}

// ===== Error Handling ===== //
function initErrorHandling() {
  window.addEventListener('error', (e) => {
    console.error('TechyVia Error:', e.error);
    
    // Show user-friendly error message for critical errors
    if (e.error && e.error.stack && e.error.stack.includes('critical')) {
      showNotification('Something went wrong. Please refresh the page.', 'error');
    }
  });
  
  window.addEventListener('unhandledrejection', (e) => {
    console.error('TechyVia Promise Rejection:', e.reason);
  });
}

// ===== Main Initialization ===== //
document.addEventListener('DOMContentLoaded', () => {
  console.log('🚀 TechyVia Base Initializing...');
  
  try {
    // Initialize all modules
    initParticles();
    initNavigation();
    initScrollAnimations();
    initBackToTop();
    initKeyboardNavigation();
    initPerformanceMonitoring();
    initAccessibility();
    initErrorHandling();
    
    console.log('✅ TechyVia Base Loaded Successfully');
    
  } catch (error) {
    console.error('❌ TechyVia Base Initialization Error:', error);
    showNotification('Failed to initialize some features. Please refresh the page.', 'error');
  }
});

// ===== Window Event Listeners ===== //
window.addEventListener('resize', debounce(() => {
  resizeCanvas();
}, 250));

window.addEventListener('beforeunload', () => {
  // Cleanup
  particles = [];
  if (canvas && ctx) {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
  }
});

// ===== Export Functions for Global Access ===== //
window.TechyVia = {
  scrollToSection,
  showNotification
};