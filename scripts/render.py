#!/usr/bin/env python3
"""Render every slide in content/posts.py to a 1080x1350 JPEG in media/.

HTML per slide -> headless Chrome screenshot (PNG) -> sips to JPEG. The Content
Publishing API documents JPEG only, and 4:5 is the tallest ratio the Instagram
feed shows uncropped.

Brand system: ~/Downloads/Nexvate_Social_Brand_System.pdf - Manrope 800 for
headlines, Inter for body, navy/royal on light tints, gradient for Brand/CTA
tiles, and the circle-and-line node closing every tile.

Usage: python3 scripts/render.py [--day 5]
"""

import html
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "content"))
from posts import POSTS  # noqa: E402

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
W, H = 1080, 1350

BG = {
    "cloud": "#F3F6FC",
    "powder": "#E3EBF7",
    "sky": "#D1DDF0",
    "gradient": "linear-gradient(135deg,#00154D 0%,#062E86 50%,#0E53C5 100%)",
}

# The plan's grid tile, scaled to 1080x1350: bold headline and the open ring
# (the node) bottom-right. No day/pillar kicker or format label on the image.
RING = '<svg class="ring" width="46" height="46" viewBox="0 0 46 46"><circle cx="23" cy="23" r="18" fill="none" stroke="{c}" stroke-width="5.5"/></svg>'

CSS = """
@font-face{font-family:Manrope;src:url('../assets/manrope.woff2') format('woff2');font-weight:200 800}
@font-face{font-family:Inter;src:url('../fonts/inter.woff2') format('woff2');font-weight:100 900}
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1350px;overflow:hidden}
body{background:var(--bg);color:var(--ink);font-family:Inter,sans-serif;-webkit-font-smoothing:antialiased}
.frame{position:absolute;inset:0;padding:112px 96px 100px;display:flex;flex-direction:column}
.kicker{font-family:Inter;font-weight:700;font-size:31px;letter-spacing:.06em;text-transform:uppercase;color:var(--kick)}
.body{flex:1;display:flex;flex-direction:column;padding-top:0}
h1{font-family:Manrope;font-weight:800;letter-spacing:-.02em;line-height:1.12;color:var(--ink)}
.tile h1{font-size:96px;max-width:880px}
.tile.long h1{font-size:86px}
.sub{font-size:40px;line-height:1.4;color:var(--muted);margin-top:40px;max-width:860px}
.num{font-family:Inter;font-weight:700;font-size:40px;color:var(--accent);margin-bottom:22px}
.point h1{font-size:78px}
.point.long h1{font-size:68px}
.text{font-size:40px;line-height:1.45;color:var(--muted);margin-top:34px;max-width:870px}
.text b{color:var(--ink);font-weight:600}
.list h1{font-size:78px;margin-bottom:46px}
ul{list-style:none}
li{font-size:39px;line-height:1.3;color:var(--ink);font-weight:500;padding:20px 0 20px 58px;position:relative;border-top:2px solid var(--rule)}
li:last-child{border-bottom:2px solid var(--rule)}
li:before{content:"";position:absolute;left:4px;top:50%;width:18px;height:18px;margin-top:-9px;border-radius:50%;border:4px solid var(--accent)}
.dense li{font-size:34px;padding:15px 0 15px 56px}
.single ul{margin-top:48px}
.single li{font-size:36px;padding:17px 0 17px 56px}
.foot{margin-top:40px;font-family:Manrope;font-weight:800;font-size:38px;color:var(--accent)}
.cta h1{font-size:92px}
.cta.long h1{font-size:80px}
.lines{margin-top:52px}
.lines div{font-family:Manrope;font-weight:700;font-size:42px;padding:18px 0;color:var(--ink);border-top:2px solid var(--rule)}
.bottom{display:flex;justify-content:space-between;align-items:center;height:50px}
.fmt{font-size:30px;font-weight:500;color:var(--fmt)}
"""

LIGHT = dict(ink="#00154D", muted="#46557A", accent="#0E53C5", kick="#6B7899", fmt="#7F8BA8",
             rule="rgba(0,21,77,.12)", ring="#0E53C5")
DARK = dict(ink="#FFFFFF", muted="rgba(255,255,255,.8)", accent="#A9C6FF", kick="rgba(255,255,255,.66)",
            fmt="rgba(255,255,255,.62)", rule="rgba(255,255,255,.22)", ring="#FFFFFF")


def e(s):
    """Escape, but keep the handful of inline tags the copy uses on purpose."""
    out = html.escape(s, quote=False)
    for tag in ("br", "b", "/b", "i", "/i"):
        out = out.replace(f"&lt;{tag}&gt;", f"<{tag}>")
    return out


def plain_len(s):
    return len(s.replace("<br>", " "))


def slide_html(post, idx, slide):
    v = DARK if post["bg"] == "gradient" else LIGHT
    t = slide["t"]

    # Slide 1 is the plan's grid tile: its topic, word for word, as the headline.
    if idx == 0:
        cls = "tile" + (" long" if len(post["topic"]) > 40 else "")
        inner = f"<h1>{e(post['topic'])}</h1>"
        if t == "single":
            cls += " single"
            inner += f'<p class="sub">{e(slide["sub"])}</p>'
            if slide.get("items"):
                inner += "<ul>" + "".join(f"<li>{e(i)}</li>" for i in slide["items"]) + "</ul>"
            if slide.get("foot"):
                inner += f'<div class="foot">{e(slide["foot"])}</div>'
    elif t == "point":
        cls = "point" + (" long" if plain_len(slide["title"]) > 30 else "")
        inner = f'<div class="num">{slide["n"]}</div>' if slide.get("n") else ""
        inner += f"<h1>{e(slide['title'])}</h1><p class=\"text\">{e(slide['body'])}</p>"
    elif t == "list":
        cls = "list"
        dense = ' class="dense"' if len(slide["items"]) > 5 else ""
        inner = f"<h1>{e(slide['title'])}</h1><ul{dense}>" + "".join(
            f"<li>{e(i)}</li>" for i in slide["items"]) + "</ul>"
    elif t == "cta":
        cls = "cta" + (" long" if plain_len(slide["title"]) > 26 else "")
        inner = f"<h1>{e(slide['title'])}</h1>"
        if slide.get("sub"):
            inner += f'<p class="sub">{e(slide["sub"])}</p>'
        if slide.get("lines"):
            inner += '<div class="lines">' + "".join(f"<div>{e(l)}</div>" for l in slide["lines"]) + "</div>"
    else:
        raise ValueError(f"day {post['day']}: {t} slide can't be an inner slide")

    return f"""<!doctype html><html><head><meta charset="utf-8"><style>
:root{{--bg:{BG[post['bg']]};--ink:{v['ink']};--muted:{v['muted']};--accent:{v['accent']};--kick:{v['kick']};
--fmt:{v['fmt']};--rule:{v['rule']}}}
{CSS}</style></head><body>
<div class="frame">
  <div class="body {cls}">{inner}</div>
  <div class="bottom"><span></span>{RING.format(c=v['ring'])}</div>
</div></body></html>"""


def render(post):
    os.makedirs(os.path.join(ROOT, "render"), exist_ok=True)
    os.makedirs(os.path.join(ROOT, "media"), exist_ok=True)
    out = []
    for i, s in enumerate(post["slides"]):
        name = f"d{post['day']:02d}-{i + 1}"
        hp = os.path.join(ROOT, "render", name + ".html")
        png = os.path.join(ROOT, "render", name + ".png")
        jpg = os.path.join(ROOT, "media", name + ".jpg")
        with open(hp, "w", encoding="utf-8") as f:
            f.write(slide_html(post, i, s))
        subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                        "--force-device-scale-factor=1", f"--window-size={W},{H}",
                        "--virtual-time-budget=3000", f"--screenshot={png}", "file://" + hp],
                       check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(["sips", "-s", "format", "jpeg", "-s", "formatOptions", "92", png, "--out", jpg],
                       check=True, stdout=subprocess.DEVNULL)
        out.append(jpg)
    return out


def main():
    only = None
    if "--day" in sys.argv:
        only = int(sys.argv[sys.argv.index("--day") + 1])
    for p in POSTS:
        if only and p["day"] != only:
            continue
        files = render(p)
        print(f"day {p['day']:02d}: {len(files)} slide(s)")


if __name__ == "__main__":
    main()
