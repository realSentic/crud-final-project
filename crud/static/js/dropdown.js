document.addEventListener('DOMContentLoaded', () => {
        const profileBtn = document.getElementById('profile-menu-button');
        const profileMenu = document.getElementById('profile-dropdown');

        // Toggle Profile Menu
        profileBtn.addEventListener('click', (event) => {
            profileMenu.classList.toggle('hidden');
            event.stopPropagation();
        });

        // Close when clicking elsewhere
        window.addEventListener('click', () => {
            if (!profileMenu.classList.contains('hidden')) {
                profileMenu.classList.add('hidden');
            }
        });
    });