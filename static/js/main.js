document.addEventListener("DOMContentLoaded", () => {
    // Add class to highlight selected radio buttons
    const pollForms = document.querySelectorAll("form");

    pollForms.forEach((form) => {
        const radios = form.querySelectorAll("input[type='radio']");
        radios.forEach((radio) => {
            radio.addEventListener("change", () => {
                radios.forEach(r => r.parentElement.classList.remove("selected"));
                if (radio.checked) {
                    radio.parentElement.classList.add("selected");
                }
            });
        });
    });

    // Fade in results after a short delay
    const results = document.querySelectorAll(".results");
    results.forEach((section) => {
        section.style.opacity = 0;
        setTimeout(() => {
            section.style.transition = "opacity 1s ease-in";
            section.style.opacity = 1;
        }, 300);
    });
});
