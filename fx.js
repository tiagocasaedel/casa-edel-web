/* Casa Edel · capa de efectos (prueba). Solo agrega comportamiento visual; no cambia cómo funciona la página. */
(function () {
  var REDUCE = matchMedia('(prefers-reduced-motion: reduce)').matches;
  var FINE = matchMedia('(hover: hover) and (pointer: fine)').matches;
  var $ = function (s, r) { return (r || document).querySelector(s); };

  /* barra de progreso al bajar */
  var bar = document.createElement('div'); bar.className = 'fx-progress'; bar.setAttribute('aria-hidden', 'true'); document.body.appendChild(bar);
  var ticking = false;
  function onScroll() {
    if (ticking) return; ticking = true;
    requestAnimationFrame(function () {
      var h = document.documentElement.scrollHeight - innerHeight;
      bar.style.setProperty('--p', h > 0 ? Math.min(1, scrollY / h) : 0);
      ticking = false;
    });
  }
  addEventListener('scroll', onScroll, { passive: true }); onScroll();

  /* encabezado: el brillo del vidrio sigue al mouse */
  var top = $('header.top');
  if (top && FINE) top.addEventListener('pointermove', function (e) {
    var r = top.getBoundingClientRect(); top.style.setProperty('--mx', ((e.clientX - r.left) / r.width * 100).toFixed(1) + '%');
  });

  /* menú: burbuja líquida que se desliza debajo del link señalado */
  var nav = $('.nav');
  if (nav) {
    var blob = document.createElement('span'); blob.className = 'fx-blob'; blob.setAttribute('aria-hidden', 'true'); nav.prepend(blob);
    var items = nav.querySelectorAll(':scope > a, .has-mega > button');
    function moveTo(el) {
      var n = nav.getBoundingClientRect(), r = el.getBoundingClientRect();
      blob.style.width = r.width + 'px'; blob.style.height = r.height + 'px';
      blob.style.transform = 'translate(' + (r.left - n.left) + 'px,' + (r.top - n.top) + 'px)';
      blob.classList.add('on');
    }
    items.forEach(function (el) { el.addEventListener('pointerenter', function () { moveTo(el); }); el.addEventListener('focus', function () { moveTo(el); }); });
    nav.addEventListener('pointerleave', function () { blob.classList.remove('on'); });
  }

  /* botones: onda al tocar */
  document.addEventListener('pointerdown', function (e) {
    var b = e.target.closest && e.target.closest('.hx-cta,.hx-wa,.btn,.add,.cart-btn,.qall,#barBtn,.menu-btn,.chip');
    if (!b || REDUCE) return;
    var r = b.getBoundingClientRect(), s = Math.max(r.width, r.height) * 2.4, w = document.createElement('span');
    w.className = 'fx-ripple'; w.style.width = w.style.height = s + 'px';
    w.style.left = (e.clientX - r.left) + 'px'; w.style.top = (e.clientY - r.top) + 'px';
    b.appendChild(w); setTimeout(function () { w.remove(); }, 700);
  }, { passive: true });

  if (REDUCE) return;

  /* tarjetas: inclinación 3D y reflejo (solo con mouse) */
  if (FINE) {
    var cur = null;
    document.addEventListener('pointermove', function (e) {
      var t = e.target.closest && e.target.closest('.card .tile, .rubro .tile, .job, .fl button');
      if (t !== cur) {
        if (cur) { cur.classList.remove('fx-hot'); cur.style.transform = ''; }
        cur = t;
        if (t) {
          t.classList.add('fx-tilt', 'fx-hot');
          if (!t.querySelector(':scope > .fx-glare')) { var g = document.createElement('span'); g.className = 'fx-glare'; t.appendChild(g); }
        }
      }
      if (!t) return;
      var r = t.getBoundingClientRect(), x = (e.clientX - r.left) / r.width, y = (e.clientY - r.top) / r.height;
      var k = t.classList.contains('job') ? 5 : 9;
      t.style.transform = 'perspective(800px) rotateX(' + ((.5 - y) * k).toFixed(2) + 'deg) rotateY(' + ((x - .5) * k).toFixed(2) + 'deg) scale(1.025)';
      t.style.setProperty('--gx', (x * 100).toFixed(1) + '%'); t.style.setProperty('--gy', (y * 100).toFixed(1) + '%');
    }, { passive: true });
    document.addEventListener('pointerleave', function () { if (cur) { cur.classList.remove('fx-hot'); cur.style.transform = ''; cur = null; } });

    /* halo eléctrico que sigue al mouse sobre las secciones oscuras */
    var halo = document.createElement('div'); halo.className = 'fx-halo'; halo.setAttribute('aria-hidden', 'true'); document.body.appendChild(halo);
    var hx = 0, hy = 0, tx = 0, ty = 0, run = false;
    function loop() { hx += (tx - hx) * .14; hy += (ty - hy) * .14; halo.style.transform = 'translate(' + hx + 'px,' + hy + 'px)'; if (Math.abs(tx - hx) + Math.abs(ty - hy) > .5) requestAnimationFrame(loop); else run = false; }
    document.addEventListener('pointermove', function (e) {
      tx = e.clientX; ty = e.clientY;
      var dark = e.target.closest && e.target.closest('.hx, .t-navy, footer, header.top, .jobs-sec');
      halo.classList.toggle('on', !!dark);
      if (!run) { run = true; requestAnimationFrame(loop); }
    }, { passive: true });
  }

  /* títulos y bloques que entran con desenfoque al aparecer */
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('fx-in'); io.unobserve(e.target); } });
    }, { rootMargin: '0px 0px -10% 0px' });
    document.querySelectorAll('.cat-head, .nv-head, .jobs-head, .contact .wrap > *').forEach(function (el) {
      if (el.getBoundingClientRect().top > innerHeight) io.observe(el);
    });
  }
})();
