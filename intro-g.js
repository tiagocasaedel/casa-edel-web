(function () {
  "use strict";

  var STORAGE_KEY = "casa_edel_intro_v1_seen";
  var LOGO_SRC = "img/logo-light.png";
  var TOTAL_DURATION_MS = 3000; // Entre 2.5s y 3.5s
  var MIN_EXIT_MS = 2600;
  var MAX_WAIT_MS = 6000;
  var REDUCED_MOTION_MS = 850;

  try {
    if (window.sessionStorage && window.sessionStorage.getItem(STORAGE_KEY)) {
      return;
    }
    if (window.sessionStorage) {
      window.sessionStorage.setItem(STORAGE_KEY, "1");
    }
  } catch (e) {
    // Continuar aunque sessionStorage esté restringido
  }

  // la página todavía no tiene <body> cuando corre este script: se tapa hasta montar la intro
  var preStyle = document.createElement("style");
  preStyle.textContent = "html{background:#050a28}body>:not(#casa-edel-intro){visibility:hidden}";
  document.head.appendChild(preStyle);

  function init() {
  var prefersReducedMotion = false;
  try {
    prefersReducedMotion =
      window.matchMedia &&
      window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  } catch (e) {
    prefersReducedMotion = false;
  }

  var prevOverflow = document.documentElement.style.overflow;
  var prevBodyOverflow = document.body ? document.body.style.overflow : "";
  var prevTouchAction = document.body ? document.body.style.touchAction : "";

  function lockScroll() {
    document.documentElement.style.overflow = "hidden";
    if (document.body) {
      document.body.style.overflow = "hidden";
      document.body.style.touchAction = "none";
    }
  }

  function unlockScroll() {
    document.documentElement.style.overflow = prevOverflow;
    if (document.body) {
      document.body.style.overflow = prevBodyOverflow;
      document.body.style.touchAction = prevTouchAction;
    }
  }

  var styleEl = document.createElement("style");
  styleEl.setAttribute("data-casa-edel-intro-style", "true");
  styleEl.textContent = [
    "#casa-edel-intro{",
    "  position:fixed;",
    "  inset:0;",
    "  width:100vw;",
    "  height:100vh;",
    "  height:100dvh;",
    "  z-index:2147483647;",
    "  background:#050a28;",
    "  display:flex;",
    "  align-items:center;",
    "  justify-content:center;",
    "  overflow:hidden;",
    "  cursor:pointer;",
    "  user-select:none;",
    "  -webkit-tap-highlight-color:transparent;",
    "  opacity:1;",
    "  transition:opacity 420ms cubic-bezier(0.22,1,0.36,1),transform 420ms cubic-bezier(0.22,1,0.36,1);",
    "  will-change:opacity,transform;",
    "}",
    "#casa-edel-intro.is-leaving{",
    "  opacity:0;",
    "  transform:scale(1.04);",
    "  pointer-events:none;",
    "}",
    "#casa-edel-intro .ce-ambient{",
    "  position:absolute;",
    "  width:min(78vw,680px);",
    "  height:min(78vw,680px);",
    "  border-radius:50%;",
    "  background:radial-gradient(circle,rgba(27,43,110,0.62) 0%,rgba(27,43,110,0.18) 45%,rgba(5,10,40,0) 72%);",
    "  filter:blur(12px);",
    "  transform:translateZ(0) scale(0.85);",
    "  opacity:0.5;",
    "  animation:ceAmbientPulse 3000ms ease-in-out forwards;",
    "  pointer-events:none;",
    "}",
    "#casa-edel-intro .ce-stage{",
    "  position:relative;",
    "  width:min(88vw,560px);",
    "  max-height:70vh;",
    "  display:flex;",
    "  align-items:center;",
    "  justify-content:center;",
    "  transform:translateZ(0);",
    "}",
    "#casa-edel-intro .ce-logo-wrap{",
    "  position:relative;",
    "  width:100%;",
    "  display:flex;",
    "  align-items:center;",
    "  justify-content:center;",
    "  opacity:0;",
    "  transform:scale(0.84) translateY(10px);",
    "  animation:ceLogoImpact 2950ms cubic-bezier(0.16,1,0.3,1) forwards;",
    "  will-change:transform,opacity,filter;",
    "}",
    "#casa-edel-intro .ce-logo{",
    "  display:block;",
    "  width:100%;",
    "  max-width:520px;",
    "  height:auto;",
    "  max-height:240px;",
    "  object-fit:contain;",
    "  filter:drop-shadow(0 0 0 rgba(255,210,63,0));",
    "  animation:ceChargeGlow 2950ms ease-in-out forwards;",
    "}",
    "#casa-edel-intro .ce-sweep{",
    "  position:absolute;",
    "  top:-15%;",
    "  bottom:-15%;",
    "  width:28%;",
    "  left:-35%;",
    "  background:linear-gradient(90deg,transparent 0%,rgba(250,246,238,0.15) 30%,rgba(255,210,63,0.75) 52%,rgba(211,49,42,0.35) 75%,transparent 100%);",
    "  transform:skewX(-22deg) translateZ(0);",
    "  filter:blur(4px);",
    "  opacity:0;",
    "  mix-blend-mode:screen;",
    "  pointer-events:none;",
    "  animation:ceCurrentSweep 1200ms cubic-bezier(0.2,0.8,0.2,1) 650ms forwards;",
    "}",
    "#casa-edel-intro .ce-bolt-svg{",
    "  position:absolute;",
    "  width:min(64vw,320px);",
    "  height:min(64vw,320px);",
    "  opacity:0;",
    "  transform:scale(0.55) rotate(-14deg) translateZ(0);",
    "  filter:drop-shadow(0 0 18px rgba(255,210,63,0.9)) drop-shadow(0 0 38px rgba(211,49,42,0.55));",
    "  pointer-events:none;",
    "  animation:ceBoltStrike 1150ms cubic-bezier(0.14,0.92,0.24,1) 1850ms forwards;",
    "  will-change:transform,opacity;",
    "}",
    "#casa-edel-intro .ce-flash{",
    "  position:fixed;",
    "  inset:0;",
    "  background:radial-gradient(circle at center,rgba(250,246,238,0.95) 0%,rgba(255,210,63,0.65) 32%,rgba(211,49,42,0.2) 62%,rgba(5,10,40,0) 85%);",
    "  opacity:0;",
    "  pointer-events:none;",
    "  animation:ceFlashBurst 680ms ease-out 2280ms forwards;",
    "}",
    "#casa-edel-intro .ce-sparks{",
    "  position:absolute;",
    "  inset:-20%;",
    "  pointer-events:none;",
    "}",
    "#casa-edel-intro .ce-spark{",
    "  position:absolute;",
    "  left:50%;",
    "  top:50%;",
    "  width:var(--s,5px);",
    "  height:var(--s,5px);",
    "  border-radius:999px;",
    "  background:var(--c,#ffd23f);",
    "  box-shadow:0 0 10px var(--c,#ffd23f);",
    "  opacity:0;",
    "  transform:translate(-50%,-50%) scale(0.3);",
    "  animation:ceSparkFly var(--d,750ms) cubic-bezier(0.16,1,0.3,1) var(--delay,400ms) forwards;",
    "  will-change:transform,opacity;",
    "}",
    "#casa-edel-intro .ce-skip{",
    "  position:fixed;",
    "  top:max(14px,env(safe-area-inset-top));",
    "  right:max(14px,env(safe-area-inset-right));",
    "  z-index:2;",
    "  padding:6px 12px;",
    "  font-family:system-ui,-apple-system,Segoe UI,Roboto,sans-serif;",
    "  font-size:12px;",
    "  font-weight:600;",
    "  letter-spacing:0.06em;",
    "  text-transform:uppercase;",
    "  color:rgba(250,246,238,0.78);",
    "  background:rgba(27,43,110,0.45);",
    "  border:1px solid rgba(250,246,238,0.2);",
    "  border-radius:999px;",
    "  cursor:pointer;",
    "  transition:background-color 180ms ease,color 180ms ease;",
    "}",
    "#casa-edel-intro .ce-skip:hover,",
    "#casa-edel-intro .ce-skip:focus-visible{",
    "  background:rgba(211,49,42,0.85);",
    "  color:#faf6ee;",
    "  outline:none;",
    "}",
    "@keyframes ceAmbientPulse{",
    "  0%{opacity:0.35;transform:scale(0.8);}",
    "  55%{opacity:0.95;transform:scale(1.08);}",
    "  80%{opacity:1;transform:scale(1.18);}",
    "  100%{opacity:0.65;transform:scale(1.25);}",
    "}",
    "@keyframes ceLogoImpact{",
    "  0%{opacity:0;transform:scale(0.8) translateY(14px);}",
    "  16%{opacity:1;transform:scale(1.03) translateY(0);}",
    "  24%{transform:scale(0.99) translateY(0);}",
    "  68%{opacity:1;transform:scale(1.02) translateY(0);}",
    "  82%{opacity:0.25;transform:scale(1.12) translateY(-4px);}",
    "  100%{opacity:0;transform:scale(1.22) translateY(-8px);}",
    "}",
    "@keyframes ceChargeGlow{",
    "  0%{filter:drop-shadow(0 0 0 rgba(255,210,63,0));}",
    "  35%{filter:drop-shadow(0 0 12px rgba(255,210,63,0.45)) drop-shadow(0 0 24px rgba(211,49,42,0.25));}",
    "  68%{filter:drop-shadow(0 0 22px rgba(255,210,63,0.85)) drop-shadow(0 0 42px rgba(250,246,238,0.45));}",
    "  100%{filter:drop-shadow(0 0 32px rgba(255,210,63,1));}",
    "}",
    "@keyframes ceCurrentSweep{",
    "  0%{left:-35%;opacity:0;}",
    "  20%{opacity:0.95;}",
    "  80%{opacity:0.85;}",
    "  100%{left:125%;opacity:0;}",
    "}",
    "@keyframes ceBoltStrike{",
    "  0%{opacity:0;transform:scale(0.45) rotate(-18deg);}",
    "  25%{opacity:1;transform:scale(1.14) rotate(4deg);}",
    "  45%{opacity:1;transform:scale(1) rotate(0deg);}",
    "  75%{opacity:1;transform:scale(1.08) rotate(0deg);}",
    "  100%{opacity:0;transform:scale(1.45) rotate(6deg);}",
    "}",
    "@keyframes ceFlashBurst{",
    "  0%{opacity:0;}",
    "  25%{opacity:0.9;}",
    "  100%{opacity:0;}",
    "}",
    "@keyframes ceSparkFly{",
    "  0%{opacity:0;transform:translate(-50%,-50%) scale(0.3);}",
    "  18%{opacity:1;}",
    "  100%{opacity:0;transform:translate(calc(-50% + var(--tx,80px)),calc(-50% + var(--ty,-60px))) scale(0.1);}",
    "}",
    "#casa-edel-intro.is-reduced .ce-ambient,",
    "#casa-edel-intro.is-reduced .ce-sweep,",
    "#casa-edel-intro.is-reduced .ce-bolt-svg,",
    "#casa-edel-intro.is-reduced .ce-flash,",
    "#casa-edel-intro.is-reduced .ce-sparks{",
    "  display:none;",
    "}",
    "#casa-edel-intro.is-reduced .ce-logo-wrap{",
    "  opacity:1;",
    "  transform:none;",
    "  animation:ceReducedFade 800ms ease forwards;",
    "}",
    "#casa-edel-intro.is-reduced .ce-logo{",
    "  animation:none;",
    "  filter:none;",
    "}",
    "@keyframes ceReducedFade{",
    "  0%{opacity:0;}",
    "  35%{opacity:1;}",
    "  75%{opacity:1;}",
    "  100%{opacity:0;}",
    "}"
  ].join("\n");

  var existingStyle = document.querySelector("style[data-casa-edel-intro-style]");
  if (existingStyle && existingStyle.parentNode) {
    existingStyle.parentNode.removeChild(existingStyle);
  }
  document.head.appendChild(styleEl);

  var overlay = document.createElement("div");
  overlay.id = "casa-edel-intro";
  overlay.setAttribute("role", "img");
  overlay.setAttribute("aria-label", "Electricidad Casa Edel");
  if (prefersReducedMotion) {
    overlay.className = "is-reduced";
  }

  var ambient = document.createElement("div");
  ambient.className = "ce-ambient";
  ambient.setAttribute("aria-hidden", "true");

  var stage = document.createElement("div");
  stage.className = "ce-stage";
  stage.setAttribute("aria-hidden", "true");

  var logoWrap = document.createElement("div");
  logoWrap.className = "ce-logo-wrap";

  var logoImg = document.createElement("img");
  logoImg.className = "ce-logo";
  logoImg.src = LOGO_SRC;
  logoImg.alt = "";
  logoImg.decoding = "async";

  var sweep = document.createElement("div");
  sweep.className = "ce-sweep";

  logoWrap.appendChild(logoImg);
  logoWrap.appendChild(sweep);

  var sparksLayer = document.createElement("div");
  sparksLayer.className = "ce-sparks";

  if (!prefersReducedMotion) {
    var sparkColors = ["#ffd23f", "#d3312a", "#faf6ee", "#ffd23f"];
    var sparkCount = 18;
    for (var i = 0; i < sparkCount; i++) {
      var spark = document.createElement("span");
      spark.className = "ce-spark";
      var angle = (Math.PI * 2 * i) / sparkCount + (i % 3) * 0.14;
      var dist = 75 + (i % 5) * 28;
      var tx = Math.round(Math.cos(angle) * dist);
      var ty = Math.round(Math.sin(angle) * dist * 0.72);
      var size = 4 + (i % 3) * 2;
      var delay = 420 + (i % 6) * 160 + (i > 11 ? 1150 : 0);
      var dur = 620 + (i % 4) * 110;
      var color = sparkColors[i % sparkColors.length];

      spark.style.setProperty("--tx", tx + "px");
      spark.style.setProperty("--ty", ty + "px");
      spark.style.setProperty("--s", size + "px");
      spark.style.setProperty("--delay", delay + "ms");
      spark.style.setProperty("--d", dur + "ms");
      spark.style.setProperty("--c", color);
      sparksLayer.appendChild(spark);
    }
  }

  var svgNs = "http://www.w3.org/2000/svg";
  var boltSvg = document.createElementNS(svgNs, "svg");
  boltSvg.setAttribute("class", "ce-bolt-svg");
  boltSvg.setAttribute("viewBox", "0 0 120 120");
  boltSvg.setAttribute("aria-hidden", "true");

  var boltPolygon = document.createElementNS(svgNs, "polygon");
  boltPolygon.setAttribute("points", "68,6 22,66 56,66 46,114 98,50 62,50");
  boltPolygon.setAttribute("fill", "#ffd23f");
  boltPolygon.setAttribute("stroke", "#faf6ee");
  boltPolygon.setAttribute("stroke-width", "3");
  boltPolygon.setAttribute("stroke-linejoin", "round");
  boltSvg.appendChild(boltPolygon);

  stage.appendChild(logoWrap);
  stage.appendChild(sparksLayer);
  stage.appendChild(boltSvg);

  var flash = document.createElement("div");
  flash.className = "ce-flash";
  flash.setAttribute("aria-hidden", "true");

  var skipBtn = document.createElement("button");
  skipBtn.type = "button";
  skipBtn.className = "ce-skip";
  skipBtn.setAttribute("aria-label", "Saltar introducción");
  skipBtn.textContent = "Saltar";

  overlay.appendChild(ambient);
  overlay.appendChild(stage);
  overlay.appendChild(flash);
  overlay.appendChild(skipBtn);

  lockScroll();

  if (document.body.firstChild) {
    document.body.insertBefore(overlay, document.body.firstChild);
  } else {
    document.body.appendChild(overlay);
  }
  if (preStyle.parentNode) preStyle.parentNode.removeChild(preStyle);

  var finished = false;
  var pageLoaded = document.readyState === "complete";
  var startTime = Date.now();
  var minTimer = null;
  var maxTimer = null;
  var cleanupTimer = null;

  function cleanup() {
    if (minTimer) clearTimeout(minTimer);
    if (maxTimer) clearTimeout(maxTimer);
    if (cleanupTimer) clearTimeout(cleanupTimer);
    window.removeEventListener("load", onWindowLoad);

    if (overlay && overlay.parentNode) {
      overlay.parentNode.removeChild(overlay);
    }
    if (styleEl && styleEl.parentNode) {
      styleEl.parentNode.removeChild(styleEl);
    }
    unlockScroll();
  }

  function startExit() {
    if (finished) return;
    finished = true;
    overlay.classList.add("is-leaving");
    cleanupTimer = setTimeout(cleanup, 440);
  }

  function evaluateExit() {
    if (finished) return;
    if (prefersReducedMotion) {
      startExit();
      return;
    }
    var elapsed = Date.now() - startTime;
    if (pageLoaded && elapsed >= MIN_EXIT_MS) {
      startExit();
    }
  }

  function onWindowLoad() {
    pageLoaded = true;
    evaluateExit();
  }

  skipBtn.addEventListener("click", function (ev) {
    ev.stopPropagation();
    startExit();
  });

  overlay.addEventListener("click", function () {
    startExit();
  });

  if (!pageLoaded) {
    window.addEventListener("load", onWindowLoad, { once: true });
  }

  if (prefersReducedMotion) {
    minTimer = setTimeout(startExit, REDUCED_MOTION_MS);
  } else {
    minTimer = setTimeout(function () {
      if (pageLoaded) {
        startExit();
      }
    }, Math.max(MIN_EXIT_MS, TOTAL_DURATION_MS));

    maxTimer = setTimeout(function () {
      startExit();
    }, MAX_WAIT_MS);
  }
    if (preStyle.parentNode) preStyle.parentNode.removeChild(preStyle);
  }

  if (document.body) init(); else document.addEventListener("DOMContentLoaded", init, { once: true });
})();
