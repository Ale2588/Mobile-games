/* Small Hours · comportamento del sito. Nessuna libreria. */
(function () {
  const SH = window.SH || {};
  const $ = (s) => document.querySelector(s);
  const $$ = (s) => Array.from(document.querySelectorAll(s));
  const fmt = (s, o) => s.replace(/\{(\w+)\}/g, (_, k) => (o[k] ?? ''));
  const store = {
    get(k) { try { return JSON.parse(localStorage.getItem(k)); } catch (e) { return null; } },
    set(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) {} },
  };

  /* lingua ricordata */
  $$('[data-setlang]').forEach((a) => a.addEventListener('click', () => {
    const p = store.get('sh:v1:profile') || {}; p.lang = a.dataset.setlang; store.set('sh:v1:profile', p);
  }));

  /* fogli dal basso */
  let lastFocus = null;
  const openSheet = (n) => { lastFocus = document.activeElement; $$(`[data-sheet="${n}"]`).forEach((x) => (x.hidden = false)); const f = $(`.sheet[data-sheet="${n}"] button, .sheet[data-sheet="${n}"] textarea`); if (f) f.focus(); };
  const closeSheet = (n) => { $$(`[data-sheet="${n}"]`).forEach((x) => (x.hidden = true)); if (lastFocus) lastFocus.focus(); };
  $$('.sheet-backdrop[data-sheet]').forEach((b) => b.addEventListener('click', () => closeSheet(b.dataset.sheet)));
  $$('.sheet[data-sheet]').forEach((s) => s.querySelectorAll('[data-close]').forEach((b) => b.addEventListener('click', () => closeSheet(s.dataset.sheet))));
  document.addEventListener('keydown', (ev) => { if (ev.key === 'Escape') $$('.sheet[data-sheet]:not([hidden])').forEach((s) => closeSheet(s.dataset.sheet)); });

  /* parere */
  $$('[data-feedback]').forEach((b) => b.addEventListener('click', () => openSheet('fb')));
  const send = $('#fbSend');
  if (send) send.addEventListener('click', () => {
    const txt = ($('#fbText').value || '').trim();
    if (!txt) { $('#fbText').focus(); return; }
    const meta = `\n\n— ${location.pathname} · ${navigator.userAgent}`;
    if (SH.email) {
      location.href = `mailto:${SH.email}?subject=${encodeURIComponent('Small Hours · parere')}&body=${encodeURIComponent(txt + meta)}`;
    } else {
      const done = () => { $('#fbMsg').textContent = SH.t['fb.copied']; };
      if (navigator.clipboard) navigator.clipboard.writeText(txt).then(done, done); else done();
    }
  });

  /* giorno e sfida */
  const locale = SH.lang === 'it' ? 'it-IT' : 'en-GB';
  const now = new Date();
  const launch = new Date(SH.launch + 'T00:00:00');
  const dayN = Math.max(1, Math.floor((now - launch) / 864e5) + 1);
  const games = SH.games || [];
  const featured = games.length ? games[(dayN - 1) % games.length] : null;
  const today = new Intl.DateTimeFormat(locale, { weekday: 'long', day: 'numeric', month: 'long' }).format(now);
  $$('[data-today]').forEach((el) => (el.textContent = today));
  if (featured) {
    const a = $('[data-featured]'); if (a) a.href = SH.root + featured.play;
    const tx = $('[data-featured-text]'); if (tx) tx.textContent = fmt(SH.t['home.today'], { game: featured.title, min: featured.minutes[1] });
  }
  const dn = $('[data-daily-n]'); if (dn) dn.textContent = fmt(SH.t['daily.eyebrow'], { n: dayN }) + ' · ' + today;
  const cd = $('[data-countdown]');
  if (cd) {
    const tick = () => {
      const d = new Date(); const m = new Date(d); m.setHours(24, 0, 0, 0);
      const s = Math.max(0, (m - d) / 1000); const h = Math.floor(s / 3600); const mi = Math.floor((s % 3600) / 60);
      cd.textContent = fmt(SH.t['daily.body'], { t: `${h} h ${mi} min` });
    };
    tick(); setInterval(tick, 30000);
  }

  /* progressi letti dai giochi */
  function progressOf(slug) {
    if (slug === 'ultima-corsa') {
      let s = null; try { s = JSON.parse(localStorage.getItem('uc-season') || 'null'); } catch (e) {}
      if (!s || !Array.isArray(s.stars)) return null;
      const stars = s.stars.reduce((a, b) => a + (b || 0), 0);
      const done = s.stars.filter((x) => x > 0).length;
      return { stars, done, open: Math.min(done + 1, 10), total: 10 };
    }
    return null;
  }
  let totS = 0, totC = 0;
  games.forEach((g) => {
    const p = progressOf(g.slug);
    if (!p) return;
    totS += p.stars; totC += p.open;
    const label = fmt(SH.t['game.chapter'], { n: p.open, t: p.total }) + ' · ' + fmt(SH.t['game.stars'], { n: p.stars });
    $$(`[data-mine="${g.slug}"]`).forEach((el) => (el.textContent = label));
    $$(`[data-mine-stars="${g.slug}"]`).forEach((el) => (el.textContent = p.stars + ' ★'));
    const list = $('[data-continue-list]');
    if (list && p.done > 0) {
      $('[data-continue]').hidden = false;
      list.insertAdjacentHTML('beforeend', `<a class="row-card" data-game="${g.slug}" href="${SH.root + g.play}"><img src="${SH.root}games/${g.slug}/icon.webp" alt=""><div><p class="row-card__title">${g.title}</p><div class="t-small">${fmt(SH.t['game.chapter'], { n: p.open, t: p.total })}</div><div class="progress" style="margin-top:8px"><i style="width:${Math.round(p.done / p.total * 100)}%"></i></div></div><span class="stars">${p.stars} ★</span></a>`);
    }
  });
  const ts = $('[data-total-stars]'); if (ts) ts.textContent = totS;
  const tc = $('[data-total-chapters]'); if (tc) tc.textContent = totC;

  const reset = $('[data-reset]');
  if (reset) reset.addEventListener('click', () => {
    if (!confirm(SH.t['progress.resetConfirm'])) return;
    try { Object.keys(localStorage).filter((k) => /^(uc-|nv-|sh:)/.test(k)).forEach((k) => localStorage.removeItem(k)); } catch (e) {}
    location.reload();
  });

  /* uscita dal gioco */
  const ex = $('[data-exit]'); if (ex) ex.addEventListener('click', () => openSheet('exit'));
})();
