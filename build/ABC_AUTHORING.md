# ABC Authoring Spec — opensongs-json

You are transcribing well-known **public-domain** melodies into ABC notation.
For each assigned song you write exactly one file: `songs/<id>/song.abc`.
A `metadata.json` already exists in each dir — **do not modify it**.

## Goal

Produce an accurate, recognizable, **monophonic** (single-line) melody of the
song's principal strain — typically the verse and/or the famous theme,
**8–16 bars**. This is a beginner library: keep it to the main tune, in a
beginner-friendly key. Do NOT write full piano arrangements, chords stacked in
the staff, or multiple voices.

## Required ABC structure

```
X:1
T:<exact title from metadata.json>
C:<composer from metadata.json>
M:<time signature, e.g. 4/4, 3/4, 6/8, 2/4>
L:1/4
Q:1/4=<tempo bpm>
K:<key, e.g. C, G, D, F, Am, Dm, Em>
<the melody, barlines included>
w: <lyrics, barline-synced — see below>
```

Notes on headers:
- `L:1/4` (quarter = unit) is required so durations read cleanly: `C` = quarter,
  `C2` = half, `C3` = dotted half, `C4` = whole, `C/2` or `C/` = eighth,
  `C/4` = sixteenth. In `6/8` you may prefer `L:1/8` — if so, set it and adjust.
- Pick a sensible `Q:` tempo for the song (e.g. 100–120 marches, 72–88 ballads,
  126+ for a Can-Can).
- Choose a **beginner key** that keeps the melody roughly C4–C6. Use the natural
  traditional key when it is easy (C, G, D, F, A minor, D minor, E minor).

## Pitch / octave in ABC (critical)

- `C D E F G A B` = the octave from middle C (C4) up to B4.
- `c d e f g a b` = the octave above (C5–B5).
- `C,` = C3 (comma lowers an octave); `c'` = C6 (apostrophe raises).
- Accidentals: `^` sharp, `_` flat, `=` natural, written **before** the note
  (`^F` = F#, `_B` = Bb). The key signature already applies — only mark
  accidentals not in the key.

## Rhythm & bars

- Put a barline `|` at every measure boundary. The number of beats per bar must
  match `M:`. Use `|]` at the very end.
- **Pickup/anacrusis:** if the tune starts on an upbeat, write the partial pickup
  bar, then `|`, then full bars. Example (4/4, pickup of one quarter):
  `G | c2 G2 | ...`
- Ties use `-` between notes (`C2-C2`); slurs use `(...)` — for these simple
  melodies you usually need neither.

## Lyrics (`w:` line) — barline-synced

If the song has words (all nursery/folk/seasonal do; purely instrumental
classical themes do not), add a `w:` line **immediately after** the tune line.

- One syllable per note, in order.
- Separate syllables **within a word** using `-` (each gets its own note):
  `pen-ny`, `won-der`.
- Separate words with spaces.
- **Put a `|` in the `w:` line at every barline**, aligned with the music's
  barlines. This is how the converter re-syncs lyrics per measure, so it is
  very forgiving of miscounts as long as the bar count matches.
- `*` = a note with no syllable (melisma start); `_` = hold previous syllable.
- For instrumental themes (e.g. Für Elise, Canon in D, Eine kleine Nachtmusik,
  Spring, Rondo alla Turca, Gymnopédie, preludes, Sugar Plum, Swan), **omit the
  `w:` line entirely.**

Example (Hot Cross Buns), already in the repo as the reference:
```
X:1
T:Hot Cross Buns
C:Traditional
M:4/4
L:1/4
Q:1/4=100
K:C
E D C2 | E D C2 | C/C/ C/C/ D/D/ D/D/ | E D C2 |]
w: Hot cross buns | Hot cross buns | One a pen-ny two a pen-ny | Hot cross buns
```

## Self-check (required before you finish)

From `/home/shaun/songlib`, with the venv active, run the converter on each
song you wrote and confirm it reports OK with a sane note range and (for songs
with lyrics) a lyric count close to the note count:

```
. .venv/bin/activate
python build/convert.py songs/<id>
```

Fix any FAIL. A good result looks like:
`OK   <id>: 34 ev, 30 lyrics, G major, 4/4, D4-E5`

Then re-read your `song.abc` once and sanity-check the opening interval against
the tune in your memory (e.g. Twinkle starts on a repeated tonic up a fifth;
Amazing Grace starts on a pickup rising a fourth to the downbeat). Accuracy of
the melody is the whole point — get the first phrase unmistakably right.

## Output

Write only `songs/<id>/song.abc` for each assigned id. Report, per song: the
key/meter you chose, bar count, and the converter's OK line. Keep it terse.
