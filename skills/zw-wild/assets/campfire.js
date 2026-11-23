/* zw-wild campfire: stars, embers and a fire glow over any page, plus a Wild switch.

   ⚠ PHOTOSENSITIVITY WARNING ⚠  Wild mode has flashing and flickering light, colour cycling and fast motion. It can
   trigger seizures in people with photosensitive epilepsy. It gets much stronger when Wild is used more than once at
   the same time: several wild pages or widgets open together, or Wild on top of Wild. So the page shows this warning
   first, and Wild stays off until the viewer presses «I understand, turn Wild on». The calm campfire (slow stars and
   a faint glow, no flashing) runs without it.

   Put it before </body>. It draws on one canvas laid over the page with a screen blend and no pointer events, so the
   page stays clickable and its pictures keep their own colours: only the canvas is ever tinted.
   «?wild=1» starts wild only once the warning has been accepted on this page. Reduced motion: a still sky.
   It uses the page's own <input type="checkbox" id="wild"> when there is one, else it adds a small switch, top right.
   window.zwWild.on reads it, window.zwWild.accepted says whether the warning was accepted, window.zwWild.set(true|false)
   flips it (turning it on still asks first).
   Part of zw-wild (Rook, with Claudia, 2026), AGPL-3.0. */
(function () {
  if (window.__zwCampfire) return;
  window.__zwCampfire = true;
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const KEY = 'zw-wild-photosensitivity-ok';
  let accepted = false;
  try { accepted = localStorage.getItem(KEY) === 'yes'; } catch (e) { /* storage blocked: ask every time */ }
  const WARN = '⚠ PHOTOSENSITIVITY WARNING ⚠ Wild mode has flashing and flickering light, colour cycling and fast motion. ' +
    'It can trigger seizures in people with photosensitive epilepsy, and it gets much stronger when Wild is used more than ' +
    'once at the same time (several wild pages or widgets open together, or Wild on top of Wild). If you or anyone watching ' +
    'is sensitive to flashing light, keep it calm.';
  let box = document.getElementById('wild');
  let chip = null;
  if (!box) {
    const lab = document.createElement('label');
    lab.style.cssText = 'position:fixed;right:14px;top:12px;z-index:2147483000;display:flex;align-items:center;gap:6px;' +
      'font:13px system-ui,"Segoe UI",sans-serif;color:#ece6ff;background:#221d30e6;border:1px solid #4a3d6e;' +
      'border-radius:8px;padding:4px 10px;cursor:pointer;';
    box = document.createElement('input');
    box.type = 'checkbox';
    box.id = 'wild';
    lab.appendChild(box);
    lab.appendChild(document.createTextNode('Wild'));
    chip = document.createElement('span');
    chip.textContent = '⚠ flashing';
    chip.title = WARN;
    chip.style.cssText = 'color:#ffb3ba;font-size:11px;border:1px solid #ff4d5e;border-radius:6px;padding:0 5px;';
    lab.appendChild(chip);
    document.body.appendChild(lab);
  } else {
    box.title = WARN;
  }
  const banner = document.createElement('div');
  banner.setAttribute('role', 'alert');
  banner.style.cssText = 'position:fixed;left:50%;top:10px;transform:translateX(-50%);z-index:2147483002;max-width:min(92vw,660px);' +
    'background:#3a0d12;color:#ffe9ea;border:2px solid #ff4d5e;border-radius:10px;padding:12px 16px;' +
    'font:14px/1.5 system-ui,"Segoe UI",sans-serif;box-shadow:0 8px 30px rgba(0,0,0,.6);display:none;';
  const text = document.createElement('div');
  text.textContent = WARN;
  const row = document.createElement('div');
  row.style.cssText = 'display:flex;gap:8px;margin-top:10px;flex-wrap:wrap;';
  const yes = document.createElement('button');
  yes.type = 'button';
  yes.textContent = 'I understand, turn Wild on';
  const no = document.createElement('button');
  no.type = 'button';
  no.textContent = 'Keep it calm';
  for (const b of [yes, no]) b.style.cssText = 'font:inherit;font-size:13px;border-radius:8px;padding:4px 12px;cursor:pointer;' +
    'background:#5a1820;color:#fff;border:1px solid #ff8a95;';
  row.appendChild(yes); row.appendChild(no);
  banner.appendChild(text); banner.appendChild(row);
  document.body.appendChild(banner);
  const show = () => { banner.style.display = 'block'; };
  const hide = () => { banner.style.display = 'none'; };
  yes.addEventListener('click', () => {
    accepted = true;
    try { localStorage.setItem(KEY, 'yes'); } catch (e) { /* this view only */ }
    hide();
    box.checked = true;
    box.dispatchEvent(new Event('change', { bubbles: true }));
  });
  no.addEventListener('click', () => { hide(); box.checked = false; });
  box.addEventListener('change', () => { if (box.checked && !accepted) { box.checked = false; show(); } });
  if (new URLSearchParams(location.search).get('wild')) { if (accepted) box.checked = true; else show(); }
  if (!accepted) show();
  const cv = document.createElement('canvas');
  cv.setAttribute('aria-hidden', 'true');
  cv.style.cssText = 'position:fixed;inset:0;width:100%;height:100%;pointer-events:none;z-index:2147482000;mix-blend-mode:screen;';
  document.body.appendChild(cv);
  const cx = cv.getContext('2d');
  let W = 0, H = 0;
  function size() {
    const d = window.devicePixelRatio || 1;
    W = innerWidth; H = innerHeight;
    cv.width = Math.round(W * d); cv.height = Math.round(H * d);
    cx.setTransform(d, 0, 0, d, 0, 0);
  }
  addEventListener('resize', size);
  size();
  const stars = Array.from({ length: 110 }, () => ({ x: Math.random(), y: Math.random(), r: .4 + Math.random() * 1.2, ph: Math.random() * 6.3 }));
  let embers = [], T = 0, last = performance.now();
  function tick(now) {
    const wild = box.checked && accepted && !reduce;
    const raw = Math.min(.05, (now - last) / 1000), dt = raw * (reduce ? 0 : 1) * (wild ? 2.2 : 1);
    last = now; T += dt;
    cx.clearRect(0, 0, W, H);
    for (const s of stars) {
      cx.globalAlpha = .06 + .3 * (.5 + .5 * Math.sin(T * 2 + s.ph));
      cx.fillStyle = '#d9ccff';
      cx.beginPath(); cx.arc(s.x * W, s.y * H, s.r, 0, 6.29); cx.fill();
    }
    const g = cx.createRadialGradient(W / 2, H + 20, 10, W / 2, H + 20, 480 * (1 + .1 * Math.sin(T * 9)));
    g.addColorStop(0, wild ? 'rgba(255,150,60,.30)' : 'rgba(255,150,60,.18)');
    g.addColorStop(1, 'rgba(255,120,40,0)');
    cx.globalAlpha = 1; cx.fillStyle = g; cx.fillRect(0, 0, W, H);
    if (!reduce) for (let k = 0; k < (wild ? 3 : 1); k++) if (Math.random() < .6) {
      embers.push({ x: Math.random() * W, y: H + 10, vx: (Math.random() - .5) * 20, vy: -(40 + Math.random() * 90) * (wild ? 1.7 : 1),
        life: 4 + Math.random() * 3, max: 7, r: .8 + Math.random() * 1.6 });
    }
    for (const e of embers) {
      e.x += e.vx * raw + Math.sin(T * 2 + e.y * .02) * 10 * raw; e.y += e.vy * raw; e.life -= raw;
      cx.globalAlpha = Math.max(0, e.life / e.max) * .85; cx.fillStyle = '#ffb347';
      cx.beginPath(); cx.arc(e.x, e.y, e.r, 0, 6.29); cx.fill();
    }
    embers = embers.filter(e => e.life > 0 && e.y > -20);
    cx.globalAlpha = 1;
    cv.style.filter = wild ? `hue-rotate(${(Math.sin(T * .25) * 14).toFixed(1)}deg)` : '';
    requestAnimationFrame(tick);
  }
  window.zwWild = {
    get on() { return box.checked && accepted; },
    get accepted() { return accepted; },
    set(v) {
      if (v && !accepted) { show(); return; }
      if (box.checked !== !!v) { box.checked = !!v; box.dispatchEvent(new Event('change', { bubbles: true })); }
    },
  };
  requestAnimationFrame(tick);
})();
