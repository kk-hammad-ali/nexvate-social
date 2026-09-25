#!/usr/bin/env python3
"""Publish any NEXVATE post that is due to Instagram (and Facebook as a fallback).

Runs on GitHub Actions at each posting slot. Facebook posts are normally handed
to Facebook's own scheduler in advance by schedule_facebook.py, which records
an fb_post_id - a post with one is treated as "Facebook handled" and only the
Instagram half is published here. A post without one is posted to both, so a
forgotten Facebook schedule degrades to a cron post rather than a missing one.

Adapted from ~/mistorganics-social/scripts/publish.py (same flows, same
one-record-per-post state that makes duplicates impossible on retry).

Instagram CAROUSEL: child container per image -> parent CAROUSEL -> publish.
Instagram IMAGE:    one container -> publish.
Facebook album:     each photo unpublished to /photos, then one /feed post.
Facebook photo:     one /photos call.
Instagram STORY:    one STORIES container -> publish.
Facebook story:     photo uploaded unpublished -> /photo_stories.

Stories come from schedule.json "stories". Only auto ones are sent; a "push"
story waits until its feed post is live on Instagram, so a failed post never
gets a "New on the feed" frame pointing at nothing. Highlights can't be set
through the API, so they're added by hand from the Story archive.

Environment:
  META_ACCESS_TOKEN   required - Social-Up system user token
  GRAPH_VERSION       optional - defaults to v23.0
  DRY_RUN=1           report what would publish, publish nothing
  PAUSED=1            hold everything

Usage:
  python3 scripts/publish.py --validate
  DRY_RUN=1 python3 scripts/publish.py
  python3 scripts/publish.py
  python3 scripts/publish.py --post nx-d01   # force one post now
  python3 scripts/publish.py --story nx-s02-push   # post one Story now (e.g. after a Reel)
"""

import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VERSION = os.environ.get("GRAPH_VERSION", "v23.0") or "v23.0"
GRAPH = f"https://graph.facebook.com/{VERSION}"
TOKEN = os.environ.get("META_ACCESS_TOKEN", "").strip()
DRY = os.environ.get("DRY_RUN", "") not in ("", "0", "false")
PAUSED = os.environ.get("PAUSED", "") not in ("", "0", "false")

# Due now or within this window. Older than this is skipped, not fired late.
GRACE = timedelta(hours=3)
CAPTION_LIMIT = 2200


def api(path, params=None, data=None, timeout=120, token=None):
    tok = token or TOKEN
    url = f"{GRAPH}/{path.lstrip('/')}"
    body = None
    if data is not None:
        payload = dict(data)
        payload["access_token"] = tok
        body = urllib.parse.urlencode(payload).encode()
    else:
        params = dict(params or {})
        params["access_token"] = tok
        url += "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, data=body, method="POST" if body else "GET")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        detail = e.read().decode(errors="replace")
        raise RuntimeError(f"Graph API {e.code} on {path}: {detail}") from None


_PAGE_TOKENS = {}


def page_token(page_id):
    if page_id not in _PAGE_TOKENS:
        _PAGE_TOKENS[page_id] = api(page_id, {"fields": "access_token"})["access_token"]
    return _PAGE_TOKENS[page_id]


def wait_ready(cid, timeout=300):
    deadline = time.time() + timeout
    delay = 3
    while time.time() < deadline:
        st = api(cid, {"fields": "status_code,status"})
        code = st.get("status_code")
        if code == "FINISHED":
            return
        if code in ("ERROR", "EXPIRED"):
            raise RuntimeError(f"container {cid} -> {code}: {st.get('status')}")
        time.sleep(delay)
        delay = min(delay * 1.5, 20)
    raise RuntimeError(f"container {cid} not ready after {timeout}s")


def media_publish(ig, cid, tries=5):
    """Instagram can report FINISHED and still refuse the publish (9007) for a few seconds."""
    for n in range(tries):
        try:
            return api(f"{ig}/media_publish", data={"creation_id": cid})["id"]
        except RuntimeError as exc:
            if '"code":9007' not in str(exc) or n == tries - 1:
                raise
            time.sleep(10 * (n + 1))


def publish_instagram(e):
    ig = e["ig_user_id"]
    if e["media_type"] == "CAROUSEL":
        children = [api(f"{ig}/media", data={"image_url": u, "is_carousel_item": "true"})["id"]
                    for u in e["media"]]
        for c in children:
            wait_ready(c)
        cid = api(f"{ig}/media", data={"media_type": "CAROUSEL", "children": ",".join(children),
                                       "caption": e["caption_ig"]})["id"]
    else:
        cid = api(f"{ig}/media", data={"image_url": e["media"][0], "caption": e["caption_ig"]})["id"]
    wait_ready(cid)
    return media_publish(ig, cid)


def publish_facebook(e):
    page = e["fb_page_id"]
    tok = page_token(page)
    if len(e["media"]) == 1:
        res = api(f"{page}/photos", data={"url": e["media"][0], "caption": e["caption_fb"],
                                          "published": "true"}, token=tok)
        return res.get("post_id") or res["id"]
    fbids = [api(f"{page}/photos", data={"url": u, "published": "false"}, token=tok)["id"]
             for u in e["media"]]
    data = {"message": e["caption_fb"]}
    for n, fbid in enumerate(fbids):
        data[f"attached_media[{n}]"] = json.dumps({"media_fbid": fbid})
    res = api(f"{page}/feed", data=data, token=tok)
    return res.get("post_id") or res["id"]


def publish_ig_story(s):
    ig = s["ig_user_id"]
    cid = api(f"{ig}/media", data={"media_type": "STORIES", "image_url": s["media"]})["id"]
    wait_ready(cid)
    return media_publish(ig, cid)


def publish_fb_story(s):
    page = s["fb_page_id"]
    tok = page_token(page)
    photo = api(f"{page}/photos", data={"url": s["media"], "published": "false"}, token=tok)["id"]
    res = api(f"{page}/photo_stories", data={"photo_id": photo}, token=tok)
    return res.get("post_id") or res.get("id") or photo


def run_stories(sched, published, pub_path, now, by_post):
    recs = published.setdefault("stories", [])
    by_id = {r["id"]: r for r in recs}
    forced = sys.argv[sys.argv.index("--story") + 1] if "--story" in sys.argv else None
    due = []
    for s in sched.get("stories", []):
        rec = by_id.get(s["id"], {})
        want = [t for t in ("ig", "fb") if not rec.get(f"{t}_story_id")]
        if not want:
            continue
        if forced:
            if s["id"] == forced:
                due.append((s, want))
            continue
        if not s["auto"]:
            continue
        when = datetime.strptime(s["publish_at_utc"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
        if when > now or now - when > GRACE:
            continue
        if s["after"] and not by_post.get(s["after"], {}).get("ig_media_id"):
            print(f"WAIT  {s['id']}: {s['after']} isn't live on Instagram yet")
            continue
        due.append((s, want))
    if not due:
        return 0
    if PAUSED:
        print(f"PAUSED - {len(due)} story(s) due and held")
        return 0
    if DRY:
        for s, want in due:
            print(f"DRY   {s['id']} -> {'+'.join(want)} story")
        return 0
    failures = 0
    for s, want in due:
        rec = by_id.get(s["id"])
        if rec is None:
            rec = {"id": s["id"], "highlight": s["highlight"], "scheduled_gst": s["publish_at_gst"]}
            by_id[s["id"]] = rec
            recs.append(rec)
        for t in want:
            try:
                rec[f"{t}_story_id"] = publish_ig_story(s) if t == "ig" else publish_fb_story(s)
                rec[f"{t}_published_utc"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
                print(f"OK    {s['id']} -> {t} story {rec[f'{t}_story_id']}")
            except Exception as exc:
                failures += 1
                print(f"FAIL  {s['id']} [{t} story]: {exc}", file=sys.stderr)
        save(published, pub_path)
    return failures


def load():
    with open(os.path.join(ROOT, "state", "schedule.json"), encoding="utf-8") as f:
        sched = json.load(f)
    pub_path = os.path.join(ROOT, "state", "published.json")
    published = {"posts": []}
    if os.path.exists(pub_path):
        with open(pub_path, encoding="utf-8") as f:
            published = json.load(f)
    return sched, published, pub_path


def save(published, pub_path):
    with open(pub_path, "w", encoding="utf-8") as f:
        json.dump(published, f, indent=2, ensure_ascii=False)
        f.write("\n")


def validate(sched):
    bad = 0
    for e in sched["posts"]:
        probs = []
        for k in ("caption_ig", "caption_fb"):
            if len(e[k]) > CAPTION_LIMIT:
                probs.append(f"{k} is {len(e[k])} chars")
            if "{" in e[k]:
                probs.append(f"{k} has an unresolved placeholder")
            tags = [w for w in e[k].split() if w.startswith("#")]
            if len(tags) != 5:
                probs.append(f"{k} has {len(tags)} hashtags, want 5")
        n = len(e["media"])
        if e["media_type"] == "CAROUSEL" and not 2 <= n <= 10:
            probs.append(f"carousel has {n} images")
        for p in probs:
            bad += 1
            print(f"FAIL  {e['id']}: {p}", file=sys.stderr)
        if not probs:
            print(f"ok    {e['id']}  {e['publish_at_gst']}  {e['media_type']:<8} {n:>2} img")
    for st in sched.get("stories", []):
        if not st["media"].endswith(".jpg"):
            bad += 1
            print(f"FAIL  {st['id']}: media is not a JPEG", file=sys.stderr)
    print(f"ok    {len(sched.get('stories', []))} stories")
    print("\nall valid" if not bad else f"\n{bad} problem(s)")
    return 1 if bad else 0


def main():
    sched, published, pub_path = load()
    if "--validate" in sys.argv:
        return validate(sched)
    by_id = {r["id"]: r for r in published["posts"]}
    forced = sys.argv[sys.argv.index("--post") + 1] if "--post" in sys.argv else None
    now = datetime.now(timezone.utc)

    due, todo = [], {}
    for e in sched["posts"]:
        rec = by_id.get(e["id"], {})
        want = [t for t, k in (("ig", "ig_media_id"), ("fb", "fb_post_id")) if not rec.get(k)]
        if not want:
            continue
        if forced:
            if e["id"] == forced:
                due.append(e)
                todo[e["id"]] = want
            continue
        when = datetime.strptime(e["publish_at_utc"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
        if when > now:
            continue
        if now - when > GRACE:
            print(f"SKIP  {e['id']} [{'+'.join(want)}] was due {e['publish_at_gst']} GST, outside the grace window")
            continue
        due.append(e)
        todo[e["id"]] = want

    if "--story" in sys.argv:
        due = []
    if not TOKEN and not DRY:
        print("META_ACCESS_TOKEN is not set", file=sys.stderr)
        return 1
    if PAUSED:
        print(f"PAUSED - {len(due)} post(s) due and held")
        due = []
    elif not due:
        print(f"no posts due at {now:%Y-%m-%d %H:%M} UTC")
    elif DRY:
        for e in due:
            print(f"DRY   {e['id']} -> {'+'.join(todo[e['id']])} ({e['media_type']}, {len(e['media'])} img)")
        due = []

    failures = 0
    for e in due:
        rec = by_id.get(e["id"])
        fresh = rec is None
        if fresh:
            rec = {"id": e["id"], "media_type": e["media_type"], "images": len(e["media"]),
                   "scheduled_gst": e["publish_at_gst"]}
        for target in todo[e["id"]]:
            try:
                stamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
                if target == "ig":
                    rec["ig_media_id"] = publish_instagram(e)
                    rec["ig_published_utc"] = stamp
                    print(f"OK    {e['id']} -> @nexvate.ae media {rec['ig_media_id']}")
                else:
                    rec["fb_post_id"] = publish_facebook(e)
                    rec["fb_published_utc"] = stamp
                    print(f"OK    {e['id']} -> fb post {rec['fb_post_id']}")
                if fresh:
                    by_id[e["id"]] = rec
                    published["posts"].append(rec)
                    fresh = False
            except Exception as exc:  # one bad post must not stall the queue
                failures += 1
                print(f"FAIL  {e['id']} [{target}]: {exc}", file=sys.stderr)
        save(published, pub_path)
    failures += run_stories(sched, published, pub_path, now, by_id)
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
