document.addEventListener('DOMContentLoaded', function () {
    const closeIcon = document.getElementById('closeIcon');
    const messageBanner = document.getElementById('messageBanner');
    if (closeIcon && messageBanner) { // Check if elements are found
        closeIcon.addEventListener('click', function () {
            messageBanner.style.display = 'none';
        });
    }
});
