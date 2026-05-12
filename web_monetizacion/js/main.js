// Simple JavaScript for KaliGhost Monetization Site

document.addEventListener('DOMContentLoaded', function() {
    // Service selection function
    window.selectService = function(serviceType) {
        // In a real implementation, this would open a modal or redirect to a quote form
        alert('Has seleccionado el servicio: ' + serviceType + '\n\nEn una implementación real, esto abriría un formulario para obtener un cotización personalizada.\n\nPor ahora, gracias por tu interés en nuestros servicios de pentesting autónomo.');
        
        // Log to console for debugging
        console.log('Service selected:', serviceType);
    };
    
    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });
    
    // Add some cyberpunk effect to headers on scroll
    let lastScrollTop = 0;
    const header = document.querySelector('.header');
    
    window.addEventListener('scroll', function() {
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        
        if (scrollTop > lastScrollTop) {
            // Scrolling down
            header.style.transform = 'translateY(-100%)';
        } else {
            // Scrolling up
            header.style.transform = 'translateY(0)';
        }
        
        lastScrollTop = scrollTop;
    }, false);
    
    // Add typing effect to header (optional)
    const headerText = document.querySelector('.header h1');
    if (headerText) {
        const originalText = headerText.textContent;
        let i = 0;
        const speed = 100; // typing speed in milliseconds
        
        function typeWriter() {
            if (i < originalText.length) {
                headerText.textContent += originalText.charAt(i);
                i++;
                setTimeout(typeWriter, speed);
            }
        }
        
        // Uncomment to enable typing effect
        // headerText.textContent = '';
        // setTimeout(typeWriter, 500);
    }
});

// Export for potential use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { selectService };
}