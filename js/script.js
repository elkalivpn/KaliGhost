// Mobile Navigation Toggle
const mobileToggle = document.querySelector('.mobile-toggle');
const navMenu = document.querySelector('.nav-menu');

mobileToggle.addEventListener('click', () => {
    navMenu.classList.toggle('active');
});

// Close mobile menu when clicking on a link
const navLinks = document.querySelectorAll('.nav-menu ul li a');

navLinks.forEach(link => {
    link.addEventListener('click', () => {
        navMenu.classList.remove('active');
    });
});

// Header scroll effect
const header = document.querySelector('.header');

window.addEventListener('scroll', () => {
    if (window.scrollY > 100) {
        header.style.padding = '0.5rem 0';
        header.style.boxShadow = '0 2px 10px rgba(0, 0, 0, 0.1)';
    } else {
        header.style.padding = '1rem 0';
        header.style.boxShadow = '0 4px 6px rgba(0, 0, 0, 0.1)';
    }
});

// Smooth scrolling for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        e.preventDefault();
        
        const target = document.querySelector(this.getAttribute('href'));
        
        if (target) {
            window.scrollTo({
                top: target.offsetTop - 80,
                behavior: 'smooth'
            });
        }
    });
});

// Form submission
const demoForm = document.getElementById('demoForm');

if (demoForm) {
    demoForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        // Get form data
        const formData = new FormData(this);
        const data = {};
        
        for (let [key, value] of formData.entries()) {
            data[key] = value;
        }
        
        // In a real application, you would send this data to your server
        console.log('Form data submitted:', data);
        
        // Show success message
        alert('¡Gracias! Su solicitud ha sido enviada. Nos pondremos en contacto con usted pronto.');
        
        // Reset form
        this.reset();
    });
}

// Animation on scroll
const animateOnScroll = () => {
    const elements = document.querySelectorAll('.feature-card, .functionality-item, .testimonial-card, .pricing-card');
    
    elements.forEach(element => {
        const elementPosition = element.getBoundingClientRect().top;
        const screenPosition = window.innerHeight / 1.3;
        
        if (elementPosition < screenPosition) {
            element.style.opacity = 1;
            element.style.transform = 'translateY(0)';
        }
    });
};

// Set initial styles for animation
document.addEventListener('DOMContentLoaded', () => {
    const animatedElements = document.querySelectorAll('.feature-card, .functionality-item, .testimonial-card, .pricing-card');
    
    animatedElements.forEach(element => {
        element.style.opacity = 0;
        element.style.transform = 'translateY(20px)';
        element.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
    });
    
    // Run animation on scroll
    window.addEventListener('scroll', animateOnScroll);
    
    // Initial check in case elements are already in view
    animateOnScroll();
});

// Testimonial slider (if needed for mobile)
const initTestimonialSlider = () => {
    const testimonialsGrid = document.querySelector('.testimonials-grid');
    
    if (window.innerWidth <= 768 && testimonialsGrid) {
        // Add slider functionality for mobile
        let isDown = false;
        let startX;
        let scrollLeft;
        
        testimonialsGrid.addEventListener('mousedown', (e) => {
            isDown = true;
            startX = e.pageX - testimonialsGrid.offsetLeft;
            scrollLeft = testimonialsGrid.scrollLeft;
        });
        
        testimonialsGrid.addEventListener('mouseleave', () => {
            isDown = false;
        });
        
        testimonialsGrid.addEventListener('mouseup', () => {
            isDown = false;
        });
        
        testimonialsGrid.addEventListener('mousemove', (e) => {
            if (!isDown) return;
            e.preventDefault();
            const x = e.pageX - testimonialsGrid.offsetLeft;
            const walk = (x - startX) * 2;
            testimonialsGrid.scrollLeft = scrollLeft - walk;
        });
    }
};

// Initialize slider
window.addEventListener('resize', initTestimonialSlider);
document.addEventListener('DOMContentLoaded', initTestimonialSlider);