# Work In Progress — opensongs-json

_Last updated: 2026-07-01_

Snapshot of in-flight work on the public-domain melody library. See
`songplan.md` for the overall plan and `README.md` for the published overview.

## Library size

- **346 songs** in `index.json`, all passing `build/validate.py`.
- Progression: 294 (all prior queues) → 297 (3 Nottingham carols) → 321
  (25-tune Nottingham sampler complete) → **346** (Wave 1 of the 969 candidate
  pool — *uncommitted, see below*).

## Uncommitted right now

Wave 1 of the Nottingham candidate pool — **25 songs, built + validated but not
yet committed**:

- 2 carols: `jubilate-deo-round`, `wassail-2`
- 5 Playford: `dick-s-maggot`, `sadlers-wells`, `st-hugh-s-jig`,
  `the-alderman-s-hat`, `the-queen-s-jig`
- 18 morris: `abbotts-bromley-horn-dance`, `beaux-of-london-city`,
  `blue-bells-of-scotland`, `constant-billy`, `fieldtown-processional`,
  `gisburn-processional`, `highland-mary`, `jockey-to-the-fair`,
  `lads-a-bunchum`, `leapfrog`, `morning-star`, `morris-off`,
  `singing-of-the-travels`, `sweet-jenny-jones`, `the-forester`,
  `tideswell-processional`, `wheatley-processional`, `william-and-nancy`

Also uncommitted: `build/scaffold_candidates.py` (new tool) and the `index.json`
bump.

### Quality checks on Wave 1 (all passed)

- **Verbatim/CC0 check:** longest shared note-run vs the GPLv3 source = **0
  chars**. No song reproduces the dataset encoding. (Anti-verbatim rule — pick a
  key different from the source, add own phrasing — was baked into authoring
  this time, so no re-do cycle was needed.)
- **Range audit** (target ~C4–C6): two minor, acceptable outliers, left as
  optional polish:
  - `highland-mary` — dips to A3 (57) on one low phrase.
  - `st-hugh-s-jig` — sits entirely in the upper octave, D5–A5 (74–81).
- Fidelity caveat from the authoring agents: `gisburn-processional` and
  `highland-mary` are lesser-known titles authored from contour only (not
  verified against a canonical morris setting); worth an ear-check before
  relying on them.

**Next action for this wave:** commit (suggested split: the
`scaffold_candidates.py` tool, then the 25 songs + index), then push.

## Pipeline & tooling

`song.abc` → `build/convert.py` → `song.musicxml` (canonical) + `song.json`
(normalized event list). Then `build/index.py` rebuilds `index.json`, and
`build/validate.py` gates the whole library. Authoring spec:
`build/ABC_AUTHORING.md`. Python venv at `.venv` (music21).

- `build/scaffold.py` — metadata.json from `build/songlist.json` (core 100).
- `build/scaffold_nottingham.py` — metadata.json from `build/nottingham_queue.json` (25-sampler).
- `build/scaffold_candidates.py` — metadata.json from a wave JSON of records
  drawn from `build/nottingham_candidates.json`. **This is the tool for the 969 pool.**

## The Nottingham candidate backlog (the 969 pool)

Source manifest: `build/NOTTINGHAM_CANDIDATES.md` + `build/nottingham_candidates.json`
(reference-only, metadata only — no GPLv3 ABC in the repo). It began as 969
clear-PD tunes not yet built; after Wave 1, **917 remain**:

| type | remaining |
|------|-----------|
| reel | 434 |
| jig | 320 |
| hornpipe | 59 |
| misc | 44 |
| waltz | 42 |
| slip-jig | 11 |
| morris | 6 |
| carol | 1 |

Strategy: continue in curated **~25-tune waves**, beginner-friendly types first
(carols/morris/playford/waltz), single-part tunes with no meter/key change,
leaving the 434 fast fiddle reels for last. Wave selection filters out anything
already built and dedupes by normalized title (Wave 1 dropped `the-boar-s-head`
as a dup of the existing `the-boars-head`).

### How to author the next wave (repeatable recipe)

1. **Contour references** require the GPLv3 source dataset, which is **NOT in the
   repo** (license) — clone it to scratch:
   `git clone --depth 1 https://github.com/jukedeck/nottingham-dataset`
   (ABC_cleaned/*.abc). It was cloned to the session scratchpad during Wave 1.
2. Select the next ~25 beginner-friendly, not-yet-built candidates; extract each
   tune's contour from the dataset by `source_collection` + `source_X`.
3. `python build/scaffold_candidates.py <wave.json>` to stamp metadata dirs.
4. Dispatch **Sonnet** subagents (~5 songs/batch) to author `song.abc` only —
   contour used as reference only; transpose off the source key + vary phrasing;
   carols get barline-synced `w:` lyrics, dance tunes stay instrumental.
5. Central pass: `convert.py` each → verbatim check (0 long shared runs) →
   `index.py` → `validate.py` → commit + push.

## Standing rules (see also memory `songlib-build-state`, `songlib-author-model-strategy`)

- **Model:** Sonnet for ALL subagents (author + review). Batches ~5 songs.
- **Copyright:** AU life+70, AU-PD only (composer d. ≤1955). Music PD ≠ lyrics PD.
  Dance collections are anonymous-traditional (PD by nature); waltzes/xmas vetted
  per-title.
- **CC0 discipline:** re-author every melody as our own ABC; a note sequence
  byte-identical to a full GPLv3 strain must be re-done in a different key with
  independent phrasing. Short (~2-bar) incidental overlaps are fine.
