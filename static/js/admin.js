document.addEventListener("DOMContentLoaded", () => {
    const sidebar = document.getElementById("adminSidebar");
    const overlay = document.getElementById("sidebarOverlay");
    const menuButton = document.getElementById("mobileMenuButton");

    const closeSidebar = () => {
        sidebar?.classList.remove("open");
        overlay?.classList.remove("open");
    };

    menuButton?.addEventListener("click", () => {
        sidebar?.classList.toggle("open");
        overlay?.classList.toggle("open");
    });

    overlay?.addEventListener("click", closeSidebar);

    document.querySelectorAll(".modal-backdrop").forEach((modal) => {
        modal.addEventListener("click", (event) => {
            if (event.target === modal) {
                modal.classList.remove("open");
            }
        });
    });

    document.querySelectorAll("[data-modal-open]").forEach((button) => {
        button.addEventListener("click", () => {
            const modalId = button.dataset.modalOpen;
            document.getElementById(modalId)?.classList.add("open");
        });
    });

    document.querySelectorAll("[data-modal-close]").forEach((button) => {
        button.addEventListener("click", () => {
            const modalId = button.dataset.modalClose;
            document.getElementById(modalId)?.classList.remove("open");
        });
    });

    document.addEventListener("keydown", (event) => {
        if (event.key === "Escape") {
            document.querySelectorAll(".modal-backdrop.open").forEach((modal) => {
                modal.classList.remove("open");
            });
            closeSidebar();
        }

        if ((event.ctrlKey || event.metaKey) && event.key.toLowerCase() === "k") {
            event.preventDefault();
            const search = document.querySelector(".topbar-search input");
            search?.focus();
        }
    });

    document.querySelectorAll("[data-delete-item]").forEach((button) => {
        button.addEventListener("click", () => {
            const item = button.dataset.deleteItem || "this item";
            const confirmed = window.confirm(`Are you sure you want to delete ${item}?`);
            if (confirmed) {
                // UI-only milestone: backend delete action will be wired later.
                button.closest("tr")?.remove();
            }
        });
    });
});
