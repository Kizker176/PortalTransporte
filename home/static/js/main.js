
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

document.addEventListener("DOMContentLoaded", () => {
    const contenedor = document.querySelector("[data-modal-campanas]");

    if (!contenedor) return;

    const avisos = Array.from(
        contenedor.querySelectorAll("[data-campana-id]")
    );

    const botonCerrar = contenedor.querySelector("[data-cerrar-campanas]");
    const botonAnterior = contenedor.querySelector("[data-campana-anterior]");
    const botonSiguiente = contenedor.querySelector("[data-campana-siguiente]");
    const contador = contenedor.querySelector("[data-campana-contador]");

    const CLAVE = "portaltransporte_campanas_vistas";
    const INTERVALO = 6000;

    function obtenerVistas() {
        try {
            return JSON.parse(localStorage.getItem(CLAVE) || "[]");
        } catch {
            return [];
        }
    }

    function registrarVista(id) {
        try {
            const vistas = obtenerVistas();

            if (!vistas.includes(id)) {
                vistas.push(id);
                localStorage.setItem(CLAVE, JSON.stringify(vistas));
            }
        } catch {
            // El navegador puede bloquear el almacenamiento local.
        }
    }

    const vistas = obtenerVistas();

    // Solo se muestran las campañas que el visitante aún no ha visto.
    /* const pendientes = avisos.filter(
        aviso => !vistas.includes(aviso.dataset.campanaId)
    ); */
    const pendientes = avisos;
    
    if (pendientes.length === 0) return;

    let actual = 0;
    let temporizador = null;

    function mostrarAviso(indice) {
        actual = (indice + pendientes.length) % pendientes.length;

        pendientes.forEach((aviso, i) => {
            aviso.hidden = i !== actual;
        });

        const id = pendientes[actual].dataset.campanaId;
        /* registrarVista(id); */

        if (contador) {
            contador.textContent =
                `${actual + 1} de ${pendientes.length}`;
        }

        const hayVarios = pendientes.length > 1;

        if (botonAnterior) botonAnterior.hidden = !hayVarios;
        if (botonSiguiente) botonSiguiente.hidden = !hayVarios;
        if (contador) contador.hidden = !hayVarios;
    }

    function detenerRotacion() {
        if (temporizador) {
            clearInterval(temporizador);
            temporizador = null;
        }
    }

    function iniciarRotacion() {
        detenerRotacion();

        if (pendientes.length > 1) {
            temporizador = setInterval(() => {
                mostrarAviso(actual + 1);
            }, INTERVALO);
        }
    }

    function cerrarModal() {
        detenerRotacion();
        contenedor.hidden = true;
    }

    botonCerrar?.addEventListener("click", cerrarModal);

    botonSiguiente?.addEventListener("click", () => {
        mostrarAviso(actual + 1);
        iniciarRotacion();
    });

    botonAnterior?.addEventListener("click", () => {
        mostrarAviso(actual - 1);
        iniciarRotacion();
    });

    contenedor.addEventListener("click", event => {
        if (event.target === contenedor) {
            cerrarModal();
        }
    });

    document.addEventListener("keydown", event => {
        if (contenedor.hidden) return;

        if (event.key === "Escape") {
            cerrarModal();
        }
    });

    mostrarAviso(0);
    contenedor.hidden = false;
    iniciarRotacion();
});
