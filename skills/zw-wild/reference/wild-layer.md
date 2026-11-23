# wild-layer.html

The wild layer for a widget built from the template, with its warning step. Append it after the widget.

> ⚠ PHOTOSENSITIVITY WARNING: wild output has flashing and flickering light, colour cycling and fast motion. It can trigger seizures in people with photosensitive epilepsy, and it gets much stronger with more than one wild thing open at once. Keep the warning and the «I understand» step in anything made from this.

Generated from `assets/wild-layer.html` for the copy of zw-wild that carries its code as Markdown. Part of zw-wild (Rook, with Claudia, 2026); the code is AGPL-3.0.

```html
<!-- zw-wild wild layer: append it after a widget built from widget-template.html (it needs #vp, #flowA and #flowB).
     Adds stars in the viewport, light flowing along every link, dots riding the links, breathing nodes, glowing boxes,
     a flicker on nodes of class «bad» (ghosts), and a «wild» button (faster, a colour drift on the viewport).
     Honours reduced motion.
     ⚠ PHOTOSENSITIVITY WARNING: wild has flashing, colour cycling and fast motion and can trigger seizures in people with
     photosensitive epilepsy; several wild widgets at once make it much stronger. The first click on «wild ⚠» shows the
     warning, and wild turns on only after «I understand». Part of zw-wild (Rook, with Claudia, 2026), AGPL-3.0. -->
<style>
  #wstars { position:absolute; inset:0; z-index:0; pointer-events:none; }
  #stage { z-index:1; }
  #wildbtn { position:absolute; right:8px; top:8px; z-index:3; font:inherit; font-size:12px; padding:2px 9px; border-radius:8px; border:0.5px solid var(--border); background:var(--surface-1); color:var(--text-primary); cursor:pointer; }
  #wildbtn.on { border-color:#ffd000; color:#ffd000; }
  #wwarn { position:absolute; left:50%; top:40px; transform:translateX(-50%); z-index:4; max-width:min(92%, 560px); background:#3a0d12; color:#ffe9ea; border:2px solid #ff4d5e; border-radius:10px; padding:10px 14px; font-size:13px; line-height:1.5; display:none; cursor:default; }
  #wwarn .wrow { display:flex; gap:8px; margin-top:8px; flex-wrap:wrap; }
  #wwarn button { font:inherit; font-size:12px; border-radius:8px; padding:3px 10px; cursor:pointer; background:#5a1820; color:#fff; border:1px solid #ff8a95; }
  @media (prefers-reduced-motion: no-preference) {
    #vp .flowchart-link { stroke-dasharray:7 6 !important; animation:wflow 1.3s linear infinite; }
    #vp.wild .flowchart-link { animation-duration:.4s; }
    #vp .node { animation:wbreathe 2.6s ease-in-out infinite; }
    #vp.wild .node { animation-duration:.9s; }
    #vp .cluster rect { animation:wglow 3.2s ease-in-out infinite; }
    #vp.wild .cluster rect { animation-duration:1s; }
  }
  @keyframes wflow { to { stroke-dashoffset:-26; } }
  @keyframes wbreathe { 50% { filter:brightness(1.45); } }
  @keyframes wglow { 50% { stroke:#c77dff; } }
</style>
<script>
(function () {
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const vp = document.getElementById('vp'); if (!vp) return;
  const NS = 'http://www.w3.org/2000/svg';
  const btn = document.createElement('button'); btn.id = 'wildbtn'; btn.textContent = 'wild ⚠'; btn.title = 'Photosensitivity warning: flashing, colour cycling and fast motion'; vp.appendChild(btn);
  let wild = false;
  // ⚠ Photosensitivity gate: wild has flashing, colour cycling and fast motion; the first click shows the warning.
  const WARN = "⚠ PHOTOSENSITIVITY WARNING ⚠ Wild mode has flashing and flickering light, colour cycling and fast motion. It can trigger seizures in people with photosensitive epilepsy, and it gets much stronger when Wild is used more than once at the same time (several wild pages or widgets open together, or Wild on top of Wild). If you or anyone watching is sensitive to flashing light, keep it calm.";
  let accepted = false; try { accepted = localStorage.getItem('zw-wild-photosensitivity-ok') === 'yes'; } catch (e) {}
  const ww = document.createElement('div'); ww.id = 'wwarn'; ww.setAttribute('role', 'alert');
  const wt = document.createElement('div'); wt.textContent = WARN; ww.appendChild(wt);
  const wr = document.createElement('div'); wr.className = 'wrow'; ww.appendChild(wr);
  const wy = document.createElement('button'); wy.type = 'button'; wy.textContent = 'I understand, turn wild on';
  const wn = document.createElement('button'); wn.type = 'button'; wn.textContent = 'Keep it calm';
  wr.appendChild(wy); wr.appendChild(wn); vp.appendChild(ww);
  for (const el of [ww, wy, wn]) { el.addEventListener('pointerdown', e => e.stopPropagation()); el.addEventListener('dblclick', e => e.stopPropagation()); el.addEventListener('wheel', e => e.stopPropagation()); }
  const setWild = v => { wild = v; btn.classList.toggle('on', wild); vp.classList.toggle('wild', wild); };
  wy.addEventListener('click', e => { e.stopPropagation(); accepted = true; try { localStorage.setItem('zw-wild-photosensitivity-ok', 'yes'); } catch (er) {} ww.style.display = 'none'; setWild(true); });
  wn.addEventListener('click', e => { e.stopPropagation(); ww.style.display = 'none'; });
  btn.addEventListener('pointerdown', e => e.stopPropagation());
  btn.addEventListener('dblclick', e => e.stopPropagation());
  btn.addEventListener('click', e => { e.stopPropagation(); if (!wild && !accepted) { ww.style.display = 'block'; return; } setWild(!wild); });
  const cv = document.createElement('canvas'); cv.id = 'wstars'; vp.insertBefore(cv, vp.firstChild); const cx = cv.getContext('2d');
  const stars = Array.from({ length: 90 }, (_, i) => ({ x: Math.random(), y: Math.random(), r: .4 + Math.random() * 1.4, ph: Math.random() * 6.3, c: i % 7 ? '#cbb8ff' : '#ffb84d' }));
  let T = 0, last = performance.now(), runners = [], ghosts = [], ready = false;
  function setup() {
    let any = false;
    for (const k of ['A', 'B']) {
      const svg = document.querySelector('#flow' + k + ' svg'); if (!svg) return false;
      svg.querySelectorAll('path.flowchart-link').forEach((p, i) => {
        let L = 0; try { L = p.getTotalLength(); } catch (e) {} if (!L) return;
        for (let j = 0; j < 2; j++) { const c = document.createElementNS(NS, 'circle'); c.setAttribute('r', 3.4); c.setAttribute('fill', j ? '#ffd000' : '#ffffff'); c.setAttribute('pointer-events', 'none'); p.parentNode.appendChild(c); runners.push({ p, L, c, t: (i * .17 + j * .5) % 1, v: .16 + (i % 3) * .05 }); any = true; }
      });
      svg.querySelectorAll('.node.bad').forEach(n => ghosts.push(n));
    }
    return any;
  }
  function tick(now) {
    const raw = Math.min(.05, (now - last) / 1000), dt = raw * (reduce ? 0 : 1) * (wild ? 3 : 1); last = now; T += dt;
    if (!ready) ready = setup();
    const w = vp.clientWidth, h = vp.clientHeight, d = window.devicePixelRatio || 1;
    if (cv.width !== Math.round(w * d) || cv.height !== Math.round(h * d)) { cv.width = Math.round(w * d); cv.height = Math.round(h * d); cv.style.width = w + 'px'; cv.style.height = h + 'px'; }
    cx.setTransform(d, 0, 0, d, 0, 0); cx.clearRect(0, 0, w, h);
    for (const s of stars) { cx.globalAlpha = .12 + .55 * (.5 + .5 * Math.sin(T * 2 + s.ph)); cx.fillStyle = s.c; cx.beginPath(); cx.arc(s.x * w, s.y * h, s.r, 0, 6.29); cx.fill(); }
    for (const r of runners) { r.t = (r.t + r.v * dt) % 1; const pt = r.p.getPointAtLength(r.t * r.L); r.c.setAttribute('cx', pt.x.toFixed(1)); r.c.setAttribute('cy', pt.y.toFixed(1)); }
    for (const g of ghosts) g.style.opacity = reduce ? '' : (.4 + .5 * (.5 + .5 * Math.sin(T * 3))).toFixed(2);
    vp.style.filter = wild && !reduce ? `hue-rotate(${(Math.sin(T * .3) * 30).toFixed(1)}deg)` : '';
    requestAnimationFrame(tick);
  }
  if (new URLSearchParams(location.search).get('wild')) btn.click();
  requestAnimationFrame(tick);
})();
</script>
```
