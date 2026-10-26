
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
