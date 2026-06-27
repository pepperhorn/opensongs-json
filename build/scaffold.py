#!/usr/bin/env python3
"""Create songs/<id>/metadata.json for every entry in build/songlist.json.
Idempotent: rewrites metadata.json but never touches an existing song.abc."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
songs = json.loads((ROOT / "build" / "songlist.json").read_text())

for s in songs:
    d = ROOT / "songs" / s["id"]
    d.mkdir(parents=True, exist_ok=True)
    meta = {
        "id": s["id"],
        "title": s["title"],
        "composer": s["composer"],
        "copyright": s.get("copyright", {"status": "public-domain", "notes": ""}),
        "tags": s["tags"],
        "difficulty": s["difficulty"],
        "category": s["category"],
        "instrumentsSuited": s["instrumentsSuited"],
        "chords": s.get("chords", []),
    }
    (d / "metadata.json").write_text(json.dumps(meta, indent=2) + "\n")

print(f"scaffolded {len(songs)} song dirs")
