/* Websa Worldwide site behaviour. No dependencies. Everything degrades to plain HTML without JS. */
(function () {
  'use strict';
  var doc = document, root = doc.documentElement, body = doc.body;
  root.classList.add('js');
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var $ = function (s, c) { return (c || doc).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || doc).querySelectorAll(s)); };
  var S = function (key, vars) {
    var t = body.getAttribute('data-s-' + key) || '';
    Object.keys(vars || {}).forEach(function (k) { t = t.split('%' + k).join(vars[k]); });
    return t;
  };
  var lang = (root.getAttribute('lang') || 'en').split('-')[0];
  var pageTitle = body.getAttribute('data-page-title') || doc.title;
  var endpoint = body.getAttribute('data-form-endpoint') || '';
  var provider = body.getAttribute('data-analytics') || '';
  function store(k, v) { try { if (v === undefined) return localStorage.getItem(k); if (v === null) localStorage.removeItem(k); else localStorage.setItem(k, v); } catch (e) { return null; } }

  /* Analytics: no-op unless a provider is configured */
  function track(name, props) {
    try {
      if (provider === 'plausible' && window.plausible) window.plausible(name, { props: props || {} });
      else if (provider === 'ga4' && window.gtag) window.gtag('event', name, props || {});
    } catch (e) {}
  }
  doc.addEventListener('click', function (e) {
    var el = e.target.closest('[data-track]');
    if (el) track(el.getAttribute('data-track'), { name: el.getAttribute('data-track-name') || el.textContent.trim().slice(0, 60), page: pageTitle });
  });
  var consent = $('#consent');
  if (consent) {
    if (!store('ww-consent')) consent.hidden = false;
    $$('[data-consent]', consent).forEach(function (b) {
      b.addEventListener('click', function () {
        var v = b.getAttribute('data-consent'); store('ww-consent', v); consent.hidden = true;
        if (window.gtag) window.gtag('consent', 'update', { analytics_storage: v });
      });
    });
  }

  /* Header: shadow when scrolled, slides away on scroll down and back on scroll up */
  var header = $(".site-header"), lastY = window.scrollY;
  function onScrollHeader() {
    if (!header) return;
    var y = window.scrollY;
    header.classList.toggle('scrolled', y > 8);
    var drawerOpen = drawer && drawer.classList.contains('open');
    var menuOpen = !!$('.has-menu.open');
    if (!drawerOpen && !menuOpen && y > lastY + 6 && y > 160) header.classList.add('hide');
    if (y < lastY - 6 || y <= 160) header.classList.remove('hide');
    lastY = y;
  }
  window.addEventListener('scroll', onScrollHeader, { passive: true }); onScrollHeader();

  /* Inner page hero: gentle parallax on the background photo */
  var phBg = $('.page-hero img.bg'), heroBgs = $$('.hero .slide img');
  if (!reduce && window.matchMedia('(min-width: 768px)').matches) {
    var pTick = false;
    window.addEventListener('scroll', function () {
      if (pTick) return; pTick = true;
      requestAnimationFrame(function () {
        var y = Math.min(window.scrollY, 900);
        if (phBg) phBg.style.transform = 'translateY(' + (y * 0.22) + 'px)';
        pTick = false;
      });
    }, { passive: true });
  }

  /* Counters: numbers in stat tiles count up when they scroll into view */
  var counters = $$('[data-count]');
  if (counters.length && !reduce && 'IntersectionObserver' in window) {
    var cio = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return; cio.unobserve(en.target);
        var el = en.target, text = el.textContent, m = text.match(/(\d+(?:\.\d+)?)/);
        if (!m) return;
        var target = parseFloat(m[1]), decimals = (m[1].split('.')[1] || '').length, start = null, dur = 1300;
        function frame(ts) {
          if (!start) start = ts;
          var t = Math.min(1, (ts - start) / dur), eased = 1 - Math.pow(1 - t, 3);
          el.textContent = text.replace(m[1], (target * eased).toFixed(decimals));
          if (t < 1) requestAnimationFrame(frame); else el.textContent = text;
        }
        requestAnimationFrame(frame);
      });
    }, { threshold: 0.4 });
    counters.forEach(function (c) { cio.observe(c); });
  }

  /* Dropdown menus (nav groups and the language pill) */
  var menus = $$('.has-menu');
  function closeMenus(except) {
    menus.forEach(function (li) {
      if (li !== except) { li.classList.remove('open'); var b = $('.nav-link', li); if (b) b.setAttribute('aria-expanded', 'false'); }
    });
  }
  menus.forEach(function (li) {
    var btn = $('.nav-link', li), timer;
    if (!btn) return;
    btn.addEventListener('click', function (e) {
      e.preventDefault(); var open = li.classList.toggle('open'); btn.setAttribute('aria-expanded', open ? 'true' : 'false'); closeMenus(li);
    });
    li.addEventListener('mouseenter', function () {
      if (!window.matchMedia('(hover: hover)').matches) return;
      clearTimeout(timer); closeMenus(li); li.classList.add('open'); btn.setAttribute('aria-expanded', 'true');
    });
    li.addEventListener('mouseleave', function () {
      if (!window.matchMedia('(hover: hover)').matches) return;
      timer = setTimeout(function () { li.classList.remove('open'); btn.setAttribute('aria-expanded', 'false'); }, 160);
    });
    li.addEventListener('focusout', function (e) { if (!li.contains(e.relatedTarget)) { li.classList.remove('open'); btn.setAttribute('aria-expanded', 'false'); } });
  });
  doc.addEventListener('click', function (e) { if (!e.target.closest('.has-menu')) closeMenus(); });
  $$('.lang-menu a').forEach(function (a) {
    if (a.getAttribute('data-lang') === lang) a.setAttribute('aria-current', 'true');
    a.addEventListener('click', function () { store('ww-lang', a.getAttribute('data-lang')); track('language_switch', { to: a.getAttribute('data-lang') }); });
  });

  /* Focus trap for dialogs */
  function trap(container) {
    function onKey(e) {
      if (e.key !== 'Tab') return;
      var f = $$('a[href], button:not([disabled]), input, select, textarea, iframe, [tabindex]:not([tabindex="-1"])', container).filter(function (el) { return el.offsetParent !== null; });
      if (!f.length) return;
      var first = f[0], last = f[f.length - 1];
      if (e.shiftKey && doc.activeElement === first) { e.preventDefault(); last.focus(); }
      else if (!e.shiftKey && doc.activeElement === last) { e.preventDefault(); first.focus(); }
    }
    container.addEventListener('keydown', onKey);
    return function () { container.removeEventListener('keydown', onKey); };
  }
  var lastFocus = null;
  function openDialog(el) { lastFocus = doc.activeElement; el.hidden = false; body.style.overflow = 'hidden'; el._untrap = trap(el); }
  function closeDialog(el) { if (el.hidden) return; el.hidden = true; body.style.overflow = ''; if (el._untrap) el._untrap(); if (lastFocus && lastFocus.focus) lastFocus.focus(); }

  /* Mobile drawer */
  var burger = $('.burger'), drawer = $('.drawer');
  function closeDrawer() { if (!drawer || !drawer.classList.contains('open')) return; drawer.classList.remove('open'); burger.setAttribute('aria-expanded', 'false'); body.style.overflow = ''; }
  if (burger && drawer) {
    burger.addEventListener('click', function () {
      var open = !drawer.classList.contains('open');
      drawer.classList.toggle('open', open); burger.setAttribute('aria-expanded', open ? 'true' : 'false'); body.style.overflow = open ? 'hidden' : '';
      if (open) { var first = $('.group-btn, .single', drawer); if (first) first.focus(); }
    });
    $$('.group-btn', drawer).forEach(function (b) {
      b.addEventListener('click', function () {
        var open = b.getAttribute('aria-expanded') === 'true';
        $$('.group-btn', drawer).forEach(function (o) { o.setAttribute('aria-expanded', 'false'); });
        b.setAttribute('aria-expanded', open ? 'false' : 'true');
      });
    });
    $$('a', drawer).forEach(function (a) { a.addEventListener('click', closeDrawer); });
    window.addEventListener('resize', function () { if (window.innerWidth > 1180) closeDrawer(); });
  }

  /* Site search */
  var overlay = $('#search'), sInput = $('#search-input'), sResults = $('.search-results'), index = null, sActive = -1;
  function loadIndex() {
    if (index) return Promise.resolve(index);
    return fetch('search-index.json').then(function (r) { return r.json(); }).then(function (j) { index = j; return j; }).catch(function () { index = []; return index; });
  }
  function openSearch() { closeDrawer(); openDialog(overlay); loadIndex(); setTimeout(function () { sInput.focus(); }, 30); track('search_open'); }
  function closeSearch() { closeDialog(overlay); }
  $$('[data-open-search]').forEach(function (b) { b.addEventListener('click', openSearch); });
  $$('[data-close-search]').forEach(function (b) { b.addEventListener('click', closeSearch); });
  if (overlay) {
    overlay.addEventListener('click', function (e) { if (e.target === overlay) closeSearch(); });
    $('.search-form', overlay).addEventListener('submit', function (e) { e.preventDefault(); var a = $('.search-results a.is-active', overlay) || $('.search-results a', overlay); if (a) a.click(); });
  }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function highlight(text, terms) {
    var out = esc(text);
    terms.forEach(function (t) { if (t.length < 2) return; out = out.replace(new RegExp('(' + t.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + ')', 'ig'), '<mark>$1</mark>'); });
    return out;
  }
  function runSearch() {
    var q = sInput.value.trim().toLowerCase();
    sActive = -1;
    if (!q) { sResults.innerHTML = ''; return; }
    var terms = q.split(/\s+/).filter(Boolean);
    var scored = index.map(function (e) {
      var t = e.t.toLowerCase(), x = (e.x || '').toLowerCase(), score = 0;
      terms.forEach(function (term) {
        if (t === term) score += 10;
        else if (t.indexOf(term) === 0) score += 6;
        else if (t.indexOf(term) !== -1) score += 4;
        if (x.indexOf(term) !== -1) score += 2;
      });
      if (e.k === 'page') score += 0.5;
      return { e: e, s: score };
    }).filter(function (r) { return r.s > 0; }).sort(function (a, b) { return b.s - a.s; }).slice(0, 12);
    if (!scored.length) { sResults.innerHTML = '<li class="none">' + esc(S('search-none')) + '</li>'; return; }
    sResults.innerHTML = scored.map(function (r) {
      return '<li><a href="' + esc(r.e.u) + '"><span class="st">' + highlight(r.e.t, terms) + '<span class="sk">' + esc(r.e.k) + '</span></span><span class="sx">' + highlight(r.e.x || '', terms) + '</span></a></li>';
    }).join('');
    track('search', { query: q.slice(0, 40), results: scored.length });
  }
  if (sInput) {
    var sTimer;
    sInput.addEventListener('input', function () { clearTimeout(sTimer); sTimer = setTimeout(function () { loadIndex().then(runSearch); }, 80); });
    sInput.addEventListener('keydown', function (e) {
      var items = $$('.search-results a', overlay); if (!items.length) return;
      if (e.key === 'ArrowDown') { e.preventDefault(); sActive = Math.min(items.length - 1, sActive + 1); }
      else if (e.key === 'ArrowUp') { e.preventDefault(); sActive = Math.max(0, sActive - 1); }
      else return;
      items.forEach(function (a, i) { a.classList.toggle('is-active', i === sActive); });
      items[sActive].scrollIntoView({ block: 'nearest' });
    });
  }
  doc.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') { closeMenus(); closeDrawer(); closeBottom(); closeSearch(); closeVideo(); }
    if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k') { e.preventDefault(); openSearch(); }
  });
  var qp = new URLSearchParams(location.search).get('q');
  if (qp && sInput) { sInput.value = qp; openSearch(); loadIndex().then(runSearch); }

  /* Video modal (YouTube loads only on play) */
  var vmodal = $('#video-modal'), vframe = vmodal && $('.video-frame', vmodal);
  function openVideo(id, title) {
    if (!vmodal) return;
    vframe.innerHTML = '<iframe src="https://www.youtube-nocookie.com/embed/' + encodeURIComponent(id) + '?autoplay=1&rel=0&modestbranding=1&hl=' + lang + '" title="' + esc(title || 'Video') + '" allow="autoplay; encrypted-media; picture-in-picture; fullscreen" allowfullscreen loading="lazy"></iframe>';
    openDialog(vmodal); setTimeout(function () { var c = $('[data-close-video]', vmodal); if (c) c.focus(); }, 30);
  }
  function closeVideo() { if (!vmodal || vmodal.hidden) return; vframe.innerHTML = ''; closeDialog(vmodal); }
  $$('[data-video]').forEach(function (b) { b.addEventListener('click', function () { openVideo(b.getAttribute('data-video'), b.getAttribute('data-video-title')); }); });
  $$('[data-close-video]').forEach(function (b) { b.addEventListener('click', closeVideo); });
  if (vmodal) vmodal.addEventListener('click', function (e) { if (e.target === vmodal) closeVideo(); });

  /* WhatsApp links carry the page context */
  function waText(extra) { return (S('wa-hello') + ' ' + S('wa-page', { p: pageTitle }) + (extra ? ' ' + extra : '')).trim(); }
  $$('[data-wa]').forEach(function (a) { a.href = 'https://wa.me/8617324010515?text=' + encodeURIComponent(waText()); });

  /* Hero slideshow */
  var hero = $('.hero');
  if (hero) {
    var slides = $$('.slide', hero), idx = 0, playing = !reduce, t, pause = $('.pause', hero);
    function show(n) { slides.forEach(function (s, i) { s.classList.toggle('is-active', i === n); }); idx = n; }
    function next() { show((idx + 1) % slides.length); }
    function start() { if (slides.length < 2) return; clearInterval(t); t = setInterval(next, 6000); }
    function stop() { clearInterval(t); }
    show(0); if (playing) start();
    if (pause) {
      pause.setAttribute('aria-pressed', playing ? 'false' : 'true');
      pause.addEventListener('click', function () {
        playing = !playing; pause.setAttribute('aria-pressed', playing ? 'false' : 'true'); pause.setAttribute('aria-label', playing ? S('pause') : S('play')); playing ? start() : stop();
      });
    }
    doc.addEventListener('visibilitychange', function () { if (doc.hidden) stop(); else if (playing) start(); });
  }

  /* Section dots and bottom bar (home) */
  var dots = $$('.dots-nav a'), bottomBar = $('.bottom-bar');
  if (dots.length) {
    var targets = dots.map(function (a) { return $(a.getAttribute('href')); }).filter(Boolean);
    var spy = function () {
      var y = window.scrollY + window.innerHeight * 0.4, current = targets[0];
      targets.forEach(function (s) { if (s.offsetTop <= y) current = s; });
      dots.forEach(function (a) { a.classList.toggle('is-active', a.getAttribute('href') === '#' + current.id); });
      $('.dots-nav').classList.toggle('on-dark', current.classList.contains('dark') || current.classList.contains('hero'));
      if (bottomBar) bottomBar.classList.toggle('show', window.scrollY < body.scrollHeight - window.innerHeight - 260);
    };
    window.addEventListener('scroll', spy, { passive: true }); window.addEventListener('resize', spy); spy();
  }
  var bbButtons = $$('.bb-group > button');
  function closeBottom() { bbButtons.forEach(function (b) { b.setAttribute('aria-expanded', 'false'); }); }
  bbButtons.forEach(function (b) {
    b.addEventListener('click', function (e) { e.stopPropagation(); var open = b.getAttribute('aria-expanded') === 'true'; closeBottom(); b.setAttribute('aria-expanded', open ? 'false' : 'true'); });
  });
  doc.addEventListener('click', function (e) { if (!e.target.closest('.bb-group')) closeBottom(); });

  /* Brand carousel */
  $$('.carousel').forEach(function (car) {
    var track_ = $('.track', car), tiles = $$('.tile', track_), prev = $('.prev', car), nextB = $('.next', car), dotsWrap = $('.car-dots', car);
    if (!track_ || !tiles.length) return;
    tiles.forEach(function (_, i) {
      var b = doc.createElement('button'); b.type = 'button'; b.setAttribute('aria-label', 'Go to brand ' + (i + 1));
      b.addEventListener('click', function () { tiles[i].scrollIntoView({ behavior: reduce ? 'auto' : 'smooth', inline: 'start', block: 'nearest' }); });
      dotsWrap.appendChild(b);
    });
    var dotBtns = $$('button', dotsWrap);
    function update() {
      var left = track_.scrollLeft, best = 0, bd = Infinity;
      tiles.forEach(function (tl, i) { var d = Math.abs(tl.offsetLeft - track_.offsetLeft - left); if (d < bd) { bd = d; best = i; } });
      dotBtns.forEach(function (b, i) { b.setAttribute('aria-current', i === best ? 'true' : 'false'); });
    }
    track_.addEventListener('scroll', update, { passive: true }); update();
    function step(dir) { track_.scrollBy({ left: dir * (tiles[0].offsetWidth + 20), behavior: reduce ? 'auto' : 'smooth' }); }
    if (prev) prev.addEventListener('click', function () { step(-1); });
    if (nextB) nextB.addEventListener('click', function () { step(1); });
    /* Autoplay until the visitor touches it */
    var auto = null, userTouched = false;
    function autoplay() {
      if (reduce) return;
      clearInterval(auto);
      auto = setInterval(function () {
        if (doc.hidden || userTouched) return;
        var atEnd = track_.scrollLeft + track_.clientWidth >= track_.scrollWidth - 4;
        if (atEnd) track_.scrollTo({ left: 0, behavior: 'smooth' }); else step(1);
      }, 4200);
    }
    ['pointerdown', 'touchstart', 'keydown', 'wheel'].forEach(function (ev) { car.addEventListener(ev, function () { userTouched = true; clearInterval(auto); }, { passive: true }); });
    car.addEventListener('mouseenter', function () { clearInterval(auto); });
    car.addEventListener('mouseleave', function () { if (!userTouched) autoplay(); });
    if ('IntersectionObserver' in window) {
      new IntersectionObserver(function (en) { en.forEach(function (e) { if (e.isIntersecting && !userTouched) autoplay(); else clearInterval(auto); }); }, { threshold: 0.3 }).observe(car);
    } else autoplay();
  });

  /* Filters */
  $$('[data-filter-root]').forEach(function (rootEl) {
    var itemsEl = $$('[data-item]', rootEl), groups = $$('[data-group]', rootEl), search = $('[data-search]', rootEl);
    var note = $('[data-results]', rootEl), empty = $('[data-empty]', rootEl), clear = $('[data-clear]', rootEl);
    function apply() {
      var s = {}; $$('input[type="radio"]:checked', rootEl).forEach(function (r) { s[r.name] = r.value; });
      var q = search ? search.value.trim().toLowerCase() : '', shown = 0;
      itemsEl.forEach(function (el) {
        var ok = true;
        Object.keys(s).forEach(function (k) { var v = s[k]; if (!v || v === 'all') return; if ((el.getAttribute('data-' + k) || '').split(/\s+/).indexOf(v) === -1) ok = false; });
        if (ok && q) ok = (el.textContent || '').toLowerCase().indexOf(q) !== -1;
        el.classList.toggle('hidden', !ok); if (ok) shown++;
      });
      groups.forEach(function (g) { g.classList.toggle('hidden', !$$('[data-item]:not(.hidden)', g).length); });
      if (note) note.textContent = shown === itemsEl.length ? S('showing-all', { n: shown }) : S('showing', { a: shown, b: itemsEl.length });
      if (empty) empty.classList.toggle('hidden', shown > 0);
    }
    $$('input[type="radio"]', rootEl).forEach(function (r) { r.addEventListener('change', apply); });
    if (search) search.addEventListener('input', apply);
    if (clear) clear.addEventListener('click', function () { $$('input[type="radio"][value="all"]', rootEl).forEach(function (r) { r.checked = true; }); if (search) search.value = ''; apply(); });
    new URLSearchParams(location.search).forEach(function (v, k) { var r = $('input[name="' + k + '"][value="' + v + '"]', rootEl); if (r) r.checked = true; });
    apply();
  });

  /* Submission: POST to the configured endpoint, or fall back to the visitor's email app */
  function makeRef() {
    var d = new Date(), pad = function (n) { return (n < 10 ? '0' : '') + n; };
    var chars = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789', r = '';
    for (var i = 0; i < 4; i++) r += chars[Math.floor(Math.random() * chars.length)];
    return 'WW-' + String(d.getFullYear()).slice(2) + pad(d.getMonth() + 1) + pad(d.getDate()) + '-' + r;
  }
  function submitData(data) {
    if (!endpoint) return Promise.reject(new Error('no-endpoint'));
    var isGoogle = endpoint.indexOf('script.google.com') !== -1;
    var opts = isGoogle
      ? { method: 'POST', body: JSON.stringify(data), headers: { 'Content-Type': 'text/plain;charset=utf-8' } }
      : { method: 'POST', body: JSON.stringify(data), headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' } };
    return fetch(endpoint, opts).then(function (r) {
      if (!r.ok) throw new Error('http ' + r.status);
      return r.json().catch(function () { return { ok: true }; });
    }).then(function (j) {
      if (j && (j.ok === true || j.success === true || j.success === 'true' || j.status === 'ok')) return j;
      throw new Error('rejected');
    });
  }
  function mailtoFallback(subject, lines) {
    window.location.href = 'mailto:info@websaworldwide.com?subject=' + encodeURIComponent(subject) + '&body=' + encodeURIComponent(lines.join('\n'));
  }
  function markInvalid(form) {
    $$('.field', form).forEach(function (f) { var c = $('input, select, textarea', f); f.classList.toggle('invalid', !!(c && !c.checkValidity())); });
  }

  /* Contact form */
  var form = $('#enquiry');
  if (form) {
    var msg = $('.form-msg', form);
    if (endpoint) { var nm = $('[data-note-mail]', form), np = $('[data-note-post]', form); if (nm) nm.hidden = true; if (np) np.hidden = false; }
    var pre = new URLSearchParams(location.search).get('type'), sel = $('#f-type');
    if (pre && sel) for (var i = 0; i < sel.options.length; i++) if (sel.options[i].text === pre) { sel.selectedIndex = i; break; }
    form.addEventListener('submit', function (e) {
      e.preventDefault(); msg.className = 'form-msg'; markInvalid(form);
      if (!form.checkValidity()) { form.reportValidity(); return; }
      var f = new FormData(form), type = f.get('type'), ref = makeRef();
      var data = { form: 'contact', ref: ref, lang: lang, page: pageTitle, name: f.get('name'), company: f.get('company'), country: f.get('country'), email: f.get('email'), phone: f.get('phone'), type: type, message: f.get('message'), submitted: new Date().toISOString() };
      var btn = $('button[type="submit"]', form); btn.disabled = true;
      submitData(data).then(function () {
        msg.textContent = S('form-ok', { r: ref }); msg.className = 'form-msg ok'; form.reset(); track('enquiry_submit', { type: type });
      }).catch(function (err) {
        if (err.message === 'no-endpoint') {
          mailtoFallback('[' + type + '] Enquiry from ' + data.name + (data.company ? ' at ' + data.company : '') + ' (' + ref + ')',
            ['Reference: ' + ref, 'Name: ' + data.name, 'Company: ' + (data.company || 'n/a'), 'Country: ' + data.country, 'Email: ' + data.email, 'Phone / WhatsApp: ' + (data.phone || 'n/a'), 'Enquiry type: ' + type, '', data.message]);
          msg.textContent = S('form-mail'); msg.className = 'form-msg ok'; track('enquiry_mailto', { type: type });
        } else { msg.textContent = S('form-err'); msg.className = 'form-msg err'; }
      }).then(function () { btn.disabled = false; });
    });
    var wa = $('#wa-prefill');
    if (wa) form.addEventListener('input', function () {
      var f = new FormData(form); var extra = (f.get('name') ? 'My name is ' + f.get('name') + '. ' : '') + (f.get('message') || '');
      wa.href = 'https://wa.me/8617324010515?text=' + encodeURIComponent(waText(extra));
    });
  }

  /* Quote wizard */
  var wiz = $('#quote');
  if (wiz) {
    var steps = $$('.wstep', wiz), cur = 0, prevB = $('[data-prev]', wiz), nextB2 = $('[data-next]', wiz), subB = $('[data-submit]', wiz);
    var bar = $('.progress span', wiz), label = $('[data-step-label]', wiz), wmsg = $('.form-msg', wiz), review = $('[data-review]', wiz), done = $('[data-done]', wiz);
    var params = new URLSearchParams(location.search);
    if (params.get('brand')) { $('#q-brand').value = params.get('brand'); }
    if (params.get('type')) { var qt = $('#q-type'); for (var j = 0; j < qt.options.length; j++) if (qt.options[j].text === params.get('type')) qt.selectedIndex = j; }
    var draft = store('ww-quote-draft');
    if (draft) { try { var d = JSON.parse(draft); Object.keys(d).forEach(function (k) { var el = wiz.elements[k]; if (!el || k === 'consent') return; if (el.type === 'radio' || (el.length && el[0] && el[0].type === 'radio')) { var r = $('input[name="' + k + '"][value="' + d[k] + '"]', wiz); if (r) r.checked = true; } else el.value = d[k]; }); } catch (e) {} }
    function saveDraft() { var o = {}; new FormData(wiz).forEach(function (v, k) { if (k !== 'consent') o[k] = v; }); store('ww-quote-draft', JSON.stringify(o)); }
    wiz.addEventListener('input', saveDraft); wiz.addEventListener('change', saveDraft);
    function labelFor(name) { var el = wiz.elements[name]; var node = el.length && !el.tagName ? el[0] : el; var f = node.closest('.field'); var l = f ? $('label', f) : null; return l ? l.textContent.replace(/\s*\(optional\)/i, '') : name; }
    function fillReview() {
      var dl = $('.review-list', review), f = new FormData(wiz), rows = [];
      var catInput = $('input[name="category"]:checked', wiz);
      rows.push(['Category', catInput ? $('strong', catInput.closest('.choice')).textContent : '']);
      ['description', 'quantity', 'unit', 'budget', 'link', 'specs', 'country', 'city', 'delivery', 'timeline'].forEach(function (k) { if (f.get(k)) rows.push([labelFor(k), f.get(k)]); });
      dl.innerHTML = rows.map(function (r) { return '<dt>' + esc(r[0]) + '</dt><dd>' + esc(r[1]) + '</dd>'; }).join('');
      review.hidden = false;
    }
    function go(n) {
      steps[cur].hidden = true; cur = n; steps[cur].hidden = false;
      bar.style.width = ((cur + 1) / steps.length * 100) + '%';
      label.textContent = S('step', { a: cur + 1, b: steps.length });
      prevB.hidden = cur === 0; nextB2.hidden = cur === steps.length - 1; subB.hidden = cur !== steps.length - 1;
      if (cur === steps.length - 1) fillReview();
      wmsg.className = 'form-msg';
      var h = $('h2', steps[cur]); if (h) { h.setAttribute('tabindex', '-1'); h.focus({ preventScroll: true }); }
      wiz.scrollIntoView({ behavior: reduce ? 'auto' : 'smooth', block: 'start' });
      track('quote_step', { step: cur + 1 });
    }
    function stepValid() {
      var ok = true;
      $$('input, select, textarea', steps[cur]).forEach(function (c) { if (!c.checkValidity()) { ok = false; var f = c.closest('.field'); if (f) f.classList.add('invalid'); } else { var g = c.closest('.field'); if (g) g.classList.remove('invalid'); } });
      if (!ok) { wmsg.textContent = S('required'); wmsg.className = 'form-msg err'; var first = $$('input, select, textarea', steps[cur]).filter(function (c) { return !c.checkValidity(); })[0]; if (first) first.focus(); }
      return ok;
    }
    nextB2.addEventListener('click', function () { if (stepValid()) go(cur + 1); });
    prevB.addEventListener('click', function () { go(cur - 1); });
    wiz.addEventListener('submit', function (e) {
      e.preventDefault(); if (!stepValid()) return;
      var f = new FormData(wiz), ref = makeRef(), data = { form: 'quote', ref: ref, lang: lang, submitted: new Date().toISOString() };
      f.forEach(function (v, k) { data[k] = v; });
      var catInput = $('input[name="category"]:checked', wiz); data.category_label = catInput ? $('strong', catInput.closest('.choice')).textContent : '';
      subB.disabled = true;
      function finish(viaMail) {
        $$('.wstep, .wnav, .progress, .step-label', wiz).forEach(function (el) { el.hidden = true; });
        $('[data-ref]', done).textContent = ref;
        var waRef = $('[data-wa-ref]', done); if (waRef) waRef.href = 'https://wa.me/8617324010515?text=' + encodeURIComponent(S('wa-hello') + ' ' + S('wa-ref', { r: ref }));
        done.hidden = false; store('ww-quote-draft', null); track(viaMail ? 'quote_mailto' : 'quote_submit', { category: data.category, country: data.country });
        var h = $('h2', done); if (h) { h.setAttribute('tabindex', '-1'); h.focus(); }
      }
      submitData(data).then(function () { finish(false); }).catch(function (err) {
        if (err.message === 'no-endpoint') {
          var lines = ['Reference: ' + ref, 'Category: ' + data.category_label, 'Description: ' + data.description, 'Quantity: ' + data.quantity + ' ' + data.unit, 'Budget: ' + (data.budget || 'n/a'), 'Link: ' + (data.link || 'n/a'), 'Specs: ' + (data.specs || 'n/a'), 'Destination: ' + data.city + ', ' + data.country, 'Delivery: ' + data.delivery, 'Timeline: ' + data.timeline, '', 'Name: ' + data.name, 'Company: ' + (data.company || 'n/a'), 'Email: ' + data.email, 'Phone: ' + data.phone, 'Type: ' + data.type, 'Brand: ' + (data.brand || 'n/a'), 'Heard via: ' + (data.heard || 'n/a')];
          mailtoFallback('[' + data.type + '] Quotation request ' + ref + ' from ' + data.name, lines); finish(true);
        } else { wmsg.textContent = S('form-err'); wmsg.className = 'form-msg err'; subB.disabled = false; }
      });
    });
    bar.style.width = (1 / steps.length * 100) + '%';
  }

  /* Reveal on scroll */
  var toReveal = $$('.reveal');
  if ('IntersectionObserver' in window && !reduce) {
    var io = new IntersectionObserver(function (entries) { entries.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); } }); }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
    toReveal.forEach(function (el) { io.observe(el); });
    setTimeout(function () { toReveal.forEach(function (el) { el.classList.add('in'); }); }, 4000);
  } else { toReveal.forEach(function (el) { el.classList.add('in'); }); }

  $$('[data-year]').forEach(function (el) { el.textContent = new Date().getFullYear(); });

  /* Current nav item */
  var path = location.pathname.split('/').pop() || 'index.html';
  $$('.nav a, .menu a').forEach(function (a) {
    if ((a.getAttribute('href') || '').split('#')[0].split('?')[0] === path) {
      a.setAttribute('aria-current', 'page'); var li = a.closest('.nav > li'); if (li) { var top = $('.nav-link', li); if (top) top.classList.add('is-current'); }
    }
  });
})();
