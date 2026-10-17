// Minimal client-side enhancements for Task Manager
document.addEventListener("DOMContentLoaded", () => {
    // 1. Auto-focus task input field
    const taskInput = document.getElementById("task-title-input");
    if (taskInput) {
        taskInput.focus();
    }

    // 2. Auto-dismiss flash notifications after 5 seconds
    const flashMessages = document.querySelectorAll(".flash-alert");
    flashMessages.forEach((alert) => {
        setTimeout(() => {
            alert.style.transition = "opacity 0.4s ease, transform 0.4s ease";
            alert.style.opacity = "0";
            alert.style.transform = "translateY(-6px)";
            setTimeout(() => {
                alert.remove();
            }, 400);
        }, 5000);
    });

    // 3. Client-side trim validation to prevent sending whitespace-only tasks
    const form = document.getElementById("add-task-form");
    if (form && taskInput) {
        form.addEventListener("submit", (e) => {
            const trimmed = taskInput.value.trim();
            if (!trimmed) {
                // If completely empty on client side, let server handle it or highlight input
                taskInput.value = "";
                taskInput.focus();
            }
        });
    }
});
