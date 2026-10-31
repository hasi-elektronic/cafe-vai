(() => {
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const clamp = (v, a = 0, b = 1) => Math.min(b, Math.max(a, v));
  const lerp = (a, b, t) => a + (b - a) * t;
  const ease = t => 1 - Math.pow(1 - t, 3);
  const rm = matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (rm) document.documentElement.classList.add('rm');

  let vw = innerWidth, vh = innerHeight;
  const mobile = () => vw < 760;

  /* ---------- word-fill text ---------- */
  const fill = $('#fill');
  const words = [];
  if (fill) {
    fill.dataset.text.split(' ').forEach(raw => {
      const s = document.createElement('span');
      let w = raw;
      if (w.startsWith('*')) { s.classList.add('am'); w = w.slice(1); }
      if (w.endsWith('*')) { w = w.slice(0, -1); }
      s.textContent = w;
      // amber continues until the closing * word
      words.push(s); fill.appendChild(s);
    });
    // second pass: mark whole amber phrases ("Meet for coffee, stay for more.")
    let inAm = false;
    fill.dataset.text.split(' ').forEach((raw, i) => {
      if (raw.startsWith('*')) inAm = true;
      if (inAm) words[i].classList.add('am');
      if (raw.endsWith('*')) inAm = false;
    });
  }

  /* ---------- scenes ---------- */
  const hero = $('.hero'), frame = $('#frame'), slides = $$('.slide'), caps = $$('.cap');
  const bgtext = $('#bgtext'), intro = $('#intro'), hint = $('#hint');
  const ticks = $('#ticks'), tickB = $$('#ticks b'), count = $('#count');
  const menu = $('.menu-sec'), track = $('#track'), panels = $$('.panel:not(.lead)'), hprog = $('#hprog');
  const spot = $('#spot'), spotbg = $('#spotbg');
  const story = $('.story'), steps = $$('.step'), screens = $$('.screen'), phone = $('#phone');
  const parimg = $('#parimg');
  const nav = $('#nav'), bar = $('#bar'), dock = $('#dock');

  let heroTop, heroH, menuTop, menuH, storyTop, storyH, trackW, panelPos = [];

  // progress buttons
  panels.forEach((p, i) => {
    const b = document.createElement('button');
    b.innerHTML = String(i + 1).padStart(2, '0') + ' ' + p.dataset.label;
    b.addEventListener('click', () => scrollToPanel(i));
    hprog.appendChild(b);
  });
  const pbtn = hprog ? $$('button', hprog) : [];

  function measure() {
    vw = innerWidth; vh = innerHeight;
    const y = scrollY;
    if (hero) { const r = hero.getBoundingClientRect(); heroTop = r.top + y; heroH = hero.offsetHeight; }
    if (story) { const r = story.getBoundingClientRect(); storyTop = r.top + y; storyH = story.offsetHeight; }
    if (menu && !rm) {
      const last = track.lastElementChild;
      trackW = last.offsetLeft + last.offsetWidth;
      menu.style.height = (trackW - vw + vh) + 'px';
      const r = menu.getBoundingClientRect(); menuTop = r.top + y; menuH = menu.offsetHeight;
      panelPos = panels.map(p => ({ l: p.offsetLeft, w: p.offsetWidth }));
    }
  }

  function scrollToPanel(i) {
    const maxX = trackW - vw;
    const x = clamp((panelPos[i].l - vw * (mobile() ? 0.02 : 0.08)) / maxX);
    scrollTo({ top: menuTop + x * (menuH - vh), behavior: 'smooth' });
  }

  /* ---------- renderers ---------- */
  function renderHero(sy) {
    const p = clamp((sy - heroTop) / (heroH - vh));
    const m = mobile();
    const e = ease(clamp(p / 0.2));
    const sT = m ? 20 : 17, eT = m ? 12 : 4;
    const sB = m ? 40 : 17, eB = m ? 40 : 4;
    const sL = m ? 16 : 34, eL = m ? 4 : 3;
    frame.style.clipPath = `inset(${lerp(sT, eT, e)}vh ${lerp(sL, eL, e)}vw ${lerp(sB, eB, e)}vh round ${lerp(36, 22, e)}px)`;
    bgtext.style.opacity = 1 - e * 0.85;
    bgtext.style.transform = `scale(${1 + e * 0.18})`;
    intro.style.opacity = 1 - clamp(p / 0.07);
    intro.style.transform = `translateY(${-p * 300}px)`;
    hint.style.opacity = 1 - clamp(p / 0.05);
    const capOn = ease(clamp((p - 0.13) / 0.07));
    const s = clamp((p - 0.2) / 0.8) * 4;
    slides.forEach((sl, i) => {
      const c = i + 0.5;
      let d = Math.abs(s - c);
      if (i === 0 && s < c) d = 0;
      if (i === 3 && s > c) d = 0;
      const o = clamp((0.62 - d) / 0.24);
      sl.style.opacity = o;
      sl.style.transform = `scale(${1.06 - 0.05 * clamp(s - i, 0, 1.2)})`;
      sl.style.zIndex = i === Math.min(3, Math.floor(s)) ? 2 : 1;
      const cp = caps[i];
      cp.style.opacity = o * capOn;
      cp.style.transform = `translateY(${(1 - o) * (s > c ? -34 : 34)}px)`;
    });
    ticks.style.opacity = capOn; count.style.opacity = capOn;
    tickB.forEach((b, i) => b.style.transform = `scaleY(${clamp(s - i)})`);
    count.firstElementChild.textContent = String(Math.min(3, Math.floor(s)) + 1).padStart(2, '0');
  }

  function renderMenu(sy) {
    const p = clamp((sy - menuTop) / (menuH - vh));
    const x = p * (trackW - vw);
    track.style.transform = `translate3d(${-x}px,0,0)`;
    pbtn.forEach((b, i) => {
      const pp = panelPos[i];
      const f = clamp((x + vw * 0.62 - pp.l) / pp.w);
      b.style.setProperty('--f', f);
      b.classList.toggle('on', f > 0 && f < 1 || (i === pbtn.length - 1 && f >= 1));
    });
  }

  function renderStory(sy) {
    const p = clamp((sy - storyTop) / (storyH - vh));
    const idx = Math.min(3, Math.floor(p * 4.0001));
    steps.forEach((s, i) => s.classList.toggle('on', i === idx));
    screens.forEach((s, i) => s.classList.toggle('on', i === idx));
    phone.style.transform = `rotateY(${(0.5 - p) * 16}deg) rotateX(${Math.sin(p * Math.PI) * 3}deg)`;
  }

  function renderFill() {
    if (!fill) return;
    const r = fill.getBoundingClientRect();
    const pf = clamp((vh * 0.82 - r.top) / (r.height + vh * 0.3));
    const n = words.length;
    words.forEach((w, i) => w.classList.toggle('on', i / n < pf * 1.04));
  }

  function renderParallax() {
    if (parimg) {
      const r = parimg.parentElement.getBoundingClientRect();
      if (r.bottom > 0 && r.top < vh) parimg.style.transform = `translate3d(0,${(r.top + r.height / 2 - vh / 2) * -0.1}px,0)`;
    }
    if (spot) {
      const r = spot.getBoundingClientRect();
      if (r.bottom > 0 && r.top < vh) {
        const t = clamp((vh - r.top) / (vh + r.height));
        spotbg.style.transform = `translate3d(0,${(t - 0.5) * -r.height * 0.16}px,0)`;
      }
    }
  }

  /* ---------- loop ---------- */
  let sy = scrollY, lastY = scrollY, navHidden = false;
  const docMax = () => document.documentElement.scrollHeight - vh;
  const sections = $$('section[id]');
  const links = $$('.nav ul a');

  function frameRender() {
    const target = scrollY;
    sy = Math.abs(target - sy) < 0.2 ? target : lerp(sy, target, 0.14);
    if (hero) renderHero(sy);
    if (menu && !rm) renderMenu(sy);
    if (story) renderStory(sy);
    renderFill(); renderParallax();
    bar.style.transform = `scaleX(${clamp(target / docMax())})`;
    nav.classList.toggle('solid', target > 40);
    if (dock) dock.classList.toggle('show', target > 260);
    const down = target > lastY + 2, up = target < lastY - 2;
    if (down && target > 500 && !navHidden && !$('#sheet').classList.contains('open')) { nav.classList.add('hide'); navHidden = true; document.body.classList.add('nav-hidden'); }
    if (up && navHidden) { nav.classList.remove('hide'); navHidden = false; document.body.classList.remove('nav-hidden'); }
    lastY = target;
    // active link
    let cur = '';
    sections.forEach(s => { if (s.getBoundingClientRect().top < vh * 0.45) cur = s.id; });
    links.forEach(a => a.classList.toggle('on', a.getAttribute('href') === '#' + cur));
    requestAnimationFrame(frameRender);
  }

  /* ---------- reduced motion static ---------- */
  function staticHero() {
    frame.style.clipPath = 'none';
    slides.forEach((s, i) => { s.style.opacity = i === 0 ? 1 : 0; });
    caps.forEach((c, i) => { c.style.opacity = i === 0 ? 1 : 0; });
    intro.style.display = 'none'; hint.style.display = 'none'; ticks.style.display = 'none'; count.style.display = 'none';
    screens.forEach((s, i) => s.classList.toggle('on', i === 2));
    words.forEach(w => w.classList.add('on'));
  }

  /* ---------- anchors, burger ---------- */
  $$('a[href^="#"]').forEach(a => a.addEventListener('click', e => {
    if (a.closest('#tabs')) return;
    const id = a.getAttribute('href'); if (id.length < 2) return;
    const t = $(id); if (!t) return;
    e.preventDefault();
    $('#sheet').classList.remove('open'); $('#burger').classList.remove('open');
    let y = t.getBoundingClientRect().top + scrollY;
    if (id === '#top') y = 0;
    scrollTo({ top: y, behavior: rm ? 'auto' : 'smooth' });
  }));
  $('#burger').addEventListener('click', () => { $('#sheet').classList.toggle('open'); $('#burger').classList.toggle('open'); nav.classList.remove('hide'); navHidden = false; document.body.classList.remove('nav-hidden'); });

  /* ---------- counters ---------- */
  const io = new IntersectionObserver(es => es.forEach(en => {
    if (!en.isIntersecting) return; io.unobserve(en.target);
    const el = en.target, to = parseFloat(el.dataset.count), dec = +(el.dataset.dec || 0), suf = el.dataset.suf || '';
    if (rm) return;
    const t0 = performance.now();
    (function step(t) {
      const k = ease(clamp((t - t0) / 1400));
      el.textContent = (to * k).toFixed(dec).replace('.', ',') + suf;
      if (k < 1) requestAnimationFrame(step);
    })(t0);
  }), { threshold: 0.6 });
  $$('[data-count]').forEach(el => io.observe(el));

  /* ---------- hours + status (Europe/Berlin) ---------- */
  const OPEN = { 5: [[11, 14], [17, 22]], 6: [[9, 14], [17, 22]], 0: [[9, 20]] };
  (function hours() {
    const parts = new Intl.DateTimeFormat('en-GB', { timeZone: 'Europe/Berlin', weekday: 'short', hour: '2-digit', minute: '2-digit', hour12: false }).formatToParts(new Date());
    const g = t => parts.find(p => p.type === t).value;
    const dmap = { Sun: 0, Mon: 1, Tue: 2, Wed: 3, Thu: 4, Fri: 5, Sat: 6 };
    const d = dmap[g('weekday')], h = +g('hour') + +g('minute') / 60;
    $$('#hours tr').forEach(tr => tr.classList.toggle('today', +tr.dataset.d === d));
    const st = $('#status'), tx = $('#statustxt');
    const slots = OPEN[d];
    if (slots) {
      const cur = slots.find(([a, b]) => h >= a && h < b);
      if (cur) { st.classList.add('open'); tx.textContent = `Jetzt geöffnet · bis ${cur[1]} Uhr`; }
      else {
        const next = slots.find(([a]) => h < a);
        st.classList.add('closed');
        tx.textContent = next ? `Gerade zu · öffnet heute um ${next[0]} Uhr` : 'Heute geschlossen · bis zum nächsten Mal';
      }
    } else if (d === 1) { st.classList.add('closed'); tx.textContent = 'Montag Ruhetag'; }
    else { tx.textContent = 'Heute: Lieferservice & Abholung'; }
  })();

  /* ---------- reservation demo ---------- */
  const SLOTS = { 5: ['11:00', '12:00', '13:00', '17:30', '19:00', '20:30'], 6: ['9:00', '10:30', '12:00', '17:30', '19:00', '20:30'], 0: ['9:00', '10:30', '12:00', '14:00', '16:00', '18:00'] };
  const DN = { 5: 'Freitag', 6: 'Samstag', 0: 'Sonntag' };
  let day = 5, time = null, pers = 2;
  const times = $('#times'), persEl = $('#pers'), toast = $('#toast');
  function drawTimes() {
    times.innerHTML = '';
    SLOTS[day].forEach((t, i) => {
      const b = document.createElement('button'); b.textContent = t;
      if (i === 3 || (day !== 5 && i === 0 && false)) { /* default */ }
      b.addEventListener('click', () => { time = t; $$('button', times).forEach(x => x.classList.toggle('on', x === b)); });
      times.appendChild(b);
    });
    time = null;
  }
  $$('#days button').forEach(b => b.addEventListener('click', () => {
    day = +b.dataset.d; $$('#days button').forEach(x => x.classList.toggle('on', x === b)); drawTimes(); toast.classList.remove('show');
  }));
  $('#minus').addEventListener('click', () => { pers = Math.max(1, pers - 1); persEl.textContent = pers + ' Pers.'; });
  $('#plus').addEventListener('click', () => { pers = Math.min(8, pers + 1); persEl.textContent = pers + ' Pers.'; });
  $('#resbtn').addEventListener('click', () => {
    if (!time) { toast.textContent = 'Bitte wähle zuerst eine Uhrzeit.'; toast.classList.add('show'); return; }
    toast.innerHTML = `<b>Demo:</b> Anfrage für ${DN[day]}, ${time} Uhr, ${pers} Pers. wäre jetzt im Verwaltungsbereich eingegangen (Kalender, Kapazitätsprüfung, Warteliste). In dieser Demo wird nichts gesendet.`;
    toast.classList.remove('show'); void toast.offsetWidth; toast.classList.add('show');
  });
  drawTimes();

  /* ---------- init ---------- */
  addEventListener('resize', measure);
  addEventListener('load', measure);
  if (document.fonts) document.fonts.ready.then(measure);
  measure();
  if (rm) { staticHero(); renderFill(); addEventListener('scroll', renderFill, { passive: true }); }
  else requestAnimationFrame(frameRender);
})();
