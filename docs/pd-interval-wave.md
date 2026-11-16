# PD interval-range wave — author & checker instructions

Queue: `build/pd_interval_queue.json` (184 songs: hymns, carols, folk, children's).
Each record has `tuneHint` and `expectedRange` — the melody's range as scale
degrees relative to the tonic (e.g. `5,6,7,1,2,3,4` = from the dominant *below*
the tonic up to the 4th above it; `1-8` = tonic to octave). Use it to confirm you
have the right tune and the right octave placement.

Repo root: `/home/user/opensongs-json`. Converter:
`.venv/bin/python build/convert.py songs/<id>` (ignore the `/home/shaun` path in
`build/ABC_AUTHORING.md` — read that spec for the ABC format rules).

## Getting references (what works in this container)

Use **Bash `curl -sL`** (WebFetch may fail DNS here). Allowed hosts include
abcnotation.com, trillian.mit.edu, hymnary.org, hymntime.com, en.wikipedia.org,
tunearch.org, ttadev.org, folkinfo.mainlynorfolk.info, contemplator.com,
cpdl.org, imslp.org, gutenberg.org, folktunefinder.com, bethsnotesplus.com,
mutopiaproject.org, thesession.org. WebSearch works for finding pages.

- **abcnotation.com (best)** — search:
  `curl -sL "https://abcnotation.com/searchTunes?q=<words+of+title>&f=c&o=a&s=0" | grep -oE 'tunePage\?a=[^"]+' | sort -u`
  then raw ABC for a hit `a=<path>`:
  `curl -sL "https://abcnotation.com/getResource/downloads/text_/x.abc?a=<path>"`.
  Many hymns and carols are there too (search the title or tune name). Beware
  same-title different tunes — check against `expectedRange`/`tuneHint`.
- **hymnary.org** — tune pages (`/tune/<name>`) give tune name, composer, dates,
  meter, and first-line text; page HTML is readable but media downloads are
  bot-blocked. Use it for identification, PD dates and lyrics.
- **hymntime.com (Cyber Hymnal; connection is flaky — skip if it times out)** — hymn pages with full PD lyrics, composer
  dates and MIDI (`.mid`). A MIDI can be read with music21:
  `.venv/bin/python -c "import music21 as m;s=m.converter.parse('x.mid');[print(n.nameWithOctave,n.quarterLength) for n in s.parts[0].flatten().notes]"`
  (part 0 is usually soprano = melody; chords → take the top note).
- **Wikipedia** — `action=raw` sometimes has `<score>` LilyPond blocks.
- **contemplator.com / folkinfo / tunearch / thesession** — folk ABC/notes.

## Author (Sonnet)

For each assigned id (metadata.json already exists — do not edit it):

1. **Find a published reference** for the melody with WebSearch/WebFetch —
   hymnary.org (tune pages: page scans, sometimes MIDI/MusicXML/ABC), Wikipedia
   scores, abcnotation.com, cpdl.org, mutopiaproject, IMSLP, Library of Congress,
   folk songbooks. **Never author from memory alone** — memory-only drafts have
   been wrong before. If you cannot find a reference you can read note-by-note,
   do not write the file: report `SKIP <id>: <reason>`.
2. Confirm it is the right tune: matches `tuneHint` and its range matches
   `expectedRange`.
3. Confirm PD under the AU rule: composer **and** lyricist died before 1955.
   Use only PD lyrics (verse 1, plus refrain if any). If not PD → SKIP.
4. Write `songs/<id>/song.abc`: monophonic melody, verse 1 (+ refrain/chorus),
   barline-synced `w:` lyrics, beginner key with range roughly C4–C6. It must be
   **our own encoding** — re-type the notes; don't paste someone's ABC file.
   Write repeats out (the converter does not expand `:|`). Only one `w:` line is
   read, so put all lyrics for the tune line(s) on one `w:` after each tune line.
5. Run the converter. Fix any FAIL. Then check **every bar's duration** equals
   the meter (pickup and final bar may be partial and should sum to one bar), and
   the lyric count ≈ note count.

Report per song (terse): `OK line`, key/meter, bars, reference URL(s), confidence
(high/med/low), and any metadata correction needed (composer/title/notes) —
don't edit metadata.json yourself.

## Checker (Sonnet)

You review songs another agent authored. For each id:

1. Open `songs/<id>/song.abc` and `metadata.json`.
2. Fetch the reference(s) the author used **and at least one independent
   reference** where possible. Compare note-by-note: opening pickup, intervals,
   rhythm, bar count, cadences. Check the range against `expectedRange` in the
   queue.
3. Check lyrics: correct PD text, one syllable per note, `|` synced per bar.
4. Check PD (composer + lyricist d. before 1955).
5. **Fix** any error directly in `song.abc` and re-run the converter.

Verdict per song: `PASS`, `FIXED: <what changed>`, or `FAIL: <reason>` (leave
the file in place; the orchestrator removes failures). Also report metadata
corrections needed.
