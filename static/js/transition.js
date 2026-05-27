// Lightweight page transition with floating bubbles
(function(){
  const makeOverlay = () => {
    const overlay = document.createElement('div');
    overlay.className = 'page-transition-overlay';
    // create a few bubbles with random sizes/colors
    const colors = ['rgba(143,75,31,0.12)','rgba(62,124,71,0.12)','rgba(140,200,220,0.12)','rgba(200,120,80,0.12)'];
    const count = 10;
    for (let i=0;i<count;i++){
      const b = document.createElement('div');
      b.className = 'pt-bubble';
      const size = 18 + Math.round(Math.random()*60);
      b.style.width = size+'px';
      b.style.height = size+'px';
      b.style.left = Math.round(Math.random()*100)+'%';
      b.style.background = colors[i % colors.length];
      const delay = Math.round(Math.random()*220);
      const duration = 700 + Math.round(Math.random()*500);
      b.style.animation = `pt-float-up ${duration}ms cubic-bezier(.22,.9,.27,1) ${delay}ms both`;
      overlay.appendChild(b);
    }
    return overlay;
  };

  const isLocal = (anchor) => {
    if (!anchor.href) return false;
    if (anchor.target && anchor.target === '_blank') return false;
    if (anchor.hasAttribute('download')) return false;
    const url = new URL(anchor.href, location.href);
    return url.origin === location.origin;
  };

  document.addEventListener('DOMContentLoaded', () => {
    // mark ready after small delay so CSS entrance runs
    document.body.setAttribute('data-page-ready','false');
    requestAnimationFrame(()=>{
      setTimeout(()=> document.body.setAttribute('data-page-ready','true'), 30);
    });

    document.addEventListener('click', (ev) => {
      const a = ev.target.closest && ev.target.closest('a');
      if (!a) return;
      if (ev.defaultPrevented) return;
      if (ev.metaKey || ev.ctrlKey || ev.shiftKey || ev.altKey) return; // allow new tab/window/open
      if (!isLocal(a)) return;
      // ignore anchor-only links
      const href = a.getAttribute('href') || a.href;
      if (!href || href.startsWith('#')) return;

      ev.preventDefault();

      // create overlay and animate
      const overlay = makeOverlay();
      document.body.appendChild(overlay);
      // fade body slightly
      document.body.classList.add('page-fade-out');

      // ensure animations run then navigate
      const wait = 700; // ms, should cover bubble durations
      setTimeout(()=>{
          // Float-in animation for common page components using IntersectionObserver
          (function(){
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

            elems.forEach(el=> el.classList.add('float-off'));

            const io = new IntersectionObserver((entries, obs)=>{
              entries.forEach(entry=>{
                if (!entry.isIntersecting) return;
                const el = entry.target;
                // compute small stagger based on visible index
                const idx = elems.indexOf(el);
                const delay = Math.min(500, (idx % 10) * 60);
                el.style.transitionDelay = delay + 'ms';
                el.setAttribute('data-stagger', delay);
                el.classList.add('float-in');
                el.classList.remove('float-off');
                obs.unobserve(el);
              });
            }, { threshold: 0.08 });

            elems.forEach(el=> io.observe(el));
          })();
        // when navigating, keep overlay briefly so transition is visible
        window.location.href = a.href;
      }, wait);
    }, true);
  });
})();
