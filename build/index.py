#!/usr/bin/env python3
"""Build the top-level index.json manifest from every songs/<id>/song.json."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Core-100 ordering first (from songlist.json), then any remaining song dirs
# (jazz/classical queue songs) appended alphabetically, so the manifest covers
# every built song.json rather than only the original songlist.
core = [s["id"] for s in json.loads((ROOT / "build" / "songlist.json").read_text())]
core_set = set(core)
extra = sorted(d.name for d in (ROOT / "songs").iterdir()
               if d.is_dir() and (d / "song.json").exists() and d.name not in core_set)
order = core + extra

entries = []
for sid in order:
    p = ROOT / "songs" / sid / "song.json"
    if not p.exists():
        print(f"  (skip, no song.json) {sid}")
        continue
    s = json.loads(p.read_text())
    entries.append({
        "id": s["id"],
        "title": s["title"],
        "composer": s["composer"],
        "category": (json.loads(mp.read_text()).get("category")
                     if (mp := ROOT / "songs" / sid / "metadata.json").exists() else None),
        "difficulty": s["difficulty"],
        "tags": s["tags"],
        "key": s["key"],
        "timeSignature": s["timeSignature"],
        "noteRange": s["noteRange"],
        "noteCount": sum(1 for e in s["events"] if e["type"] == "note"),
        "instrumentsSuited": s["instrumentsSuited"],
        "copyright": s["copyright"]["status"],
        "files": {
            "song": f"songs/{sid}/song.json",
            "abc": f"songs/{sid}/song.abc",
            "musicxml": f"songs/{sid}/song.musicxml",
        },
    })

index = {
    "name": "opensongs-json",
    "description": "Public-domain beginner melodies as ABC, MusicXML, and normalized song.json.",
    "license": "CC0-1.0 (data) — all melodies are public domain",
    "count": len(entries),
    "schemaVersion": 1,
    "songs": entries,
}
(ROOT / "index.json").write_text(json.dumps(index, indent=2) + "\n")
print(f"wrote index.json with {len(entries)} songs")
