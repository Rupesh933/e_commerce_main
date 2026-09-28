(function () {
        function showNotification(icon, message) {
            var toast = document.getElementById('quickToast');
            if (!toast) return;
            document.getElementById('quickToastIcon').textContent = icon;
            document.getElementById('quickToastMsg').textContent = message;
            toast.style.display = 'flex';
            setTimeout(function () { toast.style.opacity = '1'; toast.style.transform = 'translateY(0)'; }, 10);
            clearTimeout(window.__toastTimeout);
            window.__toastTimeout = setTimeout(function () {
                toast.style.opacity = '0'; toast.style.transform = 'translateY(10px)';
                setTimeout(function () { toast.style.display = 'none'; }, 300);
            }, 2200);
        }

        function setLanguage(lang, name, flag, notify) {
            document.getElementById('selectedLangFlag').textContent = flag || '🌐';
            document.getElementById('selectedLangName').textContent = name || 'English';
            document.querySelectorAll('.lang-option').forEach(function (el) {
                var isMatch = el.getAttribute('data-lang') === lang;
                el.classList.toggle('active', isMatch);
                var check = el.querySelector('.check-icon');
                if (check) check.classList.toggle('d-none', !isMatch);
            });
            localStorage.setItem('ecomart_lang', JSON.stringify({ lang: lang, name: name, flag: flag }));
            if (notify) showNotification(flag || '🌐', 'Language set to ' + name);
        }

        function setCurrency(code, symbol, flag, country, rate, notify) {
            document.getElementById('selectedCurrencyFlag').textContent = flag || '🇺🇸';
            document.getElementById('selectedCurrencyCode').textContent = code || 'USD';
            document.getElementById('selectedCurrencySymbol').textContent = '(' + (symbol || '$') + ')';
            document.querySelectorAll('.currency-option').forEach(function (el) {
                var isMatch = el.getAttribute('data-code') === code;
                el.classList.toggle('active', isMatch);
                var check = el.querySelector('.check-icon');
                if (check) check.classList.toggle('d-none', !isMatch);
            });
            localStorage.setItem('ecomart_currency', JSON.stringify({ code: code, symbol: symbol, flag: flag, country: country, rate: rate }));
            if (notify) showNotification(flag || '💵', 'Currency set to ' + code + ' (' + symbol + ')');
        }

        document.addEventListener('DOMContentLoaded', function () {
            try {
                var savedLang = JSON.parse(localStorage.getItem('ecomart_lang'));
                if (savedLang && savedLang.lang) setLanguage(savedLang.lang, savedLang.name, savedLang.flag, false);
            } catch (e) {}
            try {
                var savedCurr = JSON.parse(localStorage.getItem('ecomart_currency'));
                if (savedCurr && savedCurr.code) setCurrency(savedCurr.code, savedCurr.symbol, savedCurr.flag, savedCurr.country, savedCurr.rate, false);
            } catch (e) {}

            document.querySelectorAll('.lang-option').forEach(function (item) {
                item.addEventListener('click', function (e) {
                    e.preventDefault();
                    setLanguage(this.getAttribute('data-lang'), this.getAttribute('data-name'), this.getAttribute('data-flag'), true);
                });
            });
            document.querySelectorAll('.currency-option').forEach(function (item) {
                item.addEventListener('click', function (e) {
                    e.preventDefault();
                    setCurrency(this.getAttribute('data-code'), this.getAttribute('data-symbol'), this.getAttribute('data-flag'), this.getAttribute('data-country'), this.getAttribute('data-rate'), true);
                });
            });

            document.querySelectorAll('.eco-dropdown__trigger, .eco-rail__all').forEach(function (btn) {
                btn.addEventListener('click', function (e) {
                    e.stopPropagation();
                    var parent = this.closest('.eco-dropdown');
                    var isOpen = parent.classList.contains('show');
                    document.querySelectorAll('.eco-dropdown.show').forEach(function (d) { d.classList.remove('show'); });
                    if (!isOpen) parent.classList.add('show');
                });
            });
            document.addEventListener('click', function () {
                document.querySelectorAll('.eco-dropdown.show').forEach(function (d) { d.classList.remove('show'); });
            });

            var navToggle = document.querySelector('.eco-navtoggle');
            var rail = document.getElementById('ecoNavRail');
            if (navToggle && rail) navToggle.addEventListener('click', function () { rail.classList.toggle('show'); });
        });
    })();

document.addEventListener("click", function (event) {
        var menu = document.getElementById("ecoUserMenu");
        if (menu && !menu.contains(event.target)) {
            menu.removeAttribute("open");
        }
    });