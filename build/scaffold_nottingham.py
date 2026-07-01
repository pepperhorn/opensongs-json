#!/usr/bin/env python3
"""Create songs/<id>/metadata.json for every entry in build/nottingham_queue.json.
Idempotent: writes metadata.json but never touches an existing song.abc.
Mirrors scaffold.py but maps the Nottingham queue schema onto metadata.json."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
q = json.loads((ROOT / "build" / "nottingham_queue.json").read_text())

DEFAULT_INSTRUMENTS = ["keyboard", "recorder", "violin", "glockenspiel"]
# collection -> extra descriptive tags
COLL_TAGS = {
    "xmas": ["christmas"],
    "playford": ["english-country-dance", "playford"],
    "waltzes": ["waltz"],
    "jigs": ["jig", "irish"],
    "reels": ["reel", "irish"],
}

made = 0
for c in q["candidates"]:
    d = ROOT / "songs" / c["id"]
    d.mkdir(parents=True, exist_ok=True)
    coll = c.get("source_collection", "")
    tags = [c["category"]] + COLL_TAGS.get(coll, []) + ["beginner"]
    # de-dupe while preserving order
    tags = list(dict.fromkeys(tags))
    meta = {
        "id": c["id"],
        "title": c["title"],
        "composer": c.get("composer", "Traditional"),
        "copyright": {"status": "public-domain", "notes": c.get("pd_note", "")},
        "tags": tags,
        "difficulty": c.get("difficulty", 2),
        "category": c["category"],
        "instrumentsSuited": DEFAULT_INSTRUMENTS,
        "chords": [],
    }
    (d / "metadata.json").write_text(json.dumps(meta, indent=2) + "\n")
    made += 1

print(f"scaffolded {made} nottingham song dirs")
