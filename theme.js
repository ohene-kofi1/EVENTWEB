// EVENTWEB — Theme management (Light / Dark mode toggle)
(function () {
  const STORAGE_KEY = 'ew_theme';

  function getSavedTheme() {
    try {
      return localStorage.getItem(STORAGE_KEY);
    } catch (e) {
      return null;
    }
  }

  function getPreferredTheme() {
    const saved = getSavedTheme();
    if (saved === 'dark' || saved === 'light') return saved;
    return 'light'; // Default is always light mode
  }

  function applyTheme(theme) {
    const root = document.documentElement;
    root.setAttribute('data-theme', theme);
    if (document.body) {
      document.body.setAttribute('data-theme', theme);
    }
    updateToggleButtons(theme);
    window.dispatchEvent(new CustomEvent('theme-change', { detail: { theme: theme } }));
  }

  function updateToggleButtons(theme) {
    const buttons = document.querySelectorAll('.ew-theme-toggle, [data-action="toggle-theme"]');
    const isDark = theme === 'dark';
    buttons.forEach(btn => {
      btn.setAttribute('aria-label', isDark ? 'Switch to light mode' : 'Switch to dark mode');
      btn.setAttribute('title', isDark ? 'Switch to light mode' : 'Switch to dark mode');
      btn.setAttribute('aria-pressed', isDark ? 'true' : 'false');
      
      const sun = btn.querySelector('.ew-sun-icon');
      const moon = btn.querySelector('.ew-moon-icon');
      if (sun && moon) {
        sun.style.display = isDark ? 'block' : 'none';
        moon.style.display = isDark ? 'none' : 'block';
      }
    });
  }

  window.toggleTheme = function () {
    const current = document.documentElement.getAttribute('data-theme') || getPreferredTheme();
    const next = current === 'dark' ? 'light' : 'dark';
    try {
      localStorage.setItem(STORAGE_KEY, next);
    } catch (e) {}
    applyTheme(next);
    return next;
  };

  window.getTheme = function () {
    return document.documentElement.getAttribute('data-theme') || getPreferredTheme();
  };

  // Immediate execution before DOM render to prevent white flash
  const initial = getPreferredTheme();
  document.documentElement.setAttribute('data-theme', initial);

  // Sync on DOMContentLoaded and watch for dynamic buttons
  document.addEventListener('DOMContentLoaded', function () {
    applyTheme(getPreferredTheme());
  });

  // Global click delegate for theme toggle buttons
  document.addEventListener('click', function (e) {
    const toggleBtn = e.target.closest('.ew-theme-toggle, [data-action="toggle-theme"]');
    if (toggleBtn) {
      e.preventDefault();
      e.stopPropagation();
      window.toggleTheme();
    }
  });

  // Keep default light mode unless explicitly changed by user
  if (window.matchMedia) {
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', function (e) {
      if (getSavedTheme()) {
        applyTheme(getSavedTheme());
      }
    });
  }
})();
