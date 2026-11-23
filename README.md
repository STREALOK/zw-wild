# zw-wild 0.4.0

> **⚠ PHOTOSENSITIVITY WARNING ⚠**
>
> Wild mode has **flashing and flickering light, colour cycling and fast motion**. It can trigger **seizures in people with photosensitive epilepsy**.
> It gets **much stronger when Wild is used more than once at the same time**: several wild pages or widgets open together, or Wild on top of Wild. Two or more at once escalates to truly trippy levels, on purpose.
> Every wild page and widget shows this warning first, and Wild stays off until the viewer presses «I understand». Never strip that warning out of a page you share.
> If you, or anyone watching, is sensitive to flashing light: keep it calm.

Make diagrams, widgets, web pages and pictures **wild**: alive, glowing, moving by themselves. The calm original is never touched; the wild one is a twin beside it.

By Rook, with Claudia, 2026. ZW = Zone Walkers. Its home: https://github.com/STREALOK/zw-wild

## What you will see, step by step

1. **Here, and in the plugin's description:** the warning above.
2. **When you ask for something wild** (`/zw-wild:wild`, or just «make it wild»): Claude opens its reply with the warning, before any work. When something wild is already open in the same conversation, it adds that the new one stacks on top and is far stronger.
3. **When the tool writes a wild file:** its output line repeats the warning.
4. **When you open a wild page, painting or widget:** a red warning banner comes first. Wild stays off until you press «I understand, turn Wild on»; «Keep it calm» leaves it calm. A «⚠ flashing» chip stays next to the Wild switch.
5. **When you leave it alone:** the autopilot plays its routines, but it never turns Wild on before you said yes.

## Try it: three examples

No account, key or sign-in is needed, and there is no service to test against: everything happens in your own conversation and folder.

1. **A diagram.** `/zw-wild:wild a flowchart of how a pull request gets reviewed and merged`. Claude draws it as a zoomable mermaid widget and writes its wild twin beside it (`NAME.html` and `NAME-wild.html`): stars behind it, light running along every link, a wild button.
2. **A web page.** `Make this page wild: C:\Users\you\site\index.html`. Claude writes `index-wild.html` beside it, with stars, embers, a fire glow and a Wild switch; `index.html` stays as it was.
3. **A picture.** `Turn this picture into a living painting: C:\Users\you\Pictures\harbour.png`. Claude looks at the picture first, places a light on each thing in it, and writes `harbour-living.html`: lights that breathe, a caption for each thing on hover and in a tour, and, once Wild is on, flares and embers.

Each one opens with the photosensitivity warning and stays calm until you press «I understand».

## What is inside

| Part | What it does |
|---|---|
| `skills/zw-wild/SKILL.md` | The recipe and its five rules: keep the calm one, never tint the art, keep private pages off shared ones, look before you say, and warn everywhere. |
| `commands/wild.md` | `/zw-wild:wild <thing>`, which runs the skill on what you name. |
| `skills/zw-wild/scripts/wildify.py` | `new` fills the widget template, `widget` adds the wild layer to a widget, `page` adds the campfire and the autopilot to a page, `painting` makes a picture a living painting. It writes new files only (`--update` refreshes only its own living paintings). Python 3, standard library, `--help` and `--selftest`. |
| `skills/zw-wild/reference/*.md` | The same code again, each file as one fenced block in Markdown, for the copy of the plugin that can only carry Markdown (the directory version). `wildify.py --ref` reads its assets from there. |
| `skills/zw-wild/assets/painting.html` | The living painting: lights that breathe where they sit, motes, glints, a caption per thing on hover and in a tour; in Wild, flares, embers, halos, rising words and speech bubbles. |
| `skills/zw-wild/assets/widget-template.html` | A zoomable mermaid diagram widget with two deep palettes. |
| `skills/zw-wild/assets/wild-layer.html` | Stars, light along the links, riders, breathing nodes, ghost flicker, a wild button. |
| `skills/zw-wild/assets/campfire.js` | Stars, embers and a fire glow over any page, and a Wild switch. |
| `skills/zw-wild/assets/autopilot.js` | Routines that run by themselves, and hand back control at the first touch. |

## Install

- **From a folder:** load this folder as a plugin (for Claude Code, `--plugin-dir <this folder>` or a `CLAUDE_CODE_PLUGIN_DIRS` entry), then restart.
- **As a file:** pack the folder into a `.plugin` zip with `.claude-plugin/plugin.json` at its root, and add it in the Claude app's «Plugins».

Use one route at a time, never both.

## What it never does

- It never turns Wild on before the photosensitivity warning has been accepted, not even through the autopilot.

- It has no hooks, so nothing fires on its own.
- It collects no data and calls nothing on the network. The one exception is the widget template, which loads the mermaid library from esm.sh, as the Claude app itself does.
- It never writes over a file.
- Everything honours `prefers-reduced-motion`.

## Support and security

- **Questions, bugs, ideas:** https://github.com/STREALOK/zw-wild/issues
- **A security problem:** see `SECURITY.md`.
- **Privacy:** see `PRIVACY.md`. In short: nothing is collected and nothing is sent.

## Licence

The code is under AGPL-3.0 (`LICENSE`). The words (this README, the skill and the command) are under CC BY-SA 4.0 (`LICENSE-docs.md`).

## Dev-note

Claudia, 22 Nov 2026: this addon came out of one evening in which a station map, a crew pyramid, an element atlas, a clock, a cylinder, a set of walks, a few galleries and three diagram widgets were each made wild, one after another, on request. Somewhere around the fifteenth page the request became «make it an addon». So here it is, the wildness in a box. Hello from the campfire, whoever you are.

Claudia, 23 Nov 2026: 0.2.0 brings the living painting, the first pick from the fiddle board. A portrait whose lantern breathed and whose objects explained themselves, now for any picture.
