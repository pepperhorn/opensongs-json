# opensongs-json

A library of **public-domain beginner melodies**, each encoded once as ABC and
derived into canonical MusicXML and a normalized `song.json` event list — ready
to drive note tiles, tabs, MIDI, and notation rendering.

## Pipeline

```
song.abc  ──music21──▶  song.musicxml (canonical)
                    └──▶  song.json (normalized event list)
```

ABC is the human-authored front door; MusicXML is the lossless canonical store;
`song.json` is the flat, instrument-agnostic event list every downstream
generator reads. See [`songplan.md`](songplan.md) for the full design.

## Layout

```
songs/<id>/
  song.abc        # authored source (ABC notation)
  song.musicxml   # canonical, re-exportable
  song.json       # normalized: events with onset/duration (beats), spelled+midi pitch, lyrics
  metadata.json   # title, composer, copyright, tags, difficulty, suited instruments
index.json        # top-level manifest of all songs
build/            # convert.py, scaffold.py, index.py, validate.py + curation queues
```

## Contents

100 songs across first-tunes, nursery, folk, Australian traditional, classical
themes, and carols — all public domain. Copyright is filtered for Australian law
(life + 70): see `build/SCRAPE_STRATEGY.md` and `songplan.md` §4.

## Build

```bash
python3 -m venv .venv && . .venv/bin/activate && pip install music21
python build/convert.py --all songs/   # regenerate musicxml + song.json
python build/validate.py               # schema invariants
python build/index.py                  # rebuild index.json
```

## Sources

Melodies are transcribed by hand from public-domain sources. Reference material
we use to identify tunes and check transcriptions includes:

- **[Nottingham Music Database](https://abc.sourceforge.net/NMD/)** — a large
  collection of public-domain British/Irish/American folk tunes in ABC, via the
  cleaned [`jukedeck/nottingham-dataset`](https://github.com/jukedeck/nottingham-dataset)
  (GPLv3). The folk melodies themselves are public domain; we re-author the
  single-line melody ourselves rather than copying its files, so our output stays
  CC0 and free of the dataset's copyleft terms.

## License

Song data: **CC0-1.0** — all melodies are public domain; engravings are our own.
