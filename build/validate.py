#!/usr/bin/env python3
"""Validate every song.json against the songplan schema invariants."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
errs = []


def check(cond, sid, msg):
    if not cond:
        errs.append(f"{sid}: {msg}")


for d in sorted((ROOT / "songs").iterdir()):
    sj = d / "song.json"
    if not sj.exists():
        continue
    sid = d.name
    s = json.loads(sj.read_text())
    for f in ["id", "title", "composer", "key", "timeSignature", "tempo",
              "noteRange", "events"]:
        check(f in s, sid, f"missing field {f}")
    check(s["id"] == sid, sid, f"id mismatch ({s['id']})")
    ev = s["events"]
    check(len(ev) > 0, sid, "no events")
    notes = [e for e in ev if e["type"] == "note"]
    check(len(notes) > 0, sid, "no note events")
    # onsets monotonic non-decreasing
    last = -1
    for e in ev:
        check(e["onset"] >= last - 1e-6, sid, f"onset out of order at i={e['i']}")
        last = e["onset"]
        check(e["duration"] > 0, sid, f"non-positive duration at i={e['i']}")
        if e["type"] == "note":
            p = e["pitch"]
            check(p and "midi" in p and 21 <= p["midi"] <= 108, sid,
                  f"pitch/midi out of range at i={e['i']}")
    # index sequence
    check([e["i"] for e in ev] == list(range(len(ev))), sid, "i not sequential")

if errs:
    print(f"VALIDATION FAILED ({len(errs)} issues):")
    for e in errs:
        print("  " + e)
    sys.exit(1)
print("validation passed")
