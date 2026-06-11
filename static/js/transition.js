// Professional page transition — slim progress bar (GitHub / Linear style)
(function () {
    'use strict';

    // ── Progress bar element ────────────────────────────────────────
    let bar = null;
    let fillTimer = null;
    let hideTimer = null;
    let currentWidth = 0;

    function createBar() {
        bar = document.createElement('div');
        bar.className = 'page-progress-bar';
        document.body.appendChild(bar);
    }

    function setWidth(w) {
        currentWidth = w;
        if (bar) bar.style.width = w + '%';
    }

    function startProgress() {
        clearTimeout(fillTimer);
        clearTimeout(hideTimer);
        if (!bar) createBar();
        bar.style.opacity = '1';
        setWidth(0);

        // Quick jump to 30 %, then crawl to 85 %
        setTimeout(() => setWidth(30), 30);
        setTimeout(() => setWidth(60), 200);

        fillTimer = setTimeout(function crawl() {
            if (currentWidth < 85) {
                setWidth(currentWidth + 0.6);
                fillTimer = setTimeout(crawl, 80);
            }
        }, 400);
    }

    function finishProgress() {
        clearTimeout(fillTimer);
        setWidth(100);
        hideTimer = setTimeout(() => {
            if (bar) bar.style.opacity = '0';
            setTimeout(() => {
                if (bar) { bar.style.width = '0%'; }
            }, 250);
        }, 280);
    }

    // ── Helpers ─────────────────────────────────────────────────────
    function isLocal(anchor) {
        if (!anchor.href) return false;
        if (anchor.target && anchor.target === '_blank') return false;
        if (anchor.hasAttribute('download')) return false;
        try {
            const url = new URL(anchor.href, location.href);
            return url.origin === location.origin;
        } catch (_) {
            return false;
        }
    }

    function runScrollInAnimations() {
        if (window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

        const selectors = [
            '.card',
            '.dashboard-panel',
            '.insight-bars__item',
            '.recent-work-admin-item',
            '.growth-chart__group',
            '.dashboard-pie__legend-item',
            '.admin-modal__dialog',
            '.volunteer-toolbar__button',
            '.event-card',
            '.recent-work-admin-item__content'
        ];

        const elems = Array.from(document.querySelectorAll(selectors.join(',')));
        if (!elems.length) return;

        elems.forEach(el => el.classList.add('float-off'));

        const io = new IntersectionObserver((entries, obs) => {
            entries.forEach(entry => {
                if (!entry.isIntersecting) return;
                const el = entry.target;
                const idx = elems.indexOf(el);
                el.style.transitionDelay = Math.min(400, (idx % 8) * 55) + 'ms';
                el.classList.add('float-in');
                el.classList.remove('float-off');
                obs.unobserve(el);
            });
        }, { threshold: 0.07 });

        elems.forEach(el => io.observe(el));
    }

    // ── Boot ─────────────────────────────────────────────────────────
    document.addEventListener('DOMContentLoaded', () => {
        // Page entrance fade-in
        document.body.setAttribute('data-page-ready', 'false');
        createBar();

        requestAnimationFrame(() => {
            setTimeout(() => {
                document.body.setAttribute('data-page-ready', 'true');
                runScrollInAnimations();
            }, 30);
        });

        // Intercept local link clicks
        document.addEventListener('click', (ev) => {
            const a = ev.target.closest && ev.target.closest('a');
            if (!a) return;
            if (ev.defaultPrevented) return;
            if (ev.metaKey || ev.ctrlKey || ev.shiftKey || ev.altKey) return;
            if (!isLocal(a)) return;

            const href = a.getAttribute('href') || a.href;
            if (!href || href.startsWith('#')) return;

            ev.preventDefault();
            startProgress();

            // Fade body out
            document.body.classList.add('page-fade-out');

            setTimeout(() => {
                window.location.href = a.href;
            }, 200);
        }, true);

        // When navigating back (bfcache restore) finish bar immediately
        window.addEventListener('pageshow', (ev) => {
            if (ev.persisted) {
                document.body.classList.remove('page-fade-out');
                finishProgress();
                document.body.setAttribute('data-page-ready', 'true');
            }
        });
    });

    // Finish bar as soon as page fully loads (covers form submits etc.)
    window.addEventListener('load', finishProgress);
})();
