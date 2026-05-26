document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector("#volunteer-form");
    if (!form) {
        return;
    }

    form.addEventListener("submit", () => {
        const button = form.querySelector("button[type='submit']");
        if (button) {
            button.textContent = "Submitting...";
        }
    });
});
