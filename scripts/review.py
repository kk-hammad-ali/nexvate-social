#!/usr/bin/env python3
"""Build the review/ folder: contact sheets to check before anything is scheduled.

  00-grid-A.png         the Instagram profile grid on day 30, light sides / dark centre
  00-grid-B.png         the same grid with the alternative, dark sides / light centre
  dayXX.png             every slide of each feed post
  reel-covers.png       the 4 Reel covers
  stories-weekN.png     each day's Story frames (09:00 Highlight frame, post push, poll/quiz)
  highlights.png        Highlight covers and which days go into each

Usage: python3 scripts/review.py   (after render.py and render_stories.py)
"""

import copy
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "content"))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
from posts import FEED_DAYS, POSTS, REELS, grid_bg  # noqa: E402
from render import CHROME, slide_html  # noqa: E402
from stories import AM, ASK, HIGHLIGHTS  # noqa: E402

REV = os.path.join(ROOT, "review")
TMP = os.path.join(ROOT, "render", "review")
BY_DAY = {p["day"]: p for p in POSTS}

SHEET_CSS = """*{margin:0;padding:0;box-sizing:border-box}
body{background:#fff;font-family:-apple-system,Helvetica,sans-serif;color:#0A0A0A;padding:40px}
h2{font-size:30px;margin-bottom:6px}p.note{font-size:20px;color:#555;margin-bottom:28px;max-width:1100px;line-height:1.4}
.row{display:flex;gap:16px;align-items:flex-start;margin-bottom:26px}
.lab{width:150px;font-size:22px;font-weight:700;padding-top:8px}.lab small{display:block;font-weight:400;color:#666;font-size:17px;margin-top:4px}
figure{font-size:16px;color:#555}figure img{display:block;border:1px solid #ddd;border-radius:6px}
figcaption{margin-top:6px}"""


def shoot(html_doc, out, w, h):
    os.makedirs(TMP, exist_ok=True)
    hp = os.path.join(TMP, os.path.basename(out) + ".html")
    with open(hp, "w", encoding="utf-8") as f:
        f.write(html_doc)
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--allow-file-access-from-files",
                    "--force-device-scale-factor=1", f"--window-size={w},{h}", "--virtual-time-budget=4000",
                    f"--screenshot={out}", "file://" + hp],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def src(rel):
    return "file://" + os.path.join(ROOT, rel)


def b_covers():
    """Render slide 1 of each post and each Reel cover with the mode-B colours."""
    out = {}
    for day in FEED_DAYS:
        if day in BY_DAY:
            p = copy.deepcopy(BY_DAY[day])
            p["bg"] = grid_bg(day, p["plan_bg"], "B")
            doc = slide_html(p, 0, p["slides"][0])
            w, h = 1080, 1350
        else:
            r = REELS[day]
            p = dict(day=day, pillar=r["pillar"], topic=r["topic"], bg=grid_bg(day, r["plan_bg"], "B"),
                     slides=[dict(t="cover")])
            doc = slide_html(p, 0, p["slides"][0]).replace("Single", "Reel")
            w, h = 1080, 1350
        doc = doc.replace("../assets/", src("assets") + "/").replace("../fonts/", src("fonts") + "/")
        png = os.path.join(TMP, f"b-{day:02d}.png")
        shoot(doc, png, w, h)
        out[day] = "file://" + png
    return out


def grid(name, title, note, tiles):
    shown = FEED_DAYS[:len(FEED_DAYS) // 3 * 3]   # a whole number of rows
    cells = "".join(
        f'<div class="t"><img src="{tiles[d]}" style="{"object-position:center" if d in REELS else ""}"></div>'
        for d in reversed(shown))
    rows = len(shown) // 3
    tw, th = 360, 480
    doc = f"""<!doctype html><html><head><meta charset="utf-8"><style>{SHEET_CSS}
.g{{display:grid;grid-template-columns:repeat(3,{tw}px);gap:3px;width:{tw * 3 + 6}px}}
.t{{width:{tw}px;height:{th}px;overflow:hidden;background:#eee}}.t img{{width:100%;height:100%;object-fit:cover}}
</style></head><body><h2>{title}</h2><p class="note">{note}</p><div class="g">{cells}</div></body></html>"""
    shoot(doc, os.path.join(REV, name), tw * 3 + 86, rows * (th + 3) + 240)


def feed_tiles():
    t = {}
    for d in FEED_DAYS:
        t[d] = src(f"media/reels/r{d:02d}-cover.jpg") if d in REELS else src(f"media/d{d:02d}-1.jpg")
    return t


def day_sheets():
    for p in POSTS:
        n = len(p["slides"])
        figs = "".join(f'<figure><img src="{src(f"media/d{p["day"]:02d}-{i + 1}.jpg")}" width="360" height="450">'
                       f'<figcaption>d{p["day"]:02d}-{i + 1}.jpg</figcaption></figure>' for i in range(n))
        doc = (f'<!doctype html><html><head><meta charset="utf-8"><style>{SHEET_CSS}</style></head><body>'
               f'<h2>Day {p["day"]:02d} · {p["pillar"]} · {p["topic"]}</h2>'
               f'<p class="note">{"Carousel" if n > 1 else "Single"} · grid tile: {p["bg"]}'
               f'{" (centre stripe)" if p["bg"] == "gradient" else ""}</p><div class="row">{figs}</div></body></html>')
        shoot(doc, os.path.join(REV, f"day{p['day']:02d}.png"), 80 + n * 376, 640)


def reel_sheet():
    figs = "".join(f'<figure><img src="{src(f"media/reels/r{d:02d}-cover.jpg")}" width="300" height="533">'
                   f'<figcaption>Day {d:02d} · r{d:02d}-cover.jpg</figcaption></figure>' for d in REELS)
    doc = (f'<!doctype html><html><head><meta charset="utf-8"><style>{SHEET_CSS}</style></head><body>'
           f'<h2>Reel covers</h2><p class="note">Pick these as the cover when the Reel is posted. The grid shows the '
           f'middle 3:4 of the cover, which is where the tile sits.</p><div class="row">{figs}</div></body></html>')
    shoot(doc, os.path.join(REV, "reel-covers.png"), 80 + 4 * 316, 760)


def story_sheets():
    weeks = [range(1, 8), range(8, 15), range(15, 22), range(22, 31)]
    for wi, days in enumerate(weeks, 1):
        rows = ""
        for d in days:
            figs = (f'<figure><img src="{src(f"media/stories/s{d:02d}-am.jpg")}" width="225" height="400">'
                    f'<figcaption>09:00 · Highlight: <b>{AM[d]["hl"]}</b></figcaption></figure>')
            if d in FEED_DAYS:
                figs += (f'<figure><img src="{src(f"media/stories/s{d:02d}-push.jpg")}" width="225" height="400">'
                         f'<figcaption>after the {"Reel" if d in REELS else "post"} · no Highlight</figcaption></figure>')
            if d in ASK:
                figs += (f'<figure><img src="{src(f"media/stories/s{d:02d}-ask.jpg")}" width="225" height="400">'
                         f'<figcaption>{ASK[d]["kind"]}, posted by hand: {" / ".join(ASK[d]["options"])}'
                         f'</figcaption></figure>')
            rows += f'<div class="row"><div class="lab">Day {d:02d}</div>{figs}</div>'
        doc = (f'<!doctype html><html><head><meta charset="utf-8"><style>{SHEET_CSS}</style></head><body>'
               f'<h2>Stories · week {wi}</h2><div>{rows}</div></body></html>')
        shoot(doc, os.path.join(REV, f"stories-week{wi}.png"), 1060, 90 + len(days) * 470)


def highlight_sheet():
    cols = ""
    for n in HIGHLIGHTS:
        days = [d for d in range(1, 31) if AM[d]["hl"] == n]
        cols += (f'<figure style="width:170px;text-align:center"><div style="width:150px;height:150px;border-radius:50%;'
                 f'overflow:hidden;margin:0 auto;border:3px solid #ddd"><img src="{src(f"media/highlights/{n.lower()}.jpg")}"'
                 f' style="width:150px;height:267px;margin-top:-58px;border:0"></div><figcaption><b style="color:#0A0A0A;'
                 f'font-size:20px">{n}</b><br>days {", ".join(str(d) for d in days)}</figcaption></figure>')
    doc = (f'<!doctype html><html><head><meta charset="utf-8"><style>{SHEET_CSS}</style></head><body>'
           f'<h2>Highlights</h2><p class="note">Each 09:00 Story is saved to one Highlight. Covers are in '
           f'media/highlights/.</p><div class="row">{cols}</div></body></html>')
    shoot(doc, os.path.join(REV, "highlights.png"), 1200, 460)


def main():
    os.makedirs(REV, exist_ok=True)
    for f in os.listdir(REV):
        if f.endswith(".png"):
            os.remove(os.path.join(REV, f))
    tiles = feed_tiles()
    grid("00-grid-A.png", "Option A: light sides, gradient centre (rendered)",
         "The profile after 27 posts (21 Oct), newest top-left. Launch day posts 3, so the grid opens on a full row. The stripe is centred "
         "whenever the grid is whole rows: launch day, then every 3rd post. On the days between it sits one column over.", tiles)
    grid("00-grid-B.png", "Option B: gradient sides, light centre (preview only)",
         "The same grid with the alternative pattern. Two thirds of the tiles are dark.", b_covers())
    day_sheets()
    reel_sheet()
    story_sheets()
    highlight_sheet()
    print("review/ rebuilt")


if __name__ == "__main__":
    main()
