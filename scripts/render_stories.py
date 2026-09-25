#!/usr/bin/env python3
"""Render the 9:16 assets: daily Stories, Reel covers and Highlight covers.

  media/stories/sXX-am.jpg     09:00 Highlight frame (content/stories.py AM)
  media/stories/sXX-push.jpg   "New on the feed" frame, uses media/dXX-1.jpg
  media/stories/sXX-ask.jpg    days 7 and 19, background for the poll/quiz sticker
  media/reels/rXX-cover.jpg    Reel cover in the grid tile design
  media/highlights/<name>.jpg  Highlight covers, set by hand in the app

Same pipeline and brand rules as render.py. Run render.py first, because the
push frames embed the feed tiles.

Story safe area: Instagram draws the profile bar over the top ~250px and the
reply bar over the bottom ~340px, so nothing important goes there. Reel covers
are cropped to a centred 3:4 on the profile grid, so the tile sits in the
middle 1440px.

Usage: python3 scripts/render_stories.py
"""

import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "content"))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
from posts import FEED_DAYS, POSTS, REELS  # noqa: E402
from render import BG, CHROME, CSS, DARK, LIGHT, RING, e  # noqa: E402
from stories import AM, ASK, HIGHLIGHTS  # noqa: E402

W, H = 1080, 1920

STORY_CSS = CSS.replace("height:1350px", "height:1920px").replace("../assets/", "../../assets/").replace(
    "../fonts/", "../../fonts/") + """
.story{padding:300px 96px 380px}
.story .body{padding-top:0;justify-content:center;padding-bottom:80px}
.story h1{font-size:104px;max-width:890px}
.story h1.long{font-size:90px}
.story .text{font-size:46px;margin-top:48px}
.story ul{margin-top:56px}
.story li{font-size:42px;padding:26px 0 26px 60px}
.story .foot{font-size:44px;margin-top:52px}
.story .fmt{font-size:34px}
.reel{padding:352px 96px 340px}
.push .body{align-items:center;justify-content:center;padding-top:0}
.push h1{font-size:92px;text-align:center;margin-bottom:64px}
.card{width:720px;height:900px;border-radius:32px;overflow:hidden;box-shadow:0 40px 90px rgba(0,10,40,.45)}
.card img{width:100%;height:100%;object-fit:cover;display:block}
.hint{margin-top:60px;font-size:40px;color:var(--muted);text-align:center}
.ask .vote{margin-top:80px;font-family:Manrope;font-weight:800;font-size:46px;color:var(--accent)}
"""

# Highlights get their own tint so each group reads as a set.
HL_BG = {"About": "cloud", "Services": "powder", "Tips": "cloud", "Process": "sky", "Work": "sky", "Book": "gradient"}

ICON = {
    "About": '<circle cx="80" cy="56" r="26"/><path d="M30 138c6-30 26-44 50-44s44 14 50 44"/>',
    "Services": '<rect x="28" y="28" width="46" height="46" rx="10"/><rect x="86" y="28" width="46" height="46" rx="10"/>'
                '<rect x="28" y="86" width="46" height="46" rx="10"/><rect x="86" y="86" width="46" height="46" rx="10"/>',
    "Tips": '<path d="M56 104c-14-10-22-24-22-40a46 46 0 0 1 92 0c0 16-8 30-22 40v14H56z"/><path d="M60 138h40"/>',
    "Process": '<circle cx="34" cy="80" r="14"/><circle cx="80" cy="80" r="14"/><circle cx="126" cy="80" r="14"/>'
               '<path d="M48 80h18M94 80h18"/>',
    "Work": '<rect x="22" y="34" width="116" height="76" rx="10"/><path d="M58 136h44M80 110v26"/>',
    "Book": '<rect x="26" y="38" width="108" height="98" rx="12"/><path d="M26 70h108M56 24v28M104 24v28"/>',
}


def page(bg, body, frame_cls):
    v = DARK if bg == "gradient" else LIGHT
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>
:root{{--bg:{BG[bg]};--ink:{v['ink']};--muted:{v['muted']};--accent:{v['accent']};--kick:{v['kick']};
--fmt:{v['fmt']};--rule:{v['rule']}}}
{STORY_CSS}</style></head><body><div class="frame {frame_cls}">{body.replace('{RING}', RING.format(c=v['ring']))}</div></body></html>"""


def shoot(html_doc, name, sub):
    rdir = os.path.join(ROOT, "render", sub)
    mdir = os.path.join(ROOT, "media", sub)
    os.makedirs(rdir, exist_ok=True)
    os.makedirs(mdir, exist_ok=True)
    hp, png, jpg = (os.path.join(rdir, name + ".html"), os.path.join(rdir, name + ".png"),
                    os.path.join(mdir, name + ".jpg"))
    with open(hp, "w", encoding="utf-8") as f:
        f.write(html_doc)
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--allow-file-access-from-files",
                    "--force-device-scale-factor=1", f"--window-size={W},{H}", "--virtual-time-budget=3000",
                    f"--screenshot={png}", "file://" + hp],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(["sips", "-s", "format", "jpeg", "-s", "formatOptions", "92", png, "--out", jpg],
                   check=True, stdout=subprocess.DEVNULL)
    return jpg


def bottom(label):
    return f'<div class="bottom"><span class="fmt">{e(label)}</span>{{RING}}</div>'


def am_frame(day, s):
    long = " long" if len(s["title"].replace("<br>", " ")) > 30 else ""
    inner = f'<h1 class="{long.strip()}">{e(s["title"])}</h1>'
    if s.get("body"):
        inner += f'<p class="text">{e(s["body"])}</p>'
    if s.get("items"):
        inner += "<ul>" + "".join(f"<li>{e(i)}</li>" for i in s["items"]) + "</ul>"
    if s.get("foot"):
        inner += f'<div class="foot">{e(s["foot"])}</div>'
    body = f'<div class="kicker">{e(s["kicker"])}</div><div class="body">{inner}</div>' + bottom("nexvate.ae")
    return shoot(page(HL_BG[s["hl"]], body, "story"), f"s{day:02d}-am", "stories")


def push_frame(day):
    reel = day in REELS
    img = f"../../media/reels/r{day:02d}-cover.jpg" if reel else f"../../media/d{day:02d}-1.jpg"
    head = "New reel." if reel else "New on the feed."
    body = (f'<div class="body"><h1>{head}</h1>'
            f'<div class="card"><img src="{img}"></div><p class="hint">Tap @nexvate.ae to see it</p></div>'
            + bottom("nexvate.ae"))
    return shoot(page("gradient", body, "story push"), f"s{day:02d}-push", "stories")


def ask_frame(day, a):
    body = (f'<div class="kicker">{a["kind"]}</div><div class="body ask">'
            f'<h1>{e(a["title"])}</h1><div class="vote">{"Vote" if a["kind"] == "Poll" else "Take a guess"} ↓</div></div>'
            + bottom("nexvate.ae"))
    return shoot(page("sky", body, "story"), f"s{day:02d}-ask", "stories")


def reel_cover(r):
    long = " long" if len(r["topic"]) > 40 else ""
    body = (f'<div class="body tile{long}"><h1>{e(r["topic"])}</h1></div>'
            + '<div class="bottom"><span></span>{RING}</div>')
    return shoot(page(r["bg"], body, "reel"), f"r{r['day']:02d}-cover", "reels")


def highlight_cover(name):
    c = "#FFFFFF"
    svg = (f'<svg width="420" height="420" viewBox="0 0 420 420"><circle cx="210" cy="210" r="190" fill="none" '
           f'stroke="{c}" stroke-width="16"/><g transform="translate(90 90) scale(1.5)" fill="none" stroke="{c}" '
           f'stroke-width="9" stroke-linecap="round" stroke-linejoin="round">{ICON[name]}</g></svg>')
    doc = f"""<!doctype html><html><head><style>*{{margin:0}}html,body{{width:{W}px;height:{H}px}}
body{{background:{BG['gradient']};display:flex;align-items:center;justify-content:center}}</style></head>
<body>{svg}</body></html>"""
    return shoot(doc, name.lower(), "highlights")


def main():
    for r in REELS.values():
        reel_cover(r)
    print(f"reel covers: {len(REELS)}")
    for day in range(1, 31):
        am_frame(day, AM[day])
        if day in FEED_DAYS:
            push_frame(day)
        if day in ASK:
            ask_frame(day, ASK[day])
    print("stories: days 1-30")
    for n in HIGHLIGHTS:
        highlight_cover(n)
    print(f"highlight covers: {len(HIGHLIGHTS)}")


if __name__ == "__main__":
    main()
