# Work In Progress — opensongs-json

_Last updated: 2026-07-02_

Snapshot of in-flight work on the public-domain melody library. See
`songplan.md` for the overall plan and `README.md` for the published overview.

## Library size

- **371 songs** in `index.json`, all passing `build/validate.py`.
- Progression: 294 (all prior queues) → 297 (3 Nottingham carols) → 321
  (25-tune Nottingham sampler complete) → 346 (candidate Wave 1) → **371**
  (candidate Wave 2). All committed + pushed.

## Uncommitted right now

Nothing — working tree clean; Waves 1 and 2 are on `origin/master`.

## Completed waves (candidate pool)

- **Wave 1 (25):** 2 carols, 5 Playford, 18 morris. Commit `baac984`.
- **Wave 2 (25):** 24 waltzes (Daisy Bell, Kelvingrove, Hector the Hero, I
  Belong to Glasgow, …) + `winster-processional`. Melody-only. Commit `c943bd4`.

Every wave: verbatim check clean (no shared strain with the GPLv3 source),
all ranges in tolerance, `validate.py` green.

### Minor polish backlog (optional, non-blocking)

- `highland-mary` (W1) dips to A3; `just-as-the-sun-was-setting` (W2) floors at
  B3 — both one/two semitones under the C4 target, acceptable.
- Ear-check lesser-known titles authored from contour only:
  `gisburn-processional`, `highland-mary` (W1); `ffarwel-ir-marian`,
  `mist-on-the-marsh` (W2, flagged as freer reinterpretations).

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
clear-PD tunes not yet built; after Waves 1–2, **892 remain**:

| type | remaining |
|------|-----------|
| reel | 434 |
| jig | 320 |
| hornpipe | 59 |
| misc | 44 |
| waltz | 18 |
| slip-jig | 11 |
| morris | 5 |
| carol | 1 |

Strategy: continue in curated **~25-tune waves**, beginner-friendly types first
(carols/morris/playford/waltz), single-part tunes with no meter/key change,
leaving the 434 fast fiddle reels for last. Wave selection filters out anything
already built and dedupes by normalized title (Wave 1 dropped `the-boar-s-head`
as a dup of the existing `the-boars-head`).

**The "easy" pool is nearly drained.** Only **18 waltzes + 5 morris + 1 carol**
of the no-meter/key-change beginner types remain — one more wave. After that it's
all jigs/reels/hornpipes/slip-jigs: faster, wider-range session tunes. For those,
tighten selection on beginner suitability (favor simpler jigs/hornpipes, expect
more transposing-down for range, and consider raising difficulty ratings) — worth
a quick decision on approach before Wave 4.

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
