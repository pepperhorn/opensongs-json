# Scrape & Expansion Strategy — next ~200 songs (AU-PD, blended)

Goal: queue ~200 additional songs into `build/queue.json`, then author them via
the ABC pipeline and blend into the main `songs/` library with difficulty
ratings. Decisions from the user: **AU public-domain only**, **blend into the
main library** (not a separate tier).

## Source

Wikipedia `https://en.wikipedia.org/wiki/{YYYY}_in_public_domain` pages.

**Critical:** scrape the **"life + 70 years" section** of each page (composers
who *died* in `YYYY − 70`), NOT the US "songs of {year}" section. AU copyright =
life + 70, so the death year is what matters. (The first pass mistakenly used
the US 95-year song lists, most of which are still under AU copyright.)

Scrape a wide span of years (e.g. 2015–2026 → composers who died 1945–1956) to
build the pool. Also acceptable: clearly age-PD traditional/folk/parlour songs
and PD classical themes that fit a beginner library.

## Copyright rule (hard gate)

For each candidate determine, by checking the person's Wikipedia page:
1. **Music composer death year** — must be **≤ 1955** (PD in AU as of 2026).
2. **Lyricist death year** — music PD ≠ lyrics PD.
   - If lyricist also died ≤ 1955 → may include lyrics (`w:` line).
   - Otherwise → **author melody-only, omit the `w:` line.** Note this in
     metadata `copyright.notes`.
3. Exclude anything matching the spirit of songplan.md §4 watch-list.

Record per song: `music_composer`, `music_death`, `lyricist`, `lyricist_death`,
`au_pd_music` (bool), `author_mode` ("with-lyrics" | "melody-only"), `us_pd`,
`source_year`.

## Suitability

This is still a teaching library. Prefer songs with a clear, singable principal
melody. Skip dense art-songs/operetta arias that don't reduce to a recognizable
monophonic line. Assign `difficulty` 1–5 honestly (most jazz standards = 4–5).

## Dedupe

Skip any `id` already in `build/songlist.json` or already authored in `songs/`.

## Output / handoff to authoring

Append approved candidates to `build/queue.json` `kept[]` with a slug `id`,
`title`, `composer`, `difficulty`, `category` ("standard", "folk", etc.),
`author_mode`, and the copyright fields above. Then:
1. A scaffold step writes `songs/<id>/metadata.json` (extend `scaffold.py` to
   also read `queue.json`).
2. Authoring agents write `songs/<id>/song.abc` per `build/ABC_AUTHORING.md`
   (melody-only where `author_mode == "melody-only"`).
3. `python build/convert.py --all songs/` → MusicXML + song.json.
4. Review agents verify musical accuracy.
5. `python build/index.py` rebuilds `index.json`.

## Model strategy (cost)

- **Write/author subagents → Haiku** (cheapest; transcribe known melodies).
- **Review/accuracy subagents → Sonnet** (verify notes/rhythm against the known
  tune and repair the cheap pass). The review gate is mandatory for Haiku output.

## Status

Blocked on subagent fan-out until the session API limit resets (~3:30am
Australia/Sydney). 19 AU-PD candidates already verified in `queue.json`; need
~180 more from the life+70 sweep above.
