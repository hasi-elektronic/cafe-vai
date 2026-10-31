(() => {
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const D = JSON.parse($('#kdata').textContent);
  const ITEMS = D.items, UI = D.ui;
  let lang = 'de';
  try { const l = localStorage.getItem('vai-lang'); if (l) lang = l; } catch (e) {}
  if (new URLSearchParams(location.search).get('l')) lang = new URLSearchParams(location.search).get('l');
  const t = k => (UI[k] && (UI[k][lang] || UI[k].de)) || k;
  const nm = it => it.name[lang] || it.name.de;
  const eur = c => (c / 100).toFixed(2).replace('.', ',') + ' €';
  const vlabel = k => t(k);
  const norm = s => s.toLowerCase().replace(/ß/g, 'ss').replace(/ı/g, 'i').replace(/ş/g, 's').replace(/ğ/g, 'g')
    .normalize('NFD').replace(/[̀-ͯ]/g, '');
  const rm = matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------- Sprache ---------- */
  function setLang(l) {
    lang = l;
    try { localStorage.setItem('vai-lang', l); } catch (e) {}
    if (document.body.classList.contains('kp')) document.documentElement.lang = l;
    $$('.i').forEach(el => {
      if (el.dataset.de === undefined) el.dataset.de = el.textContent;
      el.textContent = l === 'de' ? el.dataset.de : (el.dataset[l] || el.dataset.de);
    });
    $$('.lang button').forEach(b => b.classList.toggle('on', b.dataset.l === l));
    const q = $('#q'); q.placeholder = l === 'de' ? phDe : (q.dataset['ph' + l[0].toUpperCase() + l.slice(1)] || phDe);
    buildIndex(); filter(); bfStatus(); renderCart();
  }
  // placeholder in DE merken
  const q = $('#q'); const phDe = q.getAttribute('placeholder');

  /* ---------- Suchindex ---------- */
  let idx = {};
  function buildIndex() {
    Object.values(ITEMS).forEach(it => {
      const cat = D.cats.find(c => c.id === it.cat);
      const parts = [it.name.de, it.name.en, it.name.tr, cat.t.de, cat.t.en, cat.t.tr];
      if (it.desc) parts.push(it.desc.de, it.desc.en, it.desc.tr);
      idx[it.id] = norm(parts.join(' '));
    });
  }

  /* ---------- Filter ---------- */
  const active = new Set();
  const lis = $$('.it'), total = lis.length;
  function filter() {
    const qs = norm($('#q').value.trim()).split(/\s+/).filter(Boolean);
    let vis = 0;
    lis.forEach(li => {
      const it = ITEMS[li.dataset.id];
      let ok = qs.every(w => idx[it.id].includes(w));
      if (active.has('u10') && +li.dataset.p >= 1000) ok = false;
      ['best', 'veg', 'home'].forEach(f => { if (active.has(f) && !li.dataset.b.split(' ').includes(f)) ok = false; });
      li.hidden = !ok; if (ok) vis++;
    });
    $$('.grp').forEach(g => g.hidden = !$$('.it:not([hidden])', g).length);
    $$('.cat').forEach(c => {
      const has = $$('.it:not([hidden])', c).length > 0;
      c.hidden = !has;
      const tab = $(`.tabs a[data-c="${c.dataset.c}"]`); if (tab) tab.hidden = !has;
    });
    $('#none').hidden = vis > 0;
    const h = total - vis;
    $('#kcnt').textContent = t('count').replace('{v}', vis).replace('{t}', total) + (h ? ' · ' + t('hidden').replace('{h}', h) : '');
  }
  $('#q').addEventListener('input', filter);
  $$('.chip').forEach(c => c.addEventListener('click', () => {
    const f = c.dataset.f; const on = !active.has(f);
    on ? active.add(f) : active.delete(f); c.setAttribute('aria-pressed', on); filter();
  }));
  // nur Chips zeigen, die vorkommen
  $$('.chip').forEach(c => {
    const f = c.dataset.f;
    const has = f === 'u10' ? true : lis.some(li => li.dataset.b.split(' ').includes(f));
    c.hidden = !has;
  });

  /* ---------- Frühstücks-Status (Berlin) ---------- */
  function bfStatus() {
    const p = new Intl.DateTimeFormat('en-GB', { timeZone: 'Europe/Berlin', weekday: 'short', hour: '2-digit', minute: '2-digit', hour12: false }).formatToParts(new Date());
    const g = x => p.find(y => y.type === x).value;
    const d = g('weekday'), h = +g('hour') + +g('minute') / 60;
    const on = (d === 'Sat' || d === 'Sun') && h >= 9 && h < 12.5;
    $('#bftxt').textContent = on ? t('open_b') : t('open_a');
    $('#bfchip').classList.toggle('on', on);
    const lv = $('#bfstatus'); if (lv) lv.textContent = on ? '● ' + t('open_b') : '';
  }

  /* ---------- Warenkorb ---------- */
  const cart = new Map(); // key -> {id, v, o, n}
  const key = (id, v, o) => [id, v || '', o ?? ''].join('|');
  const unit = (it, v) => it.vars ? it.vars.find(x => x[0] === v)[1] : it.c;
  function add(id, v, o) {
    const it = ITEMS[id];
    if (it.vars && !v) v = it.vars[0][0];
    if (it.opts && o == null) o = 0;
    const k = key(id, v, o); const e = cart.get(k) || { id, v, o, n: 0 };
    e.n++; cart.set(k, e);
    toast(nm(it) + [v ? ' · ' + vlabel(v) : '', o != null ? ' · ' + it.opts[o] : ''].join('') + ' ✓'); renderCart();
    if (navigator.vibrate) navigator.vibrate(12);
  }
  function renderCart() {
    let n = 0, sum = 0;
    cart.forEach(e => { n += e.n; sum += e.n * unit(ITEMS[e.id], e.v); });
    $('#cartbar').hidden = n === 0;
    $('#cartn').textContent = n; $('#carttot').textContent = n + ' ' + t('pos') + ' · ' + eur(sum);
    const ul = $('#clist'); ul.innerHTML = '';
    cart.forEach((e, k) => {
      const it = ITEMS[e.id]; const li = document.createElement('li');
      const sub = [e.v ? vlabel(e.v) : '', e.o != null ? it.opts[e.o] : ''].filter(Boolean).join(' · ');
      li.innerHTML = `<span>${esc(nm(it))}<small>${esc(sub)}</small></span><span class="qty"><button type="button" data-m="${k}">−</button><b>${e.n}</b><button type="button" data-p="${k}">+</button></span><b>${eur(e.n * unit(it, e.v))}</b>`;
      ul.appendChild(li);
    });
    $('#cempty').hidden = n > 0; $('#ctot').textContent = eur(sum);
    ['cshow', 'csend'].forEach(i => $('#' + i).disabled = n === 0);
    $('#cartbar').dataset.sum = sum;
  }
  const esc = s => s.replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  $('#clist').addEventListener('click', e => {
    const m = e.target.dataset.m, p = e.target.dataset.p;
    if (m) { const x = cart.get(m); x.n--; if (x.n <= 0) cart.delete(m); }
    if (p) cart.get(p).n++;
    renderCart();
  });
  let toastT;
  function toast(msg) { const el = $('#toastg'); el.textContent = msg; el.classList.add('show'); clearTimeout(toastT); toastT = setTimeout(() => el.classList.remove('show'), 1600); }

  /* ---------- Dialoge ---------- */
  function openD(d) { if (!d.open) d.showModal(); }
  function closeD(d) {
    if (!d.open) return;
    if (rm) { d.close(); return; }
    d.classList.add('closing'); setTimeout(() => { d.classList.remove('closing'); d.close(); }, 200);
  }
  $$('dialog').forEach(d => {
    d.addEventListener('cancel', e => { e.preventDefault(); closeD(d); });
    d.addEventListener('click', e => { if (e.target === d) closeD(d); });
    $$('[data-close]', d).forEach(b => b.addEventListener('click', () => closeD(d)));
  });
  let cur = null, curV = null, curO = 0;
  function showItem(id, push = true, v = null) {
    const it = ITEMS[id]; cur = id;
    curV = it.vars ? (v && it.vars.some(x => x[0] === v) ? v : it.vars[0][0]) : null; curO = 0;
    drawItem();
    openD($('#dlg'));
    if (push) history.replaceState(null, '', '?g=' + id + (lang !== 'de' ? '&l=' + lang : ''));
  }
  function drawItem() {
    const it = ITEMS[cur];
    const img = it.imgs ? it.imgs[Math.min(curO, it.imgs.length - 1)] : null;
    $('#dimg').innerHTML = img ? `<img src="assets/${img[0]}" alt="" style="object-position:${img[1]}">` : '';
    $('#dname').textContent = nm(it);
    $('#ddesc').textContent = it.desc ? (it.desc[lang] || it.desc.de) : '';
    $('#dbd').innerHTML = it.badges.map(b => `<em class="bd b-${b}">${t(b)}</em>`).join('');
    $('#dopts').innerHTML = it.opts ? it.opts.map((o, i) => `<button type="button" data-o="${i}" aria-pressed="${i === curO}">${esc(o)}</button>`).join('') : '';
    $('#dvars').innerHTML = it.vars ? it.vars.map(([k, c]) => `<button type="button" data-v="${k}" aria-pressed="${k === curV}">${t(k)}<small>${eur(c)}</small></button>`).join('') : '';
    $('#dprice').textContent = eur(unit(it, curV));
  }
  $('#dopts').addEventListener('click', e => { const b = e.target.closest('[data-o]'); if (b) { curO = +b.dataset.o; drawItem(); } });
  $('#dvars').addEventListener('click', e => { const b = e.target.closest('[data-v]'); if (b) { curV = b.dataset.v; drawItem(); } });
  $('#dadd').addEventListener('click', () => add(cur, curV, ITEMS[cur].opts ? curO : null));
  $('#dshare').addEventListener('click', async () => {
    const url = location.origin + location.pathname + '?g=' + cur;
    try { if (navigator.share) { await navigator.share({ title: nm(ITEMS[cur]) + ' — Café VAI', url }); return; } } catch (e) { return; }
    try { await navigator.clipboard.writeText(url); toast(t('copied')); } catch (e) { toast(url); }
  });
  $('#dlg').addEventListener('close', () => { history.replaceState(null, '', location.pathname + (lang !== 'de' ? '?l=' + lang : '')); });

  document.addEventListener('click', e => {
    const o = e.target.closest('[data-open]'); if (o) { const li = o.closest('.it'); const sp = li && li.querySelector('.vp.on'); showItem(o.dataset.open, true, sp ? sp.dataset.v : null); return; }
    const vp = e.target.closest('.vp');
    if (vp) { $$('.vp', vp.parentElement).forEach(x => { const on = x === vp; x.classList.toggle('on', on); x.setAttribute('aria-pressed', on); }); return; }
    const a = e.target.closest('[data-add]');
    if (a) {
      const it = ITEMS[a.dataset.add]; const li = a.closest('.it');
      const sel = li && li.querySelector('.vp.on'); const v = sel ? sel.dataset.v : null;
      if (it.opts) { showItem(a.dataset.add, false, v); return; }
      add(a.dataset.add, v); a.classList.add('ok'); setTimeout(() => a.classList.remove('ok'), 500);
    }
  });
  $('#cartopen').addEventListener('click', () => { renderCart(); openD($('#cdlg')); });

  /* ---------- Bestellzettel ---------- */
  $('#cshow').addEventListener('click', () => {
    const tbl = $('#tbl').value.trim();
    $('#stbl').textContent = tbl ? t('table') + ' ' + tbl : '';
    const ul = $('#slist'); ul.innerHTML = ''; let sum = 0;
    cart.forEach(e => {
      const it = ITEMS[e.id]; const c = e.n * unit(it, e.v); sum += c;
      const sub = [e.v ? vlabel(e.v) : '', e.o != null ? it.opts[e.o] : ''].filter(Boolean).join(' · ');
      const li = document.createElement('li');
      li.innerHTML = `<span>${e.n}× ${esc(nm(it))}${sub ? `<small>${esc(sub)}</small>` : ''}</span><span>${eur(c)}</span>`; ul.appendChild(li);
    });
    $('#stot').textContent = eur(sum);
    $('#stime').textContent = new Date().toLocaleTimeString(lang === 'de' ? 'de-DE' : lang === 'tr' ? 'tr-TR' : 'en-GB', { hour: '2-digit', minute: '2-digit', timeZone: 'Europe/Berlin' });
    closeD($('#cdlg')); setTimeout(() => openD($('#sdlg')), 220);
  });
  $('#csend').addEventListener('click', () => {
    const el = $('#ctoast'); el.textContent = t('sent'); el.classList.remove('show'); void el.offsetWidth; el.classList.add('show');
  });

  /* ---------- Reiterleiste: Scroll-Spy ---------- */
  const tabs = $('#tabs'), cats = $$('.cat'), hero = $('.hero-k'), bar = $('#bar'), own = document.body.classList.contains('kp');
  function spy() {
    const y = innerHeight * 0.35; let cur = null;
    cats.forEach(c => { if (!c.hidden && c.getBoundingClientRect().top < y) cur = c.dataset.c; });
    $$('a', tabs).forEach(a => {
      const on = a.dataset.c === cur; a.classList.toggle('an', on);
      if (on && !a._seen) { a._seen = 1; tabs.scrollTo({ left: a.offsetLeft - tabs.clientWidth / 2 + a.clientWidth / 2, behavior: rm ? 'auto' : 'smooth' }); }
      if (!on) a._seen = 0;
    });
    if (hero) tabs.classList.toggle('show', scrollY > hero.offsetHeight * 0.6);
    if (own) bar.style.transform = `scaleX(${Math.min(1, scrollY / (document.documentElement.scrollHeight - innerHeight))})`;
  }
  addEventListener('scroll', spy, { passive: true }); addEventListener('resize', spy);
  $$('a', tabs).forEach(a => a.addEventListener('click', e => {
    e.preventDefault();
    const c = $(a.getAttribute('href')); window.scrollTo({ top: c.getBoundingClientRect().top + scrollY - (own ? (innerWidth >= 900 ? 175 : 150) : (innerWidth >= 900 ? 150 : 140)), behavior: rm ? 'auto' : 'smooth' });
  }));

  /* ---------- Einblenden ---------- */
  const io = new IntersectionObserver(es => es.forEach(en => { if (en.isIntersecting) { en.target.classList.add('vis'); io.unobserve(en.target); } }), { rootMargin: '0px 0px -8% 0px' });
  $$('.it').forEach((li, i) => { li.classList.add('pre'); li.style.transitionDelay = (i % 4) * 60 + 'ms'; io.observe(li); });
  $$('.catimg').forEach(c => io.observe(c));

  $('#printbtn').addEventListener('click', () => window.print());
  $$('.lang button').forEach(b => b.addEventListener('click', () => setLang(b.dataset.l)));

  /* ---------- Start ---------- */
  setLang(lang);
  spy();
  const g = new URLSearchParams(location.search).get('g');
  if (g && ITEMS[g]) {
    const el = $(`.it[data-id="${g}"]`); if (el) { el.classList.add('vis'); window.scrollTo(0, el.getBoundingClientRect().top + scrollY - 120); }
    showItem(g, false);
  }
})();
