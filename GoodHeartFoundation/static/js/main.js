document.addEventListener("DOMContentLoaded", () => {
    document.body.classList.add("app-ready");

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
});
