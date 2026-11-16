#!/usr/bin/env python3
"""Create songs/<id>/metadata.json for records in build/pd_interval_queue.json.

Usage: python build/scaffold_queue.py <id> [<id> ...]
Idempotent: (re)writes metadata.json, never touches an existing song.abc."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
QUEUE = ROOT / "build" / "pd_interval_queue.json"
DEFAULT_INSTRUMENTS = ["keyboard", "recorder", "violin", "voice"]


def main(ids):
    q = {r["id"]: r for r in json.loads(QUEUE.read_text())}
    for i in ids:
        r = q[i]
        d = ROOT / "songs" / i
        d.mkdir(parents=True, exist_ok=True)
        meta = {
            "id": i,
            "title": r["title"],
            "composer": r["composer"],
            "copyright": {"status": "public-domain", "notes": r["copyrightNotes"]},
            "tags": r["tags"],
            "difficulty": r.get("difficulty", 2),
            "category": r["category"],
            "instrumentsSuited": DEFAULT_INSTRUMENTS,
            "chords": [],
        }
        (d / "metadata.json").write_text(json.dumps(meta, indent=2, ensure_ascii=False) + "\n")
    print(f"scaffolded {len(ids)} song dirs")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    main(sys.argv[1:])
