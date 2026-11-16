# Work In Progress — opensongs-json

_Last updated: 2026-10-21_

Snapshot of in-flight work on the public-domain melody library. See
`songplan.md` for the overall plan and `README.md` for the published overview.

## Library size

- **548 songs** in `index.json`, all passing `build/validate.py`.
- Progression: 294 (all prior queues) → 297 (3 Nottingham carols) → 321
  (25-tune Nottingham sampler complete) → 346 (candidate Wave 1) → 371
  (candidate Wave 2) → **457** (world folk wave). All committed + pushed.

## Uncommitted right now

Nothing — working tree clean.

## PD interval-range wave (2026-11-16, in progress)

Queue: `build/pd_interval_queue.json` (184 songs; `status` per record). Instructions:
`docs/pd-interval-wave.md`. Sonnet authors + Sonnet checkers, ~6 songs/batch.

- Wave 2 (30 carols/classical): **22 done**, 8 `needs-source`.
- Wave 3 (30 carols/hymns): **28 done**, 2 `needs-source`.
- Wave 4 (30 hymns): **28 done**, 2 `needs-source`.
- Hymn source: pdhymns.com PD hymnal PDFs (539 pp + 41 pp Christmas), indexed by page — agents read pages as images.
- Wave 1 (30 folk/children/Cohan): **13 done**, 16 `needs-source`, 1 `not-pd`
  (Just a Closer Walk — 1940 Kenneth Morris).
- Network: added reference hosts to the environment allowlist. Use `curl`
  (WebFetch fails DNS). abcnotation raw ABC + bethsnotesplus score images work;
  hymnary media downloads are bot-blocked; hymntime.com doesn't connect.
- Lesson: obscure folk titles often have no free notation — expect higher yield
  on hymns/carols (abcnotation has many).

## World folk wave (2026-10-21, 86 songs)

Source list: `docs/folk-songs/normalized_folk_traditional_songs_master_list.md`
(~250 titles). 86 authored; the rest skipped as duplicates of existing songs,
non-AU-PD (composer d. > 1955), or no reliable melody reference.

- Lesson: authoring from memory alone fails (Sonnet skipped nearly all; Opus
  drafts were often wrong). What worked: Opus subagents that **verify every
  melody note-by-note against a published reference** (Wikipedia scores,
  abcnotation/trillian, thesession, flutetunes, hymnary, Levy, national
  songbooks), then re-author as our own ABC.
- Converter gotchas found: only the first `w:` line is read; repeat signs are
  not expanded (write repeats out); an over-long bar can still report OK with a
  bogus meter — check per-measure durations.
- Ear-check backlog: hush-little-baby (rhythm inferred), frog-went-a-courtin /
  the-ants-go-marching (lyric fitting), sakura-sakura (final cadence).

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
