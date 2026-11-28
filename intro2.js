/* Casa Edel · intro v2 (prueba): el logo se carga de electricidad, se vuelve un rayo
   y la web aparece desde una burbuja de vidrio líquido.
   Una vez por visita (sessionStorage). Se salta tocando la pantalla. Respeta "reducir movimiento". */
(function () {
  var KEY = 'ce-intro2', FORCE = /[?&]intro\b/.test(location.search);
  if (!FORCE) { try { if (sessionStorage.getItem(KEY)) return; sessionStorage.setItem(KEY, '1'); } catch (e) {} }
  var REDUCE = matchMedia('(prefers-reduced-motion: reduce)').matches;
  document.documentElement.classList.add('intro2-on');

  var css = [
    '#ce2{position:fixed;inset:0;z-index:2147483000;display:grid;place-items:center;cursor:pointer;-webkit-tap-highlight-color:transparent}',
    '#ce2 .bg{position:absolute;inset:0;background:radial-gradient(120% 90% at 50% 45%,#122063 0%,#070d33 55%,#03061c 100%)}',
    '#ce2 .grid{position:absolute;inset:-10%;opacity:.18;background-image:linear-gradient(rgba(255,255,255,.08) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.08) 1px,transparent 1px);background-size:48px 48px;-webkit-mask:radial-gradient(60% 50% at 50% 50%,#000,transparent);mask:radial-gradient(60% 50% at 50% 50%,#000,transparent);animation:ce2-grid 3s linear both}',
    '#ce2 .logo{position:relative;width:min(70vw,520px);aspect-ratio:541/143;animation:ce2-in .9s cubic-bezier(.2,.9,.2,1) both, ce2-charge .55s .95s ease-in both, ce2-squeeze .32s 1.5s cubic-bezier(.6,0,.9,.4) forwards}',
    '#ce2 .logo img{width:100%;height:100%;display:block;filter:drop-shadow(0 6px 30px rgba(211,49,42,.45))}',
    '#ce2 .logo .sheen{position:absolute;inset:0;-webkit-mask:url(img/logo-light.png) center/100% 100% no-repeat;mask:url(img/logo-light.png) center/100% 100% no-repeat;background:linear-gradient(105deg,transparent 35%,rgba(255,255,255,.95) 48%,rgba(255,240,170,.9) 52%,transparent 65%) -150% 0/250% 100% no-repeat;animation:ce2-sheen .9s .55s ease-in-out both}',
    '#ce2 svg.arcs{position:absolute;inset:-30% -12%;width:124%;height:160%;overflow:visible;opacity:0;animation:ce2-arcs .7s .9s steps(1) both}',
    '#ce2 svg.arcs path{fill:none;stroke:#bfe2ff;stroke-width:2;stroke-linecap:round;stroke-linejoin:round;filter:drop-shadow(0 0 6px #6fb8ff) drop-shadow(0 0 14px #2f7bff)}',
    '#ce2 .bolt{position:absolute;width:min(22vw,120px);aspect-ratio:100/160;opacity:0;transform:scale(.2) rotate(-8deg);animation:ce2-bolt .55s 1.72s cubic-bezier(.2,1.4,.4,1) both, ce2-boltout .28s 2.32s cubic-bezier(.7,0,.9,.3) forwards}',
    '#ce2 .bolt svg{width:100%;height:100%;overflow:visible;filter:drop-shadow(0 0 18px rgba(255,210,63,.9)) drop-shadow(0 0 50px rgba(211,49,42,.8))}',
    '#ce2 .flash{position:absolute;inset:0;background:radial-gradient(circle at 50% 50%,rgba(255,250,220,.95),rgba(255,210,63,.35) 18%,transparent 45%);opacity:0;animation:ce2-flash .5s 1.72s ease-out both}',
    '#ce2 .dot{position:absolute;width:18px;height:18px;border-radius:50%;background:#fff;box-shadow:0 0 30px 10px rgba(255,220,120,.9),0 0 80px 30px rgba(211,49,42,.6);opacity:0;transform:scale(0);animation:ce2-dot .3s 2.45s cubic-bezier(.2,1.6,.4,1) both}',
    '#ce2 .ring{position:absolute;left:50%;top:50%;width:0;height:0;border-radius:50%;pointer-events:none;transform:translate(-50%,-50%);',
    '  box-shadow:inset 0 0 0 2px rgba(255,255,255,.75),inset 0 10px 30px rgba(255,255,255,.35),inset 0 -12px 30px rgba(120,180,255,.35),0 0 0 1px rgba(255,255,255,.25),0 20px 80px rgba(0,0,0,.25);',
    '  background:radial-gradient(closest-side,transparent 86%,rgba(255,255,255,.18) 93%,rgba(255,255,255,.55) 99%,transparent 100%);',
    '  -webkit-backdrop-filter:blur(2px) saturate(170%);backdrop-filter:blur(2px) saturate(170%)}',
    '#ce2 .ring::before{content:"";position:absolute;left:14%;top:7%;width:34%;height:14%;border-radius:50%;background:linear-gradient(180deg,rgba(255,255,255,.85),rgba(255,255,255,0));transform:rotate(-24deg);filter:blur(1px)}',
    '#ce2 .skip{position:absolute;right:max(18px,env(safe-area-inset-right));bottom:max(18px,env(safe-area-inset-bottom));font:600 13px/1 system-ui,sans-serif;letter-spacing:.06em;text-transform:uppercase;color:rgba(255,255,255,.8);background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.2);border-radius:999px;padding:10px 16px;-webkit-backdrop-filter:blur(10px);backdrop-filter:blur(10px);animation:ce2-fade .5s .4s both}',
    '#ce2.popping .bg,#ce2.popping .grid,#ce2.popping .flash{transition:none}',
    'html.intro2-on body{overflow:hidden}',
    'html.intro2-pop,html.intro2-pop body{background:#050a28}',
    'html.intro2-pop main,html.intro2-pop footer{animation:ce2-page .9s cubic-bezier(.2,1.25,.35,1) both;transform-origin:50% 0}',
    'html.intro2-pop header.top{animation:ce2-head .7s ease-out both}',
    '@keyframes ce2-head{from{opacity:0;filter:blur(8px)}}',
    '@keyframes ce2-grid{from{transform:scale(1.15)}to{transform:scale(1)}}',
    '@keyframes ce2-in{from{opacity:0;transform:scale(.86) translateY(10px);filter:blur(14px)}to{opacity:1;transform:none;filter:none}}',
    '@keyframes ce2-sheen{to{background-position:150% 0}}',
    '@keyframes ce2-charge{0%,100%{transform:none}20%{transform:translate(-2px,1px) skewX(-2deg)}40%{transform:translate(2px,-1px)}60%{transform:translate(-1px,-1px) skewX(2deg)}80%{transform:translate(1px,1px)}}',
    '@keyframes ce2-squeeze{0%{transform:none;opacity:1;filter:none}60%{transform:scale(.18,1.08);filter:brightness(2.4) blur(1px)}100%{transform:scale(.02,1.3);opacity:0;filter:brightness(4) blur(4px)}}',
    '@keyframes ce2-arcs{0%{opacity:1}15%{opacity:.2}30%{opacity:1}45%{opacity:0}55%{opacity:1}75%{opacity:.3}90%{opacity:1}100%{opacity:0}}',
    '@keyframes ce2-bolt{from{opacity:0;transform:scale(.2) rotate(-8deg)}to{opacity:1;transform:none}}',
    '@keyframes ce2-boltout{to{opacity:0;transform:scale(.05,.4);filter:brightness(3)}}',
    '@keyframes ce2-flash{0%{opacity:0}15%{opacity:1}100%{opacity:0}}',
    '@keyframes ce2-dot{to{opacity:1;transform:scale(1)}}',
    '@keyframes ce2-fade{from{opacity:0}}',
    '@keyframes ce2-page{from{transform:scale(.94);filter:blur(6px);opacity:.4}to{transform:none;filter:none;opacity:1}}',
    '@media (prefers-reduced-motion:reduce){#ce2 *{animation-duration:.01s!important;animation-delay:0s!important}}'
  ].join('\n');

  // un rayo con la forma del logo (rojo con borde amarillo)
  var BOLT = 'M58 2 L16 92 H46 L32 158 L86 58 H54 L74 2 Z';
  function arc(x0, y0, x1, y1, n) {
    var d = 'M' + x0 + ' ' + y0, i;
    for (i = 1; i < n; i++) {
      var t = i / n, x = x0 + (x1 - x0) * t + (Math.random() - .5) * 28, y = y0 + (y1 - y0) * t + (Math.random() - .5) * 28;
      d += ' L' + x.toFixed(1) + ' ' + y.toFixed(1);
    }
    return d + ' L' + x1 + ' ' + y1;
  }
  var arcs = '';
  [[-10, 40, 120, 70], [600, 20, 470, 90], [80, 180, 260, 120], [560, 190, 400, 130], [300, -20, 330, 60], [250, 220, 280, 150]].forEach(function (a) { arcs += '<path d="' + arc(a[0], a[1], a[2], a[3], 7) + '"/>'; });

  var html = '<div class="bg"></div><div class="grid"></div><div class="flash"></div>' +
    '<div class="logo"><img src="img/logo-light.png" alt="" width="541" height="143"><div class="sheen"></div>' +
    '<svg class="arcs" viewBox="0 0 600 200" preserveAspectRatio="none" aria-hidden="true">' + arcs + '</svg></div>' +
    '<div class="bolt"><svg viewBox="0 0 100 160" aria-hidden="true"><path d="' + BOLT + '" fill="#ffd23f" transform="translate(4 4)" opacity=".9"/>' +
    '<path d="' + BOLT + '" fill="#d3312a" stroke="#ffe48a" stroke-width="2.5" stroke-linejoin="round"/>' +
    '<path d="M60 10 L22 86" stroke="rgba(255,255,255,.55)" stroke-width="4" stroke-linecap="round"/></svg></div>' +
    '<div class="dot"></div><div class="ring"></div><button class="skip" type="button">Saltar</button>';

  function mount() {
    var st = document.createElement('style'); st.textContent = css; document.head.appendChild(st);
    var el = document.createElement('div'); el.id = 'ce2'; el.setAttribute('role', 'img'); el.setAttribute('aria-label', 'Electricidad Casa Edel');
    el.innerHTML = html; document.body.appendChild(el);
    var ring = el.querySelector('.ring'), root = document.documentElement, done = false, popping = false;

    function finish() {
      if (done) return; done = true;
      el.remove(); root.classList.remove('intro2-on');
      setTimeout(function () { root.classList.remove('intro2-pop'); st.remove(); }, 1000);
    }
    // la burbuja: un agujero circular que crece en la capa de la intro, con un borde de vidrio
    function pop() {
      if (popping) return; popping = true;
      el.classList.add('popping'); root.classList.add('intro2-pop');
      var W = innerWidth, H = innerHeight, R = Math.hypot(W, H) / 2 + 40, t0 = performance.now(), D = REDUCE ? 1 : 900;
      function ease(t) { var c = 1.35; return 1 + (c + 1) * Math.pow(t - 1, 3) + c * Math.pow(t - 1, 2); } // easeOutBack
      function frame(now) {
        var t = Math.min(1, (now - t0) / D), r = Math.max(0, ease(t) * R);
        var m = 'radial-gradient(circle at 50% 50%,transparent ' + r + 'px,#000 ' + (r + 1.5) + 'px)';
        el.style.webkitMaskImage = m; el.style.maskImage = m;
        ring.style.width = ring.style.height = (r * 2 + 6) + 'px';
        ring.style.opacity = t < .8 ? 1 : (1 - t) * 5;
        if (t < 1) requestAnimationFrame(frame); else finish();
      }
      requestAnimationFrame(frame);
    }
    el.addEventListener('click', function () { el.querySelectorAll('.logo,.bolt,.dot,.flash').forEach(function (n) { n.style.opacity = 0; }); pop(); });
    var minT = REDUCE ? 300 : 2650, t0 = performance.now();
    function go() { setTimeout(pop, Math.max(0, minT - (performance.now() - t0))); }
    if (document.readyState === 'complete') go(); else addEventListener('load', go, { once: true });
    setTimeout(pop, 6000); // por si la página tarda en cargar
  }
  if (document.body) mount(); else document.addEventListener('DOMContentLoaded', mount, { once: true });
})();
