document.addEventListener('DOMContentLoaded', function() {
    const themeToggle = document.getElementById('theme-toggle');
    const body = document.body;
    const currentTheme = localStorage.getItem('theme') || 'light'; // default to light mode


    function setTheme(theme) {
        if (theme === 'dark') {
            body.classList.add('dark-mode');
            themeToggle.checked = true;
        } else {
            body.classList.remove('dark-mode');
           themeToggle.checked = false;
        }
        localStorage.setItem('theme', theme);
    }
     setTheme(currentTheme)
    themeToggle.addEventListener('change', function() {
        if (this.checked) {
            setTheme('dark');
        } else {
            setTheme('light');
        }
    });
});