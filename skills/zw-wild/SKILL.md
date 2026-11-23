---
name: "zw-wild"
description: "Use when someone asks to make a diagram, widget, chart or web page «wild» (animated, alive, more motion), or runs /zw-wild:wild. Keeps the calm original whole and builds a wild twin beside it: a zoomable mermaid widget gets the wild layer (stars, light along every link, runners, breathing nodes, a wild button), a page gets the campfire (stars, embers, a Wild switch) and an autopilot that runs routines by itself. Rules: reduced motion honoured, art never tinted (only canvases), private pages never linked from shared ones, every picture looked at before a word about it, and a render checked by eye before saying it works."
---

# zw-wild 0.2.1: make it wild

Part of zw-wild (Rook, with Claudia, 2026). The code is AGPL-3.0 and these words are CC BY-SA 4.0.

«Wild» means more alive: things move, glow and run by themselves. It never means louder colours on someone's art, and it never means the calm version is gone.

## The four rules

1. **Keep the calm one whole.** Never edit the original. The wild one is a twin beside it (`NAME-wild.html`), and both stay as options. `wildify.py` refuses to write over anything.
2. **Never tint the art.** Paintings, photos and portraits keep their own colours. A colour drift goes on the canvases, the frames and the diagram lines, never on the picture.
3. **Private stays private.** A page that shows someone's private pictures or words is never linked from a page meant to be shared. Say which is which.
4. **Look, then say.** Look at every picture by eye before writing a word about it. Render the wild result (a headless browser is enough), look at the shot, and say plainly what you did not watch (for example, a timer that fires after the shot).

## A mermaid diagram: the widget and its wild layer

- `assets/widget-template.html` is a zoomable widget. It has two deep palettes (A and B), zooms at the cursor with the wheel, pans by drag, has the +, -, 1:1 and fit buttons, and double-click fits it. Zoom resizes the SVG itself, so text stays sharp.
- Fill it with the tool:

  ```
  python scripts/wildify.py new NAME body.mmd classes.txt "legend line" [--wild]
  ```

  `body.mmd` is the mermaid source (flowchart). `classes.txt` holds lines like `class A t2`.
  - Palette names: `t1` deep red, `t2` deep blue, `t3` deep green, `his` purple, `rook` amber, `vid` yellow on black, `bad` dark red, `good` dark green.
  - The legend line says what each colour means in this diagram.
- To make an existing template widget wild, so it gets a twin:

  ```
  python scripts/wildify.py widget NAME.html
  ```

- `assets/wild-layer.html` adds:
  - stars in the viewport;
  - light flowing along every link, with dots riding them;
  - breathing nodes and glowing group boxes;
  - a flicker on nodes of class `bad` (ghosts);
  - a «wild» button in the top right of the diagram, for faster motion and a colour drift on the diagram.
- In a chat that can show HTML widgets, show the finished file's content as the widget.

## A web page: the campfire and the autopilot

```
python scripts/wildify.py page PAGE.html
```

This writes `PAGE-wild.html` with two scripts inline before `</body>`.

- **campfire.js:**
  - stars, embers and a fire glow on one canvas over the page, with a screen blend and no pointer events;
  - a Wild switch: it uses the page's own `<input type="checkbox" id="wild">`, or adds one top right;
  - `?wild=1` starts it wild;
  - `window.zwWild.set(true|false)` flips it.
- **autopilot.js:**
  - routines that run by themselves, shown in a pill at the bottom;
  - it starts at load, and again after 45 seconds idle; the first touch hands control back;
  - `?autopilot=0` keeps it off at load.
  - Generic routines: wild for a while, a tour (it clicks the first `[data-wild-tour]` element, and again to end it), a slow scroll round the page, a quiet moment.
  - A page can bring its own routines, set before the script:

    ```js
    window.WILD_ROUTINES = [
      async w => { w.say('rush hour'); w.wild(true); await w.hold(14000); w.wild(false); },
      async w => { w.say('a tour'); w.click('#tour'); await w.hold(30000); },
    ];
    ```

    The helper `w` has `say`, `hold`, `alive`, `wild`, `box(id, on)`, `click(selector)` and `$`.

When a page deserves more than the kit (a living painting, cards that turn, a map whose trains move), build it by hand. Keep the same rules and the same switches (`#wild`, `?wild=1`, `?autopilot=0`), and load the autopilot.

## A picture: the living painting

```
python scripts/wildify.py painting IMAGE --spots SPOTS.json [--title "..."] [--out OUT.html] [--update]
```

This writes `IMAGE-stem-living.html` in the current folder, never beside someone else's picture, and the picture stays as it is.

- Look at the picture first, then place its spots. Each spot is a thing in the picture, at `x` and `y` given as fractions of the picture's width and height (0 to 1).
- What a spot holds:
  - a `label` and a `says` line (why it is there): shown on hover and in the tour;
  - optionally a `light`, an optional `color` ("r,g,b") and `r` (size);
  - optionally `speaks`: speech bubbles in Wild.
- The kinds of light:
  - `lamp`: a breathing warm light with motes; embers in Wild;
  - `far`: a slow pulse; a halo in Wild;
  - `glint`: a sparkle now and then;
  - `glimmer`: a small soft glow in its colour.
- A spot without a label is a light only: it gets no caption and no stop on the tour.
- Optional `rise`: words that rise in Wild, within `riseAreas` (boxes of fractions).
- Without `--spots`, the tool writes a starter `IMAGE-stem-spots.json` to fill in. After that, `--spots` and `--update` refresh the page. `--update` only ever replaces a living painting this tool made.

## Reduced motion

Everything here honours `prefers-reduced-motion`: the sky stands still, nothing flies, and the autopilot never starts by itself.

## Before saying it is done

- `python scripts/wildify.py --selftest` passes (15 cases in 0.2.0).
- Render the wild file, look at the shot, and check three things: the Wild switch or button is there, the motion layer shows, and no picture changed colour.
- Name the calm original and the wild twin by their full paths, and say what was not watched.
