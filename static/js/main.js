document.addEventListener("DOMContentLoaded", () => {
    document.body.classList.add("app-ready");

    // --- Dynamic Navbar ---
    const navbar = document.querySelector('.premium-nav');
    if (navbar) {
        window.addEventListener('scroll', () => {
            if (window.scrollY > 20) {
                navbar.classList.add('nav-scrolled');
            } else {
                navbar.classList.remove('nav-scrolled');
            }
        }, { passive: true });
    }

    const carousel = document.querySelector("[data-achievements-carousel]");
    const track = document.querySelector("[data-achievement-track]");
    const slides = document.querySelectorAll("[data-achievement-slide]");
    const nextButton = document.querySelector("[data-achievement-next]");
    const prevButton = document.querySelector("[data-achievement-prev]");

    if (!carousel || !track || slides.length === 0) {
        return;
    }

    let currentIndex = 0;

    const renderSlide = () => {
        track.style.transform = `translateX(-${currentIndex * 100}%)`;
    };

    const showNext = () => {
        currentIndex = (currentIndex + 1) % slides.length;
        renderSlide();
    };

    const showPrev = () => {
        currentIndex = (currentIndex - 1 + slides.length) % slides.length;
        renderSlide();
    };

    if (nextButton) {
        nextButton.addEventListener("click", showNext);
    }

    if (prevButton) {
        prevButton.addEventListener("click", showPrev);
    }

    if (slides.length > 1) {
        setInterval(showNext, 4500);
    }

    const recentWorksCarousel = document.querySelector("[data-recent-works-carousel]");
    const recentWorksTrack = document.querySelector("[data-recent-work-track]");
    const recentWorksSlides = document.querySelectorAll("[data-recent-work-slide]");
    const recentWorksNext = document.querySelector("[data-recent-work-next]");
    const recentWorksPrev = document.querySelector("[data-recent-work-prev]");

    if (recentWorksCarousel && recentWorksTrack && recentWorksSlides.length) {
        let recentWorkIndex = 0;

        const renderRecentWork = () => {
            recentWorksTrack.style.transform = `translateX(-${recentWorkIndex * 100}%)`;
        };

        const showRecentNext = () => {
            recentWorkIndex = (recentWorkIndex + 1) % recentWorksSlides.length;
            renderRecentWork();
        };

        const showRecentPrev = () => {
            recentWorkIndex = (recentWorkIndex - 1 + recentWorksSlides.length) % recentWorksSlides.length;
            renderRecentWork();
        };

        if (recentWorksNext) {
            recentWorksNext.addEventListener("click", showRecentNext);
        }

        if (recentWorksPrev) {
            recentWorksPrev.addEventListener("click", showRecentPrev);
        }

        if (recentWorksSlides.length > 1) {
            setInterval(showRecentNext, 5000);
        }
    }

    // --- Stats Counter Animation ---
    const counters = document.querySelectorAll('.counter-number');
    if (counters.length > 0) {
        const animateCounters = (entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const counter = entry.target;
                    const target = +counter.getAttribute('data-target');
                    const prefix = counter.getAttribute('data-prefix') || '';
                    const duration = 2500; // slightly longer, 2.5 seconds
                    const frameDuration = 1000 / 60; // ~60fps
                    const totalFrames = Math.round(duration / frameDuration);
                    let frame = 0;
                    
                    const updateCount = () => {
                        frame++;
                        const progress = Math.min(frame / totalFrames, 1);
                        // Ease Out Expo - very fast start, slow elegant finish
                        const easeOut = progress === 1 ? 1 : 1 - Math.pow(2, -10 * progress);
                        const current = Math.round(target * easeOut);
                        
                        // Format with commas using Indian numbering system
                        const formattedNumber = current.toLocaleString('en-IN');
                        counter.innerText = prefix + formattedNumber;
                        
                        if (frame < totalFrames) {
                            requestAnimationFrame(updateCount);
                        } else {
                            // Ensure final target is exact and formatted
                            counter.innerText = prefix + target.toLocaleString('en-IN');
                        }
                    };
                    
                    updateCount();
                    observer.unobserve(counter); // Only animate once
                }
            });
        };

        const observer = new IntersectionObserver(animateCounters, { threshold: 0.5 });
        counters.forEach(counter => {
            observer.observe(counter);
        });
    }
});
