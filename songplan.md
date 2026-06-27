# Beginner Song Library — Architecture, Schema & Repertoire

A foundation library of public-domain folk, nursery, and classical-theme melodies, encoded once and transformed into note tiles, Dottl, guitar tab, violin tab, MIDI, and standard notation.

---

## 1. Format decision (the keystone)

**Don't make MIDI the source of truth.** MIDI is timing data, not notation — it can't reliably represent note *spelling* (C♯ vs D♭), lyrics, beaming, or clean rhythmic values. Always *derive* MIDI from a notation source, never the reverse.

Recommended three-layer model:

| Layer | Format | Why |
|---|---|---|
| **Authoring (front door)** | ABC notation **and/or** MuseScore | ABC is dramatically faster for simple monophonic tunes and there are large public-domain ABC corpora to import (TheSession, Nottingham DB, tunearch). MuseScore for anything two-handed (classical themes). |
| **Canonical (stored in git)** | **MusicXML** | Lossless for everything we need, universal, re-exportable to MIDI/anything. `abc2xml` converts the ABC front door into this. |
| **Normalized (generator input)** | **Song-document JSON** (schema below) | `music21` parses MusicXML once and emits a flat event list. Every downstream generator reads *only this* — never raw MusicXML. Decouples tiles/tab/Dottl from notation parsing. |

Pipeline:

```
ABC ─┐
     ├─→ MusicXML (canonical) ─→ music21 ─→ song.json ─┬─→ note tiles
MuseScore ─┘                                           ├─→ Dottl
                                                       ├─→ guitar tab
                                                       ├─→ violin tab / fingering
                                                       ├─→ MIDI (playback)
                                                       └─→ notation SVG (Verovio)
```

Each generator is an independent, testable module consuming the same JSON. Add an instrument format later without touching the corpus.

---

## 2. Normalized song-document schema

```json
{
  "id": "hot-cross-buns",
  "title": "Hot Cross Buns",
  "composer": "Traditional",
  "copyright": { "status": "public-domain", "notes": "Trad. nursery rhyme." },
  "tags": ["nursery", "beginner", "3-note"],
  "difficulty": 1,
  "key": "C major",
  "keySignature": 0,
  "timeSignature": [4, 4],
  "tempo": 100,
  "pickupBeats": 0,
  "instrumentsSuited": ["keyboard", "recorder", "violin", "glockenspiel"],
  "noteRange": { "low": "C4", "high": "E4" },
  "chords": [{ "onset": 0, "symbol": "C" }],
  "events": [
    { "i": 0,  "measure": 1, "beat": 1.0, "onset": 0.0,  "duration": 1.0, "type": "note", "pitch": {"step":"E","alter":0,"octave":4,"midi":64,"spelled":"E4"}, "lyric": "Hot",   "tie": null },
    { "i": 1,  "measure": 1, "beat": 2.0, "onset": 1.0,  "duration": 1.0, "type": "note", "pitch": {"step":"D","alter":0,"octave":4,"midi":62,"spelled":"D4"}, "lyric": "cross", "tie": null },
    { "i": 2,  "measure": 1, "beat": 3.0, "onset": 2.0,  "duration": 2.0, "type": "note", "pitch": {"step":"C","alter":0,"octave":4,"midi":60,"spelled":"C4"}, "lyric": "buns",  "tie": null },
    { "i": 3,  "measure": 2, "beat": 1.0, "onset": 4.0,  "duration": 1.0, "type": "note", "pitch": {"step":"E","alter":0,"octave":4,"midi":64,"spelled":"E4"}, "lyric": "Hot",   "tie": null },
    { "i": 4,  "measure": 2, "beat": 2.0, "onset": 5.0,  "duration": 1.0, "type": "note", "pitch": {"step":"D","alter":0,"octave":4,"midi":62,"spelled":"D4"}, "lyric": "cross", "tie": null },
    { "i": 5,  "measure": 2, "beat": 3.0, "onset": 6.0,  "duration": 2.0, "type": "note", "pitch": {"step":"C","alter":0,"octave":4,"midi":60,"spelled":"C4"}, "lyric": "buns",  "tie": null },
    { "i": 6,  "measure": 3, "beat": 1.0, "onset": 8.0,  "duration": 0.5, "type": "note", "pitch": {"step":"C","alter":0,"octave":4,"midi":60,"spelled":"C4"}, "lyric": "One",   "tie": null },
    { "i": 7,  "measure": 3, "beat": 1.5, "onset": 8.5,  "duration": 0.5, "type": "note", "pitch": {"step":"C","alter":0,"octave":4,"midi":60,"spelled":"C4"}, "lyric": "a",     "tie": null },
    { "i": 8,  "measure": 3, "beat": 2.0, "onset": 9.0,  "duration": 0.5, "type": "note", "pitch": {"step":"C","alter":0,"octave":4,"midi":60,"spelled":"C4"}, "lyric": "pen",   "tie": null },
    { "i": 9,  "measure": 3, "beat": 2.5, "onset": 9.5,  "duration": 0.5, "type": "note", "pitch": {"step":"C","alter":0,"octave":4,"midi":60,"spelled":"C4"}, "lyric": "ny",    "tie": null },
    { "i": 10, "measure": 3, "beat": 3.0, "onset": 10.0, "duration": 0.5, "type": "note", "pitch": {"step":"D","alter":0,"octave":4,"midi":62,"spelled":"D4"}, "lyric": "two",   "tie": null },
    { "i": 11, "measure": 3, "beat": 3.5, "onset": 10.5, "duration": 0.5, "type": "note", "pitch": {"step":"D","alter":0,"octave":4,"midi":62,"spelled":"D4"}, "lyric": "a",     "tie": null },
    { "i": 12, "measure": 3, "beat": 4.0, "onset": 11.0, "duration": 0.5, "type": "note", "pitch": {"step":"D","alter":0,"octave":4,"midi":62,"spelled":"D4"}, "lyric": "pen",   "tie": null },
    { "i": 13, "measure": 3, "beat": 4.5, "onset": 11.5, "duration": 0.5, "type": "note", "pitch": {"step":"D","alter":0,"octave":4,"midi":62,"spelled":"D4"}, "lyric": "ny",    "tie": null },
    { "i": 14, "measure": 4, "beat": 1.0, "onset": 12.0, "duration": 1.0, "type": "note", "pitch": {"step":"E","alter":0,"octave":4,"midi":64,"spelled":"E4"}, "lyric": "Hot",   "tie": null },
    { "i": 15, "measure": 4, "beat": 2.0, "onset": 13.0, "duration": 1.0, "type": "note", "pitch": {"step":"D","alter":0,"octave":4,"midi":62,"spelled":"D4"}, "lyric": "cross", "tie": null },
    { "i": 16, "measure": 4, "beat": 3.0, "onset": 14.0, "duration": 2.0, "type": "note", "pitch": {"step":"C","alter":0,"octave":4,"midi":60,"spelled":"C4"}, "lyric": "buns",  "tie": null }
  ]
}
```

Field notes:
- `onset` / `duration` are in **beats** (quarter = 1.0 in 4/4) — instrument-agnostic, easy to map to any timeline.
- `pitch` carries both `spelled` (for notation/tab) and `midi` (for playback/transposition). Keep both; never reconstruct one from the other lossily.
- `fingering` can be added per-event by each generator (keyboard finger number, violin string+finger, fret position) rather than stored in the source.
- `chords` is an optional harmony track for guitar/uke accompaniment, independent of the melody events.

**Twinkle Twinkle** first bar, same pattern (C major, 4/4): `C4 q "Twin", C4 q "kle", G4 q "twin", G4 q "kle"` → bar 2 `A4 q "lit", A4 q "tle", G4 h "star"` → bar 3 `F4 F4 E4 E4 "how I won-der"` → bar 4 `D4 D4 C4(h) "what you are"`.

---

## 3. Repertoire — vetted candidate list (~110, pick 50–100)

Difficulty 1–5. "3-note / 5-note" flags the true entry tier. All listed are public domain **unless noted**; see the exclusion list at the end.

### A. First songs (3–5 notes, difficulty 1)
| Song | Notes | Suited |
|---|---|---|
| Hot Cross Buns | 3-note (E-D-C) | all |
| Mary Had a Little Lamb | 3-note | all |
| Au Clair de la Lune | 4-note | all |
| Merrily We Roll Along | 3-note | all |
| Frère Jacques | 5-note | all (round) |
| Twinkle Twinkle / Baa Baa Black Sheep / ABC Song | 6-note | all |
| Rain Rain Go Away | 3-note | all |
| Cuckoo (Sol-Mi) | 2-note | voice/perc |

### B. Nursery & children's (difficulty 1–2)
Old MacDonald · Row Row Row Your Boat · London Bridge · Itsy Bitsy / Incy Wincy Spider · The Wheels on the Bus · If You're Happy and You Know It · Head Shoulders Knees & Toes · Pop Goes the Weasel · Ring a Ring o' Roses · Three Blind Mice · Hickory Dickory Dock · This Old Man · Bingo · Five Little Ducks · The Farmer in the Dell · Skip to My Lou · Oranges and Lemons · Polly Put the Kettle On · Lavender's Blue · Sing a Song of Sixpence · The Mulberry Bush · The Muffin Man · Yankee Doodle · She'll Be Coming Round the Mountain · Happy Birthday *(now PD — see note)*

### C. Folk & traditional (difficulty 2–3)
Scarborough Fair · Greensleeves · Auld Lang Syne · Home on the Range · Oh! Susanna *(Foster)* · Camptown Races *(Foster)* · Old Folks at Home/Swanee *(Foster)* · Clementine · Down in the Valley · Red River Valley · The Water Is Wide · Shenandoah · When the Saints Go Marching In · Amazing Grace · Wayfaring Stranger · Simple Gifts · Aura Lee · My Bonnie Lies Over the Ocean · Molly Malone · The Ash Grove · All Through the Night · Loch Lomond · Skye Boat Song · Danny Boy/Londonderry Air · Michael Row the Boat Ashore · Kumbaya · He's Got the Whole World in His Hands

### D. Australian traditional (difficulty 2–3)
Waltzing Matilda · Click Go the Shears · Botany Bay · The Wild Colonial Boy · The Drover's Dream · South Australia *(sea shanty, popular AU)*

### E. Classical themes (difficulty 2–4) — works are PD; we engrave our own
Ode to Joy *(Beethoven)* · Für Elise theme · Symphony No. 5 motif · Eine kleine Nachtmusik theme *(Mozart)* · Rondo alla Turca theme · Minuet in G *(Petzold)* · Musette in D *(Bach)* · Jesu, Joy of Man's Desiring · Prelude in C / "Bach Ave Maria" · Canon in D theme *(Pachelbel)* · Spring theme *(Vivaldi)* · Surprise Symphony theme *(Haydn)* · New World Largo / "Goin' Home" *(Dvořák)* · Brahms' Lullaby · Swan Lake theme · Dance of the Sugar Plum Fairy · In the Hall of the Mountain King · Morning Mood *(Grieg)* · Can-Can *(Offenbach)* · The Swan *(Saint-Saëns)* · Gymnopédie No. 1 *(Satie)* · Prelude in E minor *(Chopin)* · Sonatina Op. 36/1 theme *(Clementi)* · Land of Hope and Glory theme *(Elgar)*

### F. Seasonal / carols (difficulty 2–3, all PD)
Jingle Bells · Silent Night · We Wish You a Merry Christmas · Deck the Halls · Joy to the World · O Come All Ye Faithful · The First Noel · Away in a Manger · Good King Wenceslas

### G. Rounds & canons (great for ensemble teaching)
Frère Jacques · Three Blind Mice · Row Row Row Your Boat · Are You Sleeping · Hey Ho Nobody Home · Dona Nobis Pacem

---

## 4. Copyright watch-list — EXCLUDE or handle with care

Operating from Australia (copyright = life + 70 years). **Not legal advice — confirm edge cases.**

| Song | Status | Action |
|---|---|---|
| **Kookaburra Sits in the Old Gum Tree** | Marion Sinclair (d. 1988) — in copyright in AU until ~2058 (the *Men at Work* case) | **EXCLUDE.** Common trap — sounds traditional, isn't. |
| **Edelweiss** | Rodgers & Hammerstein, 1959 | **EXCLUDE.** Not a folk song. |
| **This Land Is Your Land** | Woody Guthrie (d. 1967) | **EXCLUDE** in AU until ~2038. |
| **Wild Mountain Thyme / Will Ye Go Lassie Go** | McPeake arrangement is claimed | Use only a clearly traditional base, or skip. |
| **Happy Birthday** | Melody = "Good Morning to All" (Hill sisters; Patty d. 1946). PD in AU from ~2017; ruled effectively PD in the US in 2016 | **INCLUDE**, but keep the note on file. |
| **Classical "editions"** | The *works* are PD; a specific publisher's *engraving* may carry a typographical/publication right (esp. EU/UK, 25 yr) | Safe because **we generate our own engraving** from our own encoding. Don't copy a publisher's PDF. |
| **Recordings** | A PD composition can have a copyrighted *recording* | Irrelevant here — we encode notation, not audio. |

---

## 5. What's left to spec before building generators

The front half (ABC/MuseScore → MusicXML → song.json) is instrument-agnostic and ready to build. The back half needs your internal format definitions:

- **Note tiles** — the `github.com/pepperhorn` note-tile generator's expected input (and tile vocabulary).
- **Dottl** — the note/event format the Dottl app ingests.
- **Guitar tab** — string/fret representation, and whether chord diagrams are wanted alongside melody.
- **Violin tab / fingering** — string + finger + position conventions you teach.

Point me at any of these (repo, schema, or an example file) and each becomes a small generator module over the same `song.json`.
