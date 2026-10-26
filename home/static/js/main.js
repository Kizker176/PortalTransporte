
document.addEventListener("DOMContentLoaded", () => {
    const menuToggle = document.getElementById("menuToggle");
    const menuPrincipal = document.getElementById("menuPrincipal");

    if (!menuToggle || !menuPrincipal) {
        return;
    }

    menuToggle.addEventListener("click", () => {
        const abierto = menuPrincipal.classList.toggle("menu-abierto");

        menuToggle.setAttribute(
            "aria-expanded",
            String(abierto)
        );
    });

    menuPrincipal.querySelectorAll("a").forEach((enlace) => {
        enlace.addEventListener("click", () => {
            menuPrincipal.classList.remove("menu-abierto");
            menuToggle.setAttribute("aria-expanded", "false");
        });
    });
});


document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll(".hero-carousel").forEach((carousel) => {
        const slides = [...carousel.querySelectorAll(".carousel-slide")];
        const indicators = [
            ...carousel.querySelectorAll(".carousel-indicator")
        ];

        const previous = carousel.querySelector(".carousel-control.prev");
        const next = carousel.querySelector(".carousel-control.next");

        if (slides.length <= 1) {
            previous.hidden = true;
            next.hidden = true;
            carousel.querySelector(".carousel-indicators").hidden = true;
            return;
        }

        let current = 0;
        let timer;

        function showSlide(index) {
            current = (index + slides.length) % slides.length;

            slides.forEach((slide, i) => {
                const active = i === current;
                slide.classList.toggle("active", active);
                slide.setAttribute("aria-hidden", String(!active));
            });

            indicators.forEach((indicator, i) => {
                const active = i === current;
                indicator.classList.toggle("active", active);

                if (active) {
                    indicator.setAttribute("aria-current", "true");
                } else {
                    indicator.removeAttribute("aria-current");
                }
            });
        }

        function startAutoplay() {
            stopAutoplay();
            timer = setInterval(() => showSlide(current + 1), 5000);
        }

        function stopAutoplay() {
            clearInterval(timer);
        }

        previous.addEventListener("click", () => {
            showSlide(current - 1);
            startAutoplay();
        });

        next.addEventListener("click", () => {
            showSlide(current + 1);
            startAutoplay();
        });

        indicators.forEach((indicator, i) => {
            indicator.addEventListener("click", () => {
                showSlide(i);
                startAutoplay();
            });
        });

        carousel.addEventListener("mouseenter", stopAutoplay);
        carousel.addEventListener("mouseleave", startAutoplay);

        carousel.addEventListener("focusin", stopAutoplay);
        carousel.addEventListener("focusout", startAutoplay);

        showSlide(0);
        startAutoplay();
    });
});
