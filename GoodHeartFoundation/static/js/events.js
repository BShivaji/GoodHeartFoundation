document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll("[data-event-card]").forEach((card, index) => {
        card.style.animationDelay = `${index * 0.08}s`;
    });
});
