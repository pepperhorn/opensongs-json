#!/usr/bin/env python3
r"""Convert an ABC source (+ metadata sidecar) into canonical MusicXML and a
normalized song.json, per songplan.md schema.

Pipeline:  song.abc  --music21-->  song.musicxml (canonical)
                                \--> song.json (normalized event list)

Lyrics are taken from ABC ``w:`` lines and aligned to notes with barline (|)
sync, which is far more reliable than music21's ABC lyric importer.

Usage:
    python build/convert.py <song_dir> [<song_dir> ...]
    python build/convert.py --all songs/
"""
import json
import re
import sys
from pathlib import Path

from music21 import (converter, note, chord, harmony, tempo, key as m21key,
                     meter, pitch as m21pitch)


def _spelled(p):
    return {
        "step": p.step,
        "alter": int(p.alter),
        "octave": p.octave,
        "midi": p.midi,
        "spelled": p.nameWithOctave.replace("-", "b").replace("##", "x"),
    }


def _midi_to_spelled(m):
    return m21pitch.Pitch(m).nameWithOctave.replace("-", "b")


def _parse_lyric_line(line):
    """Tokenize one ABC w: line into a list of measure-chunks; each chunk is a
    list of syllable-or-None tokens (None = skip this note: rest, *, or _)."""
    body = line.split(":", 1)[1].strip() if ":" in line else line.strip()
    chunks, cur = [], []
    for word in body.split():
        if word == "|":
            chunks.append(cur)
            cur = []
            continue
        # split a hyphenated word into syllables; keep blank/hold markers
        for syl in re.split(r"-", word):
            syl = syl.strip()
            if syl == "" :
                continue
            if syl in ("*", "_"):
                cur.append(None)
            else:
                cur.append(syl.replace("~", " "))
    chunks.append(cur)
    return chunks


def _lyric_lines(abc_text):
    return [ln for ln in abc_text.splitlines() if ln.strip().startswith("w:")]


def convert_song(song_dir: Path):
    song_dir = Path(song_dir)
    abc_path = song_dir / "song.abc"
    meta_path = song_dir / "metadata.json"
    if not abc_path.exists():
        raise FileNotFoundError(f"missing {abc_path}")
    abc_text = abc_path.read_text()
    meta = json.loads(meta_path.read_text()) if meta_path.exists() else {}

    score = converter.parse(abc_text, format="abc")
    score.write("musicxml", fp=str(song_dir / "song.musicxml"))

    part = score.parts[0] if score.parts else score
    flat = part.flatten()

    ks = flat.getElementsByClass(m21key.KeySignature)
    keysig = ks[0].sharps if ks else 0
    keyobj = flat.getElementsByClass(m21key.Key)
    key_name = str(keyobj[0]) if keyobj else (meta.get("key", "C major"))
    ts = flat.getElementsByClass(meter.TimeSignature)
    time_sig = [ts[0].numerator, ts[0].denominator] if ts else [4, 4]
    bar_dur = ts[0].barDuration.quarterLength if ts else 4.0
    mm = flat.getElementsByClass(tempo.MetronomeMark)
    bpm = int(mm[0].number) if mm and mm[0].number else meta.get("tempo", 100)

    measures = part.getElementsByClass("Measure")
    pickup_beats = 0.0
    if measures and measures[0].duration.quarterLength < bar_dur:
        pickup_beats = float(bar_dur - measures[0].duration.quarterLength)

    # build raw events; normalize measure numbers so the first bar == 1.
    # Exclude chord-symbol/annotation objects (quoted "Dm", "A7", "f" in the ABC
    # parse as zero-duration harmony.Harmony) and ornamental grace notes — both
    # would otherwise emit phantom zero-duration events. The MusicXML written
    # above keeps them; song.json is the clean monophonic melody.
    raw = [n for n in flat.notesAndRests
           if not isinstance(n, harmony.Harmony)
           and not n.duration.isGrace
           and n.duration.quarterLength > 0]
    min_meas = min((n.measureNumber for n in raw if n.measureNumber is not None),
                   default=1)
    shift = 1 - min_meas

    events, lo, hi = [], None, None
    for i, n in enumerate(raw):
        meas = (int(n.measureNumber) + shift) if n.measureNumber is not None else None
        beat = round(float(n.beat), 3) if n.beat is not None else None
        ev = {
            "i": i, "measure": meas, "beat": beat,
            "onset": round(float(n.offset), 3),
            "duration": round(float(n.duration.quarterLength), 3),
            "type": "note", "pitch": None, "lyric": None, "tie": None,
        }
        if getattr(n, "tie", None):
            ev["tie"] = n.tie.type
        if isinstance(n, note.Note):
            ev["pitch"] = _spelled(n.pitch)
            m = n.pitch.midi
            lo = m if lo is None or m < lo else lo
            hi = m if hi is None or m > hi else hi
        elif isinstance(n, chord.Chord):
            ev["pitch"] = _spelled(n.pitches[-1])
        else:
            ev["type"] = "rest"
        events.append(ev)

    # lyric assignment: barline-synced per measure, skipping rests
    wlines = _lyric_lines(abc_text)
    if wlines:
        chunks = _parse_lyric_line(wlines[0])
        by_measure = {}
        for ev in events:
            if ev["type"] == "note":
                by_measure.setdefault(ev["measure"], []).append(ev)
        measures_sorted = sorted(by_measure)
        for ci, chunk in enumerate(chunks):
            if ci >= len(measures_sorted):
                break
            notes_in = by_measure[measures_sorted[ci]]
            for si, syl in enumerate(chunk):
                if si < len(notes_in) and syl is not None:
                    notes_in[si]["lyric"] = syl

    note_range = ({"low": _midi_to_spelled(lo), "high": _midi_to_spelled(hi)}
                  if lo is not None else {"low": "C4", "high": "C5"})

    song = {
        "id": meta.get("id", song_dir.name),
        "title": meta.get("title") or (score.metadata.title if score.metadata else song_dir.name),
        "composer": meta.get("composer") or "Traditional",
        "copyright": meta.get("copyright", {"status": "public-domain", "notes": ""}),
        "tags": meta.get("tags", []),
        "difficulty": meta.get("difficulty", 1),
        "key": key_name,
        "keySignature": keysig,
        "timeSignature": time_sig,
        "tempo": bpm,
        "pickupBeats": pickup_beats,
        "instrumentsSuited": meta.get("instrumentsSuited", []),
        "noteRange": note_range,
        "chords": meta.get("chords", []),
        "events": events,
    }
    (song_dir / "song.json").write_text(json.dumps(song, indent=2) + "\n")
    return song


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        sys.exit(1)
    if args[0] == "--all":
        root = Path(args[1])
        dirs = sorted([d for d in root.iterdir() if (d / "song.abc").exists()])
    else:
        dirs = [Path(a) for a in args]
    ok, fail = 0, 0
    for d in dirs:
        try:
            s = convert_song(d)
            nl = sum(1 for e in s["events"] if e.get("lyric"))
            print(f"OK   {d.name}: {len(s['events'])} ev, {nl} lyrics, "
                  f"{s['key']}, {s['timeSignature'][0]}/{s['timeSignature'][1]}, "
                  f"{s['noteRange']['low']}-{s['noteRange']['high']}")
            ok += 1
        except Exception as e:
            print(f"FAIL {d.name}: {e}")
            fail += 1
    print(f"\n{ok} ok, {fail} failed")
    sys.exit(1 if fail else 0)


if __name__ == "__main__":
    main()
