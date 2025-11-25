document.addEventListener("DOMContentLoaded", function() {
    
    /* =========================================
       SELECTOR DE IDIOMAS (Dropdown)
       ========================================= */
    const langBtn = document.getElementById("lang-btn");
    const langMenu = document.getElementById("lang-menu");
    const langForm = document.getElementById("lang-form");
    const langInput = document.getElementById("lang-input");
    const langOptions = document.querySelectorAll(".lang-menu li");

    // Verificamos que los elementos existan para evitar errores en páginas donde no estén
    if (langBtn && langMenu && langForm && langInput) {

        // 1. Abrir/Cerrar menú al hacer clic
        langBtn.addEventListener("click", function(e) {
            e.stopPropagation(); // Evita que el clic cierre el menú inmediatamente
            langMenu.classList.toggle("show");
        });

        // 2. Cerrar el menú si haces clic fuera
        document.addEventListener("click", function(e) {
            if (!langBtn.contains(e.target) && !langMenu.contains(e.target)) {
                langMenu.classList.remove("show");
            }
        });

        // 3. Al elegir un idioma, enviar el formulario
        langOptions.forEach(option => {
            option.addEventListener("click", function() {
                const selectedLang = this.getAttribute("data-lang");
                langInput.value = selectedLang;
                langForm.submit(); // Django recibe esto y cambia el idioma
            });
        });
    }

    /* =========================================
       MODO OSCURO
       ========================================= */
    const darkModeToggle = document.getElementById("darkModeToggle");
    
    // Cargar preferencia guardada
    if (localStorage.getItem("dark-mode") === "enabled") {
        document.body.classList.add("dark-mode");
        // Aplicar a otros elementos si es necesario
        const headers = document.querySelectorAll("header, nav, footer");
        headers.forEach(el => el.classList.add("dark-mode"));
    }

    if (darkModeToggle) {
        darkModeToggle.addEventListener("click", () => {
            const isEnabled = document.body.classList.toggle("dark-mode");
            
            // Toggle en header, nav y footer
            const headers = document.querySelectorAll("header, nav, footer");
            headers.forEach(el => el.classList.toggle("dark-mode"));

            if (isEnabled) {
                localStorage.setItem("dark-mode", "enabled");
            } else {
                localStorage.setItem("dark-mode", "disabled");
            }
        });
    }
});