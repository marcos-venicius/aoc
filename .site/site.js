// BLACKSITE — progressive enhancement only; every page works without JS.
(() => {
  // Language tabs on day pages
  const tabs = [...document.querySelectorAll('[role="tab"]')];
  const select = (tab, focus) => {
    tabs.forEach(t => {
      const on = t === tab;
      t.setAttribute('aria-selected', on);
      t.tabIndex = on ? 0 : -1;
      document.getElementById(t.getAttribute('aria-controls')).hidden = !on;
    });
    if (focus) tab.focus();
    history.replaceState(null, '', '#' + tab.id.slice(4));
  };
  tabs.forEach((t, i) => {
    t.tabIndex = t.getAttribute('aria-selected') === 'true' ? 0 : -1;
    t.addEventListener('click', () => select(t));
    t.addEventListener('keydown', e => {
      if (e.key === 'ArrowRight' || e.key === 'ArrowLeft') {
        e.preventDefault(); e.stopPropagation();
        select(tabs[(i + (e.key === 'ArrowRight' ? 1 : -1) + tabs.length) % tabs.length], true);
      }
    });
  });
  // Deep link: #go, #python, or #go-0-L12 opens the right tab
  const hash = decodeURIComponent(location.hash.slice(1));
  if (hash && tabs.length) {
    const lang = hash.split('-')[0];
    const tab = document.getElementById('tab-' + lang);
    if (tab) {
      tabs.forEach(t => {
        const on = t === tab;
        t.setAttribute('aria-selected', on);
        t.tabIndex = on ? 0 : -1;
        document.getElementById(t.getAttribute('aria-controls')).hidden = !on;
      });
      const el = document.getElementById(hash);
      if (el) el.scrollIntoView();
    }
  }

  // Copy buttons
  document.querySelectorAll('.copy').forEach(btn => {
    btn.addEventListener('click', async () => {
      const src = document.getElementById(btn.dataset.target).value;
      try {
        await navigator.clipboard.writeText(src);
        btn.textContent = '[copied]';
      } catch {
        btn.textContent = '[denied]';
      }
      setTimeout(() => (btn.textContent = '[copy]'), 1400);
    });
  });

  // Keyboard navigation: h/← prev, l/→ next, u up
  document.addEventListener('keydown', e => {
    if (e.metaKey || e.ctrlKey || e.altKey || /input|textarea|select/i.test(e.target.tagName)) return;
    if (e.target.getAttribute && e.target.getAttribute('role') === 'tab') return;
    const go = sel => { const a = document.querySelector(sel); if (a) location.href = a.href; };
    if (e.key === 'h' || e.key === 'ArrowLeft') go('a[rel="prev"]');
    else if (e.key === 'l' || e.key === 'ArrowRight') go('a[rel="next"]');
    else if (e.key === 'u') go('.crumbs a');
  });

  // Language filter on the index
  const chips = [...document.querySelectorAll('.chip')];
  chips.forEach(chip => chip.addEventListener('click', () => {
    chips.forEach(c => c.classList.toggle('active', c === chip));
    const lang = chip.dataset.lang;
    document.querySelectorAll('.cell.on').forEach(cell => {
      cell.classList.toggle('dim-out', !!lang && !cell.getAttribute('aria-label').includes(lang));
    });
  }));
})();
