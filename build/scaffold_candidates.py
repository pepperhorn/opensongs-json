#!/usr/bin/env python3
"""Create songs/<id>/metadata.json for a wave of Nottingham-candidate records.

Usage: python build/scaffold_candidates.py <wave.json>
where wave.json is a list of candidate records from nottingham_candidates.json
(fields: id, title, type, source_collection, meter, unit, key, ...).
Idempotent: writes metadata.json but never touches an existing song.abc."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

CATEGORY = {"carol": "carol"}  # everything else -> folk
NOTES = {
    "carol": "Traditional carol (pre-1900)",
    "playford": "English country dance (Playford, 1651+); anonymous traditional",
    "morris": "Traditional morris dance tune; anonymous traditional",
    "waltz": "Traditional waltz (pre-1900)",
    "jig": "Traditional Irish jig; anonymous traditional",
    "reel": "Traditional Irish reel; anonymous traditional",
    "hornpipe": "Traditional hornpipe; anonymous traditional",
    "slip-jig": "Traditional slip jig; anonymous traditional",
    "misc": "Traditional tune (pre-1900)",
}
TYPE_TAGS = {
    "carol": ["carol"],
    "playford": ["english-country-dance", "playford"],
    "morris": ["morris", "english"],
    "waltz": ["waltz"],
    "jig": ["jig", "irish"],
    "reel": ["reel", "irish"],
    "hornpipe": ["hornpipe"],
    "slip-jig": ["slip-jig", "irish"],
}
DEFAULT_INSTRUMENTS = ["keyboard", "recorder", "violin", "glockenspiel"]


def main(wave_path):
    wave = json.loads(Path(wave_path).read_text())
    made = 0
    for c in wave:
        t = c["type"]
        d = ROOT / "songs" / c["id"]
        d.mkdir(parents=True, exist_ok=True)
        tags = list(dict.fromkeys(TYPE_TAGS.get(t, [t]) + ["beginner"]))
        meta = {
            "id": c["id"],
            "title": c["title"],
            "composer": "Traditional",
            "copyright": {"status": "public-domain", "notes": NOTES.get(t, "Traditional (pre-1900)")},
            "tags": tags,
            "difficulty": c.get("difficulty", 2),
            "category": CATEGORY.get(t, "folk"),
            "instrumentsSuited": DEFAULT_INSTRUMENTS,
            "chords": [],
        }
        (d / "metadata.json").write_text(json.dumps(meta, indent=2) + "\n")
        made += 1
    print(f"scaffolded {made} candidate song dirs")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("usage: python build/scaffold_candidates.py <wave.json>")
    main(sys.argv[1])
