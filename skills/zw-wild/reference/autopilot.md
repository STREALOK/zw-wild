# autopilot.js

The autopilot: routines that run by themselves; it never turns Wild on before the warning is accepted. Put it inline after the campfire.

> ⚠ PHOTOSENSITIVITY WARNING: wild output has flashing and flickering light, colour cycling and fast motion. It can trigger seizures in people with photosensitive epilepsy, and it gets much stronger with more than one wild thing open at once. Keep the warning and the «I understand» step in anything made from this.

Generated from `assets/autopilot.js` for the copy of zw-wild that carries its code as Markdown. Part of zw-wild (Rook, with Claudia, 2026); the code is AGPL-3.0.

```js
/* zw-wild autopilot: wild routines that run themselves, like a screensaver that hands back control at the first touch.
   A pill at the bottom of the page shows what it is doing; click it to switch it on or off. It starts when the page
   loads, and again after 45 seconds with no mouse, key or wheel. «?autopilot=0» keeps it off at load. Reduced motion:
   it never starts by itself.
   A page may bring its own routines: set window.WILD_ROUTINES = [async w => { ... }, ...] before this script. Each
   routine gets a helper w: w.say(text), await w.hold(ms), w.alive(), w.wild(true|false), w.box(id, true|false),
   w.click(selector), w.$(id). Without its own routines a page gets the generic ones below. A routine that throws is
   skipped, never retried in a loop.
   ⚠ PHOTOSENSITIVITY: the autopilot never turns Wild on before the page's photosensitivity warning has been accepted
   (Wild has flashing light and fast motion; it can trigger seizures in people with photosensitive epilepsy).
   Part of zw-wild (Rook, with Claudia, 2026), AGPL-3.0. */
(function () {
  if (window.__zwAutopilot) return;
  window.__zwAutopilot = true;
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const Q = new URLSearchParams(location.search);
  const wait = ms => new Promise(r => setTimeout(r, ms));
  const $ = id => document.getElementById(id);
  const setBox = (id, v) => { const b = $(id); if (b && b.checked !== v) { b.checked = v; b.dispatchEvent(new Event('change', { bubbles: true })); } };
  const badge = document.createElement('button');
  badge.type = 'button';
  badge.style.cssText = 'position:fixed;left:50%;transform:translateX(-50%);bottom:12px;z-index:2147483001;' +
    'font:13px system-ui,"Segoe UI",sans-serif;color:#e8e4f4;background:#1f1b2bee;border:1px solid #6f5aa8;' +
    'border-radius:999px;padding:4px 12px;cursor:pointer;';
  document.body.appendChild(badge);
  let on = false, idleStart = false, gen = 0, lastInput = performance.now();
  const say = t => { badge.textContent = '◉ autopilot · ' + t; badge.style.borderColor = '#ffb347'; };
  const off = () => { on = false; idleStart = false; gen++; badge.textContent = '○ autopilot'; badge.style.borderColor = '#6f5aa8'; };
  off();
  badge.addEventListener('click', e => { e.stopPropagation(); if (on) off(); else { on = true; idleStart = false; run(++gen); } });
  ['pointerdown', 'keydown', 'wheel'].forEach(ev => addEventListener(ev, e => {
    lastInput = performance.now();
    if (on && idleStart && e.target !== badge) off();
  }, { capture: true }));
  setInterval(() => { if (!on && !reduce && performance.now() - lastInput > 45000) { on = true; idleStart = true; run(++gen); } }, 2000);
  const alive = g => on && g === gen;
  async function hold(g, ms) { const end = performance.now() + ms; while (alive(g) && performance.now() < end) await wait(250); }
  const GENERIC = [
    async w => { if (!w.$('wild')) return; w.say('wild for a while'); w.wild(true); await w.hold(14000); w.wild(false); },
    async w => {
      const t = document.querySelector('[data-wild-tour]'); if (!t) return;
      w.say('a tour'); t.click(); await w.hold(30000); if (w.alive()) t.click();
    },
    async w => {
      const max = document.documentElement.scrollHeight - innerHeight; if (max < 40) return;
      w.say('a slow look round');
      for (let k = 0; k <= 40 && w.alive(); k++) { scrollTo(0, max * (0.5 - 0.5 * Math.cos(k / 40 * 6.283))); await w.hold(300); }
    },
    async w => { w.say('a quiet moment'); await w.hold(8000); },
  ];
  function helper(g) {
    return {
      say, $, alive: () => alive(g), hold: ms => hold(g, ms),
      wild: v => {
        let ok = !!(window.zwWild && window.zwWild.accepted);
        if (!window.zwWild) { try { ok = localStorage.getItem('zw-wild-photosensitivity-ok:' + location.pathname) === 'yes'; } catch (e) { ok = false; } }
        if (v && !ok) { say('Wild waits for the photosensitivity warning to be accepted'); return; }
        return window.zwWild ? window.zwWild.set(v) : setBox('wild', v);
      },
      box: setBox,
      click: sel => { const el = document.querySelector(sel); if (el) el.click(); return !!el; },
    };
  }
  async function run(g) {
    const own = Array.isArray(window.WILD_ROUTINES) && window.WILD_ROUTINES.length ? window.WILD_ROUTINES : null;
    const list = own || GENERIC;
    let prev = -1;
    while (alive(g)) {
      let i = Math.floor(Math.random() * list.length);
      if (i === prev && list.length > 1) i = (i + 1) % list.length;
      prev = i;
      try { await list[i](helper(g)); } catch (e) { say('skipped a step'); await wait(1500); }
      await wait(300);
    }
  }
  if (Q.get('autopilot') !== '0' && !reduce) { on = true; run(++gen); }
})();
```
