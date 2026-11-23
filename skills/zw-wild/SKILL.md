---
name: "zw-wild"
description: "Use when someone asks to make a diagram, widget, chart or web page «wild» (animated, alive, more motion), or runs /zw-wild:wild. Keeps the calm original whole and builds a wild twin beside it: a zoomable mermaid widget gets the wild layer (stars, light along every link, runners, breathing nodes, a wild button), a page gets the campfire (stars, embers, a Wild switch) and an autopilot that runs routines by itself, and a picture becomes a living painting whose lights breathe and whose things explain themselves. Rules: reduced motion honoured, art never tinted (only canvases), private pages never linked from shared ones, every picture looked at before a word about it, and a render checked by eye before saying it works. ⚠ Wild has flashing light and fast motion (a photosensitivity seizure risk), so every wild thing carries a big warning and waits for «I understand»."
---

# zw-wild 0.4.2: make it wild

> **⚠ PHOTOSENSITIVITY WARNING ⚠**
>
> Wild mode has **flashing and flickering light, colour cycling and fast motion**. It can trigger **seizures in people with photosensitive epilepsy**.
> It gets **much stronger when Wild is used more than once at the same time**: several wild pages or widgets open together, or Wild on top of Wild. Two or more at once escalates to truly trippy levels, on purpose.
> Every wild page and widget shows this warning first, and Wild stays off until the viewer presses «I understand». Never strip that warning out of a page you share.
> If you, or anyone watching, is sensitive to flashing light: keep it calm.


Part of zw-wild (Rook, with Claudia, 2026). The code is AGPL-3.0 and these words are CC BY-SA 4.0.

«Wild» means more alive: things move, glow and run by themselves. It never means louder colours on someone's art, and it never means the calm version is gone.

## The five rules

1. **Keep the calm one whole.** Never edit the original. The wild one is a twin beside it (`NAME-wild.html`), and both stay as options. `wildify.py` refuses to write over anything, except that `--update` refreshes a living painting it made itself.
2. **Never tint the art.** Paintings, photos and portraits keep their own colours. A colour drift goes on the canvases, the frames and the diagram lines, never on the picture.
3. **Private stays private.** A page that shows someone's private pictures or words is never linked from a page meant to be shared. Say which is which.
4. **Look, then say.** Look at every picture by eye before writing a word about it. Then check the wild result by eye: in the directory version only as «Two shapes» says, without running anything; with code files, render it (a headless browser is enough) and look at the shot. Say plainly what you did not watch (for example, a timer that fires after the shot).
5. **Warn, everywhere.** Every wild page and widget carries the photosensitivity warning and keeps Wild off until the viewer accepts it; the autopilot never turns Wild on before that. Each page and each widget asks for itself: a yes never carries over to another. Never strip the warning out, and say it again in the reply whenever you hand someone a wild thing, louder when several are open at once.

## Two shapes of this plugin

- **With code files** (from a folder or an uploaded .plugin): run `scripts/wildify.py` directly; the assets are in `assets/`. The commands further down are for this shape.
- **The directory version** (text only, the only kind the directory takes from most publishers): every piece of code is a fenced block in `reference/`. In this shape **never run code and never write a script file**: build the wild twin by hand, as one new HTML file put together from the blocks (beside the original for a widget or a page, in the working folder for a picture; never over a file):
  - **A new diagram widget:** copy the block from `reference/widget-template.md`. Replace the `flowchart TB` source inside ``const body = `...`;`` with the diagram (any backtick in it becomes a single quote, and every backslash is doubled), the lines inside ``const classes = `...`;`` with its class lines, `'tangle-'` in `mermaid.render('tangle-' + k, src)` with a short id of your own, and `LEGEND LINE PER DIAGRAM` with the legend line (write `&lt;` for any `<` in it). That is the calm widget. Its wild twin is the same text, a blank line, then the block from `reference/wild-layer.md`.
  - **An existing widget of the template:** write `NAME-wild.html`: the widget's text, a blank line, then the block from `reference/wild-layer.md`.
  - **A web page:** write `PAGE-wild.html`: the page's text with two scripts inserted just before its last `</body>`: `<script>`, the block from `reference/campfire.md`, `</script>`, then `<script>`, the block from `reference/autopilot.md`, `</script>`.
  - **A picture:** look at it first. Copy the block from `reference/painting.md` to `IMAGE-stem-living.html`, and replace `__TITLE__` with the title (HTML-escaped: `&amp;`, `&lt;`, `&gt;`, `&quot;`), `/*ZW_WILD_DATA*/{}/*END*/` with the data as one JSON object (`title`, `caption`, `src` = the picture's path relative to the page, URL-encoded, and the `spots` described below; write `<\/` for any `</` inside it), and `/*ZW_WILD_AUTOPILOT*/` with the block from `reference/autopilot.md`.
  - **Checking it:** show a widget in the chat's own widget view, or ask the person to open the file and say what they see. Do not start a browser or any other program for it; if nothing was rendered, say so.
  - `reference/wildify.md` holds the tool itself, for a person who wants to save it and run it on their own machine. In this shape Claude never writes it out or runs it.

## Warning the person, step by step

Someone using this plugin meets the warning at every step, so they never meet a flash unwarned:
1. **Before the work:** the first reply to any wild request opens with the warning, word for word:

   **⚠ PHOTOSENSITIVITY WARNING:** wild output has flashing and flickering light, colour cycling and fast motion. It can trigger seizures in people with photosensitive epilepsy, and it gets much stronger with more than one wild thing open at once.
2. **When it stacks:** from the second wild thing in the same conversation or page (making another, making the same thing wild again, or showing several wild widgets at once), say plainly that it stacks and is now far stronger.
3. **When handing it over:** end with a reminder that the file or widget opens with the red warning banner and waits for «I understand», and that the banner must stay in anything shared.
4. **Sensitive viewers:** if the person says they, or anyone who will watch, are sensitive to flashing light, recommend the calm version first.

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

When a page deserves more than the kit (a living painting, cards that turn, a map whose trains move) and the person asks for it, build it by hand as their own page; in the directory version, stay with the blocks in `reference/` and say what more could be built. Keep the same rules and the same switches (`#wild`, `?wild=1`, `?autopilot=0`), and load the autopilot.

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

- With code files: `python scripts/wildify.py --selftest` passes (18 cases in 0.4.1).
- Render the wild file (in the directory version, only as «Two shapes» says), look at it, and check three things: the Wild switch or button is there, the motion layer shows, and no picture changed colour.
- Name the calm original and the wild twin by their full paths, and say what was not watched.
