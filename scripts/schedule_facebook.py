#!/usr/bin/env python3
"""Hand NEXVATE feed posts to Facebook's own scheduler.

Each post is created on the Page unpublished, with scheduled_publish_time set
to its slot, so Facebook publishes it itself. The returned id is saved as
fb_post_id in state/published.json. publish.py then skips the Facebook half,
and a post that never got scheduled here falls back to a cron post.

Facebook only accepts schedule times 10 minutes to 30 days out. Anything
further away is left for a later run. The GitHub workflow runs this daily, so
later posts are picked up once they're in range.

Single photo: /photos with published=false + scheduled_publish_time.
Album:        each photo to /photos (published=false, temporary=true), then
              one /feed post with attached_media and the schedule time.

Usage:
  python3 scripts/schedule_facebook.py            # dry run: what would be scheduled
  python3 scripts/schedule_facebook.py --apply    # schedule everything in range
  python3 scripts/schedule_facebook.py --list     # Facebook's scheduled posts for the Page
  python3 scripts/schedule_facebook.py --cancel nx-d05
"""

import json
import os
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from publish import GRAPH, TOKEN, api, load, page_token, save  # noqa: E402

MIN_LEAD = timedelta(minutes=20)
MAX_LEAD = timedelta(days=29, hours=12)


def schedule(e, when):
    page = e["fb_page_id"]
    tok = page_token(page)
    ts = str(int(when.timestamp()))
    if len(e["media"]) == 1:
        res = api(f"{page}/photos", data={"url": e["media"][0], "caption": e["caption_fb"], "published": "false",
                                          "scheduled_publish_time": ts}, token=tok)
        return res.get("post_id") or res["id"]
    fbids = [api(f"{page}/photos", data={"url": u, "published": "false", "temporary": "true"}, token=tok)["id"]
             for u in e["media"]]
    data = {"message": e["caption_fb"], "published": "false", "scheduled_publish_time": ts}
    for n, fbid in enumerate(fbids):
        data[f"attached_media[{n}]"] = json.dumps({"media_fbid": fbid})
    return api(f"{page}/feed", data=data, token=tok)["id"]


def delete(obj, tok):
    url = f"{GRAPH}/{obj}?" + urllib.parse.urlencode({"access_token": tok})
    with urllib.request.urlopen(urllib.request.Request(url, method="DELETE"), timeout=60) as r:
        return json.loads(r.read().decode())


def main():
    sched, published, pub_path = load()
    if not TOKEN:
        print("META_ACCESS_TOKEN is not set", file=sys.stderr)
        return 1
    page = sched["posts"][0]["fb_page_id"]
    by_id = {r["id"]: r for r in published["posts"]}

    if "--list" in sys.argv:
        tok = page_token(page)
        res = api(f"{page}/scheduled_posts", {"fields": "id,message,scheduled_publish_time", "limit": 100}, token=tok)
        for p in res.get("data", []):
            print(f"{p['id']}  {p.get('scheduled_publish_time')}  {(p.get('message') or '')[:60]!r}")
        print(f"{len(res.get('data', []))} scheduled on Facebook")
        return 0

    if "--cancel" in sys.argv:
        pid = sys.argv[sys.argv.index("--cancel") + 1]
        rec = by_id.get(pid)
        if not rec or not rec.get("fb_post_id") or rec.get("fb_published_utc"):
            print(f"{pid} has no pending Facebook schedule", file=sys.stderr)
            return 1
        delete(rec["fb_post_id"], page_token(page))
        for k in ("fb_post_id", "fb_scheduled_utc"):
            rec.pop(k, None)
        save(published, pub_path)
        print(f"cancelled {pid}")
        return 0

    apply = "--apply" in sys.argv
    now = datetime.now(timezone.utc)
    failures = 0
    for e in sched["posts"]:
        rec = by_id.get(e["id"], {})
        if rec.get("fb_post_id"):
            continue
        when = datetime.strptime(e["publish_at_utc"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
        if when - now < MIN_LEAD:
            continue   # too close or past: publish.py posts it at the slot
        if when - now > MAX_LEAD:
            print(f"LATER {e['id']}  {e['publish_at_gst']} GST, beyond Facebook's 30-day limit")
            continue
        if not apply:
            print(f"WOULD {e['id']}  {e['publish_at_gst']} GST  {len(e['media'])} img")
            continue
        try:
            fid = schedule(e, when)
        except Exception as exc:
            failures += 1
            print(f"FAIL  {e['id']}: {exc}", file=sys.stderr)
            continue
        if e["id"] not in by_id:
            rec = {"id": e["id"], "media_type": e["media_type"], "images": len(e["media"]),
                   "scheduled_gst": e["publish_at_gst"]}
            by_id[e["id"]] = rec
            published["posts"].append(rec)
        rec = by_id[e["id"]]
        rec["fb_post_id"] = fid
        rec["fb_scheduled_utc"] = now.strftime("%Y-%m-%dT%H:%M:%SZ")
        save(published, pub_path)
        print(f"OK    {e['id']} scheduled on Facebook for {e['publish_at_gst']} GST ({fid})")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
