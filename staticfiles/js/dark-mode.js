(function () {
    const STORAGE_KEY = 'theme';
    const html = document.documentElement;
    const body = document.body;
    const mq = window.matchMedia('(prefers-color-scheme: dark)');

    function resolveTheme() {
        const stored = localStorage.getItem(STORAGE_KEY);
        if (stored === 'dark' || stored === 'light') return stored;
        return mq.matches ? 'dark' : 'light';
    }

    function applyTheme(theme) {
        const isDark = theme === 'dark';
        html.classList.toggle('dark-mode', isDark);
        body.classList.toggle('dark-mode', isDark);

        const btn = document.getElementById('themeToggleBtn');
        if (btn) {
            btn.querySelector('.icon-sun').style.display  = isDark ? 'none'         : 'inline';
            btn.querySelector('.icon-moon').style.display = isDark ? 'inline'       : 'none';
            btn.setAttribute('aria-label', isDark ? 'Switch to light mode' : 'Switch to dark mode');
            btn.title = isDark ? 'Switch to light mode' : 'Switch to dark mode';
        }
    }

    function setTheme(theme) {
        localStorage.setItem(STORAGE_KEY, theme);
        applyTheme(theme);
    }

    // Apply on DOM ready (body exists)
    document.addEventListener('DOMContentLoaded', function () {
        applyTheme(resolveTheme());

        const btn = document.getElementById('themeToggleBtn');
        if (btn) {
            btn.addEventListener('click', function () {
                const next = html.classList.contains('dark-mode') ? 'light' : 'dark';
                setTheme(next);
            });
        }
    });

    // React to OS-level theme changes (only when user hasn't set a manual preference)
    mq.addEventListener('change', function (e) {
        if (!localStorage.getItem(STORAGE_KEY)) {
            applyTheme(e.matches ? 'dark' : 'light');
        }
    });
})();
