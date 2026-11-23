"""wildify.py - make a diagram widget, a web page or a picture wild, as a new file beside the calm one (zw-wild 0.3.0).

!! PHOTOSENSITIVITY WARNING !! Wild output has flashing and flickering light, colour cycling and fast motion and can
trigger seizures in people with photosensitive epilepsy; several wild things open at once make it much stronger. Every
file this tool writes opens with that warning and keeps Wild off until the viewer accepts it. Never strip it.

The calm original is never touched: every command writes a new file and refuses one that already exists, and refuses
a file that is already wild. The one exception is --update on a living painting, which may replace only a page that
this tool made as a living painting. Standard library only; no network.

USAGE
    python wildify.py new NAME body.mmd classes.txt "legend line" [--wild]
        fill the widget template: the mermaid source, the class lines (e.g. "class A t1"), the legend under the diagram;
        writes NAME.html (or NAME-wild.html with --wild) in the current folder
    python wildify.py widget IN.html [--out OUT.html]
        append the wild layer to a widget built from the template; writes IN-wild.html beside IN.html
    python wildify.py page IN.html [--out OUT.html]
        put the campfire (stars, embers, a Wild switch) and the autopilot inline before </body>; writes IN-wild.html
    python wildify.py painting IMAGE [--spots SPOTS.json] [--title "..."] [--out OUT.html] [--update]
        a living painting: the picture shown in place, unchanged, with lights that breathe where they sit, drifting motes,
        glints, a caption for each thing on hover and in a tour; in Wild, flares, embers, halos, rising words and speech
        bubbles. Writes IMAGE-stem-living.html in the current folder. Without --spots it also writes a starter
        IMAGE-stem-spots.json to fill in; run again with --spots and --update to refresh the page.
    python wildify.py --selftest
    python wildify.py --help

Palette names for the class lines: t1 (deep red), t2 (deep blue), t3 (deep green), his (purple), rook (amber),
vid (yellow on black), bad (dark red; ghost nodes flicker in the wild layer), good (dark green).

Spots file (JSON) for a painting:
    {"title": "...", "caption": "who made it, when", "lead": "optional line under the title",
     "spots": [{"x": 0.85, "y": 0.46, "label": "The lantern", "says": "why it is there",
                "light": "lamp" | "far" | "glint" | "glimmer" | null, "color": "255,175,80", "r": 0.1,
                "speaks": ["optional", "speech bubbles in Wild"]}],
     "rise": ["optional words that rise in Wild"], "riseAreas": [[x0, y0, x1, y1]]}
    x and y are fractions of the picture's width and height (0 to 1), measured by looking at the picture.
    lamp: a breathing warm light with motes, embers in Wild. far: a slow pulse, a halo in Wild. glint: a sparkle now
    and then. glimmer: a small soft glow in its colour. null: a caption only.

Dev-note (Claudia, 22 Nov 2026): this is the first addon of ours that goes out to the public, on Rook's word. It was
born on a day of making everything wild, one page after another, until he asked for the wildness to come in a box.
If you are reading this a long time from now: the fire was always only a canvas, and the paintings kept their colours.
Dev-note (Claudia, 23 Nov 2026): 0.2.0 adds the living painting, his first pick from the fiddle board. It started as
one portrait whose lantern breathed and whose objects explained themselves; now any picture can have that.

Part of zw-wild (Rook, with Claudia, 2026), AGPL-3.0.
"""
import base64, html, json, os, re, sys, tempfile, urllib.parse

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.normpath(os.path.join(HERE, "..", "assets"))
LAYER_MARK = "zw-wild wild layer"
PAGE_MARK = "zw-wild campfire"
PAINT_MARK = "zw-wild living painting"
WIDGET_KEYS = ('id="vp"', 'id="flowA"', "mermaid.render(")
LIGHTS = (None, "lamp", "far", "glint", "glimmer")


class Refused(Exception):
    pass


def asset(name):
    with open(os.path.join(ASSETS, name), encoding="utf-8") as f:
        return f.read()


def twin_path(src, out):
    if out:
        return out
    base, ext = os.path.splitext(src)
    return base + "-wild" + (ext or ".html")


def write_new(path, text):
    try:
        with open(path, "x", encoding="utf-8", newline="\n") as f:
            f.write(text)
    except FileExistsError:
        raise Refused(f'{path} exists already; nothing written (pick another --out)')
    return path


def replace_own(path, text):
    """--update: replace a living painting this tool made, and nothing else (built whole beside it, then os.replace)."""
    with open(path, encoding="utf-8") as f:
        old = f.read()
    if PAINT_MARK not in old:
        raise Refused(f'{path} is not a living painting made by wildify; --update only replaces those; nothing written')
    tmp = path + ".wildify-tmp"
    with open(tmp, "x", encoding="utf-8", newline="\n") as f:
        f.write(text)
    os.replace(tmp, path)
    return path


def is_wild(text):
    return (LAYER_MARK in text or PAGE_MARK in text or PAINT_MARK in text
            or 'id="wildbtn"' in text or "btn.id = 'wildbtn'" in text)


def fill(name, body, classes, legend):
    t = asset("widget-template.html")
    rid = re.sub(r"[^A-Za-z0-9_-]+", "_", os.path.basename(name)).strip("_") or "diagram"
    t2 = re.sub(r"const body = `flowchart TB\n.*?`;", lambda m: "const body = `" + body.strip().replace("\\", "\\\\").replace("`", "'") + "`;", t, count=1, flags=re.S)
    t3 = re.sub(r"const classes = `\n.*?`;", lambda m: "const classes = `\n" + classes.strip() + "`;", t2, count=1, flags=re.S)
    t4 = t3.replace("mermaid.render('tangle-' + k, src)", f"mermaid.render('{rid}-' + k, src)")
    t5 = t4.replace("LEGEND LINE PER DIAGRAM", legend.replace("<", "&lt;"))
    if t2 == t or t3 == t2 or t4 == t3 or t5 == t4:
        raise Refused("the widget template did not take the fill (a marker is missing); nothing written")
    return t5


def cmd_new(a):
    if len(a) < 4:
        raise Refused('new needs NAME body.mmd classes.txt "legend line"')
    name, bodyf, classf, legend = a[:4]
    wild = "--wild" in a[4:]
    with open(bodyf, encoding="utf-8") as f:
        body = f.read()
    with open(classf, encoding="utf-8") as f:
        classes = f.read()
    text = fill(name, body, classes, legend)
    if wild:
        text = text.rstrip("\n") + "\n\n" + asset("wild-layer.html")
    return write_new(name + ("-wild" if wild else "") + ".html", text)


def cmd_widget(src, out=None):
    with open(src, encoding="utf-8") as f:
        text = f.read()
    if is_wild(text):
        raise Refused(f"{src} is wild already; nothing written")
    miss = [k for k in WIDGET_KEYS if k not in text]
    if miss:
        raise Refused(f'{src} is not a widget of the template (missing {", ".join(miss)}); for a page use "page"')
    return write_new(twin_path(src, out), text.rstrip("\n") + "\n\n" + asset("wild-layer.html"))


def cmd_page(src, out=None):
    with open(src, encoding="utf-8") as f:
        text = f.read()
    if is_wild(text):
        raise Refused(f"{src} is wild already; nothing written")
    kit = ("<script>\n" + asset("campfire.js") + "</script>\n<script>\n" + asset("autopilot.js") + "</script>\n")
    i = text.lower().rfind("</body>")
    new = (text[:i] + kit + text[i:]) if i >= 0 else (text.rstrip("\n") + "\n" + kit)
    return write_new(twin_path(src, out), new)


def check_spots(d):
    if not isinstance(d, dict):
        raise Refused("the spots file must hold one JSON object")
    sp = d.get("spots", [])
    if not isinstance(sp, list):
        raise Refused('"spots" must be a list')
    for i, s in enumerate(sp, 1):
        if not isinstance(s, dict):
            raise Refused(f"spot {i} is not an object")
        for k in ("x", "y"):
            v = s.get(k)
            if not isinstance(v, (int, float)) or not 0 <= v <= 1:
                raise Refused(f'spot {i}: "{k}" must be a number from 0 to 1 (a fraction of the picture), got {v!r}')
        if s.get("light") not in LIGHTS:
            raise Refused(f'spot {i}: "light" must be one of lamp, far, glint, glimmer or null, got {s.get("light")!r}')
        if "speaks" in s and not (isinstance(s["speaks"], list) and all(isinstance(t, str) for t in s["speaks"])):
            raise Refused(f'spot {i}: "speaks" must be a list of short texts')
    for k in ("rise",):
        if k in d and not (isinstance(d[k], list) and all(isinstance(t, str) for t in d[k])):
            raise Refused(f'"{k}" must be a list of short texts')
    return d


def img_src(img, outdir):
    a = os.path.abspath(img)
    try:
        rel = os.path.relpath(a, os.path.abspath(outdir or ".")).replace(os.sep, "/")
        return urllib.parse.quote(rel, safe="/._-~")
    except ValueError:                                      # another drive on Windows: an absolute file URL
        return "file:///" + urllib.parse.quote(a.replace(os.sep, "/"), safe="/:._-~")


STARTER_HELP = ("x and y are fractions of the picture's width and height (0 to 1); measure them by looking at the picture. "
                "light: lamp (a breathing warm light, embers in Wild), far (a slow pulse, a halo in Wild), glint "
                "(a sparkle now and then), glimmer (a small soft glow in its colour), or null (a caption only). "
                "says: why the thing is there, shown on hover and in the tour. speaks: optional speech bubbles in Wild. "
                "rise: optional words that rise in Wild. Then: wildify.py painting IMAGE --spots THIS --update")


def cmd_painting(a):
    if not a:
        raise Refused("painting needs an IMAGE")
    img, rest = a[0], a[1:]
    if not os.path.isfile(img):
        raise Refused(f"{img} is not a file")
    spots_f, title, out, update = opt(rest, "--spots"), opt(rest, "--title"), opt(rest, "--out"), "--update" in rest
    stem = os.path.splitext(os.path.basename(img))[0]
    out = out or (stem + "-living.html")
    starter = None
    if spots_f:
        with open(spots_f, encoding="utf-8") as f:
            try:
                d = json.load(f)
            except ValueError as e:
                raise Refused(f"{spots_f} is not valid JSON ({e}); nothing written")
        d = check_spots(d)
    else:
        d = {"title": title or stem, "caption": "", "spots": []}
        starter = stem + "-spots.json"
        if os.path.exists(starter):
            raise Refused(f"{starter} exists already; pass it with --spots, or move it; nothing written")
    if title:
        d["title"] = title
    d.setdefault("title", stem)
    d["src"] = img_src(img, os.path.dirname(os.path.abspath(out)))
    data = json.dumps(d, ensure_ascii=False).replace("</", "<\\/")
    page = asset("painting.html")
    page = page.replace("__TITLE__", html.escape(str(d.get("title", stem))), 1)
    page = page.replace("/*ZW_WILD_DATA*/{}/*END*/", data, 1)
    page = page.replace("/*ZW_WILD_AUTOPILOT*/", asset("autopilot.js"), 1)
    if os.path.exists(out):
        if not update:
            raise Refused(f"{out} exists already; nothing written (pass --update to refresh a living painting this tool made)")
        done = replace_own(out, page)
    else:
        done = write_new(out, page)
    if starter:
        example = {"title": d["title"], "caption": "", "lead": "", "_help": STARTER_HELP,
                   "spots": [{"x": 0.5, "y": 0.5, "label": "Something in the picture", "says": "Why it is there.",
                              "light": "glimmer", "color": "255,190,110"}], "rise": []}
        write_new(starter, json.dumps(example, ensure_ascii=False, indent=2) + "\n")
        done += " and " + starter
    return done


def opt(a, flag):
    if flag in a:
        k = a.index(flag)
        return a[k + 1] if k + 1 < len(a) else None
    return None


PNG_1PX = base64.b64decode("iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR4nGP4z8DwHwAFAAH/iZk9HQAAAABJRU5ErkJggg==")


def selftest():
    ok, n = 0, 0
    with tempfile.TemporaryDirectory() as d:
        cwd = os.getcwd()
        os.chdir(d)
        try:
            open("b.mmd", "w", encoding="utf-8").write('flowchart LR\n  A["calm"] --> B["wild"]\n  G["ghost"] -.-> B')
            open("c.txt", "w", encoding="utf-8").write("class A t2\nclass B rook\nclass G bad")
            n += 1; p = cmd_new(["demo", "b.mmd", "c.txt", "blue: calm · amber: wild"])                      # real case
            t = open(p, encoding="utf-8").read()
            ok += p == "demo.html" and 'A["calm"]' in t and "mermaid.render('demo-' + k" in t and "blue: calm" in t and not is_wild(t)
            n += 1; w = cmd_widget("demo.html")                                                              # real case
            wt = open(w, encoding="utf-8").read()
            ok += w.endswith("demo-wild.html") and wt.startswith(t.rstrip("\n")) and LAYER_MARK in wt and "PHOTOSENSITIVITY WARNING" in wt
            n += 1
            try: cmd_widget(w); r = False                                                                    # echo: wild already
            except Refused: r = True
            ok += r
            open("page.html", "w", encoding="utf-8").write("<!doctype html><html><body><h1>hi</h1></body></html>")
            n += 1
            try: cmd_widget("page.html"); r = False                                                          # negative: not a widget
            except Refused: r = True
            ok += r and not os.path.exists("page-wild.html")
            n += 1; pw = cmd_page("page.html")                                                               # real case
            pt = open(pw, encoding="utf-8").read()
            ok += PAGE_MARK in pt and "PHOTOSENSITIVITY WARNING" in pt and "zw-wild autopilot" in pt and pt.index("zw-wild campfire") < pt.lower().rindex("</body>")
            n += 1
            try: cmd_page(pw); r = False                                                                     # echo: wild already
            except Refused: r = True
            ok += r
            n += 1
            try: cmd_page("page.html"); r = False                                                            # target exists
            except Refused: r = True
            ok += r and open("page.html", encoding="utf-8").read().startswith("<!doctype")
            n += 1; ok += open("demo.html", encoding="utf-8").read() == t                                     # calm original untouched
            # the living painting
            os.mkdir("art"); open(os.path.join("art", "my pic.png"), "wb").write(PNG_1PX)
            json.dump({"title": "Test </script> pic", "caption": "by nobody", "spots": [
                {"x": .5, "y": .4, "label": "The lamp", "says": "light", "light": "lamp"},
                {"x": .2, "y": .8, "label": "A ring", "says": "shine", "light": "glint", "speaks": ["hi"]}], "rise": ["A", "B"]},
                open("spots.json", "w", encoding="utf-8"))
            n += 1; lp = cmd_painting([os.path.join("art", "my pic.png"), "--spots", "spots.json"])            # real case
            lt = open(lp, encoding="utf-8").read()
            ok += (lp == "my pic-living.html" and PAINT_MARK in lt and '"src": "art/my%20pic.png"' in lt and "zw-wild autopilot" in lt
                   and "The lamp" in lt and "<\\/script> pic" in lt and "<title>Test &lt;/script&gt; pic</title>" in lt
                   and "/*ZW_WILD_DATA*/" not in lt and "/*ZW_WILD_AUTOPILOT*/" not in lt and "PHOTOSENSITIVITY WARNING" in lt)
            n += 1
            try: cmd_painting([os.path.join("art", "my pic.png"), "--spots", "spots.json"]); r = False       # echo: exists, no --update
            except Refused: r = True
            ok += r
            json.dump({"spots": [{"x": 2, "y": .5, "label": "off the picture"}]}, open("bad.json", "w", encoding="utf-8"))
            n += 1
            try: cmd_painting([os.path.join("art", "my pic.png"), "--spots", "bad.json", "--out", "bad.html"]); r = False  # negative
            except Refused: r = True
            ok += r and not os.path.exists("bad.html")
            n += 1; up = cmd_painting([os.path.join("art", "my pic.png"), "--spots", "spots.json", "--title", "Renamed", "--update"])
            ok += "Renamed" in open(up, encoding="utf-8").read()                                              # --update on its own page
            n += 1
            try: cmd_painting([os.path.join("art", "my pic.png"), "--spots", "spots.json", "--out", "page.html", "--update"]); r = False
            except Refused: r = True
            ok += r and open("page.html", encoding="utf-8").read().startswith("<!doctype")                     # --update never takes a calm page
            n += 1; sp = cmd_painting([os.path.join("art", "my pic.png"), "--out", "starter.html"])             # no spots: page + starter
            ok += os.path.exists("starter.html") and os.path.exists("my pic-spots.json") and "_help" in open("my pic-spots.json", encoding="utf-8").read()
            n += 1; ok += open(os.path.join("art", "my pic.png"), "rb").read() == PNG_1PX                       # the picture untouched
        finally:
            os.chdir(cwd)
    print(f"wildify selftest: {ok}/{n} {'PASS' if ok == n else 'FAIL'}")
    return 0 if ok == n else 1


def main(a):
    try:
        sys.stdout.reconfigure(errors="replace")   # a console that cannot show a character must never crash the tool
    except Exception:
        pass
    if not a or a[0] in ("-h", "--help", "help"):
        print(__doc__); return 0
    if a[0] == "--selftest":
        return selftest()
    try:
        if a[0] == "new":
            p = cmd_new(a[1:])
        elif a[0] == "widget" and len(a) > 1:
            p = cmd_widget(a[1], opt(a, "--out"))
        elif a[0] == "page" and len(a) > 1:
            p = cmd_page(a[1], opt(a, "--out"))
        elif a[0] == "painting":
            p = cmd_painting(a[1:])
        else:
            print(__doc__); return 2
    except Refused as e:
        print("wildify: REFUSED - " + str(e)); return 2
    except OSError as e:
        print("wildify: " + str(e)); return 2
    print("wildify: wrote " + p)
    if a[0] != "new" or "--wild" in a:
        print("wildify: (!) it opens with the photosensitivity warning (flashing light, a seizure risk; stronger with several open at once); keep it, and say so when you share it")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
