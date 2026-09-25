#!/usr/bin/env python3
"""Take down already-published feed posts and publish them again with the current media.

For each id, in the order given: delete the Instagram media and the Facebook
post, clear its record in state/published.json, then publish it again on both.
Used when the design changes after a post has gone live.

Instagram only lets the API delete media on some accounts. If the delete is
refused, the old post is left up, the id is reported, and nothing is
republished for it, so the grid never shows the same post twice.

Usage: python3 scripts/replace.py nx-d01,nx-d03,nx-d04
"""

import os
import sys
import urllib.error
import urllib.parse
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from publish import (GRAPH, TOKEN, load, page_token, publish_facebook,  # noqa: E402
                     publish_instagram, save)
from datetime import datetime, timezone  # noqa: E402


def delete(obj, tok):
    url = f"{GRAPH}/{obj}?" + urllib.parse.urlencode({"access_token": tok})
    try:
        with urllib.request.urlopen(urllib.request.Request(url, method="DELETE"), timeout=60) as r:
            return r.read().decode()
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"Graph API {e.code} deleting {obj}: {e.read().decode(errors='replace')}") from None


def main():
    if not TOKEN:
        print("META_ACCESS_TOKEN is not set", file=sys.stderr)
        return 1
    ids = [i for i in sys.argv[1].split(",") if i]
    sched, published, pub_path = load()
    entries = {e["id"]: e for e in sched["posts"]}
    by_id = {r["id"]: r for r in published["posts"]}
    failures = 0
    for pid in ids:
        e, rec = entries[pid], by_id.get(pid)
        if rec is None:
            print(f"FAIL  {pid}: nothing published to replace", file=sys.stderr)
            failures += 1
            continue
        page = e["fb_page_id"]
        if rec.get("ig_media_id"):
            try:
                delete(rec["ig_media_id"], TOKEN)
                print(f"DEL   {pid} instagram {rec['ig_media_id']}")
            except Exception as exc:
                print(f"FAIL  {pid}: {exc}", file=sys.stderr)
                failures += 1
                continue
            for k in ("ig_media_id", "ig_published_utc"):
                rec.pop(k, None)
            save(published, pub_path)
        if rec.get("fb_post_id"):
            fid = rec["fb_post_id"] if "_" in rec["fb_post_id"] else f"{page}_{rec['fb_post_id']}"
            try:
                delete(fid, page_token(page))
                print(f"DEL   {pid} facebook {fid}")
            except Exception as exc:
                print(f"WARN  {pid}: {exc}", file=sys.stderr)
            for k in ("fb_post_id", "fb_published_utc", "fb_scheduled_utc"):
                rec.pop(k, None)
            save(published, pub_path)
    # Republish in the order given, so the grid keeps its order.
    for pid in ids:
        e, rec = entries[pid], by_id.get(pid)
        if rec is None or rec.get("ig_media_id"):
            continue
        for target, fn, key in (("ig", publish_instagram, "ig_media_id"), ("fb", publish_facebook, "fb_post_id")):
            try:
                rec[key] = fn(e)
                rec[f"{target}_published_utc"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
                print(f"OK    {pid} -> {target} {rec[key]}")
            except Exception as exc:
                failures += 1
                print(f"FAIL  {pid} [{target}]: {exc}", file=sys.stderr)
            save(published, pub_path)
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
