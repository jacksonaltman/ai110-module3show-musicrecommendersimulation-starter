# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

Real-world platforms like Spotify and YouTube predict what you'll love next by combining two ideas: collaborative filtering (finding listeners whose behavior resembles yours and recommending what they played) and content-based filtering (matching the attributes of songs you already like). They blend both in hybrid systems, then rank candidates with models that also use context such as skips, time of day, and predicted watch time. My simulation has no listening data from other users, so it is purely content-based. It prioritizes how well a song's vibe matches the user's stated taste: mood first, then how close the song's energy is to the user's target, then genre, with a smaller bonus for acousticness. Every song gets a score from a scoring rule, and a ranking rule sorts all the scores and returns the top k with a short reason for each pick.

### Song features

Each `Song` has these fields:

- `id`, `title`, `artist` (identifying info, not used in scoring)
- `genre` (categorical, exact-match bonus)
- `mood` (categorical, exact-match bonus)
- `energy` (0-1, scored by closeness to the user's target)
- `acousticness` (0-1, scored against the user's acoustic preference)
- `tempo_bpm`, `valence`, `danceability` (loaded but not scored in the first version)

### UserProfile features

Each `UserProfile` stores:

- `favorite_genre`: the genre to match
- `favorite_mood`: the mood to match
- `target_energy`: the energy level the user wants (0-1)
- `likes_acoustic`: whether the user prefers acoustic-sounding songs

### Scoring and ranking

- **Scoring rule (one song):** add a mood match bonus, a genre match bonus, an energy closeness score (`1 - abs(song.energy - target_energy)`), and an acousticness bonus, each multiplied by its weight.
- **Ranking rule (all songs):** score every song in the catalog, sort from highest to lowest, and return the top k.

### Algorithm Recipe

Each song's score is the sum of four points, for a maximum of 6.0:

| Rule | Points |
|---|---|
| Mood matches `favorite_mood` exactly | +2.0 |
| Genre matches `favorite_genre` exactly | +1.0 |
| Energy closeness: `2.0 * (1 - abs(song.energy - target_energy))` | 0 to +2.0 |
| Acousticness: song above 0.6 when `likes_acoustic` is true, or below 0.3 when it is false | +1.0 |

Ties are broken by the order songs appear in the CSV. Each rule that adds points also adds a short reason, such as "mood matches (chill)", so every recommendation can explain itself.

### Expected biases

- **Mood can outweigh a good sonic match.** Mood is the largest single bonus and must match exactly. A lofi song at nearly the target energy but labeled "focused" ranks below an ambient song labeled "chill."
- **Genre is all-or-nothing.** "Indie pop" earns nothing for a user who asked for "pop," even though they are close.
- **Calm songs are double-counted.** Energy and acousticness are strongly inverse in this catalog, so a calm-music user gets rewarded twice for the same trait.
- **The catalog skews the results.** Lofi has three songs, most genres have one, and the values are invented, so users who like lofi get fuller lists than users who like anything else.
- **Hard acoustic cutoffs.** A song at 0.59 acousticness gets nothing and one at 0.61 gets a full point.
- **One fixed taste per user.** The profile is a single point, so it can't represent someone who likes both lofi and rock, and it has no valence target to separate dark intense music from bright intense music.
- **No crowd signal.** With no other users' listening data, the system can't surface surprising picks outside the user's stated taste.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

`python -m src.main` runs seven taste profiles: three typical listeners (High-Energy Pop, Chill Lofi, Deep Intense Rock) and four adversarial ones built to stress the scoring (a conflicting profile, a genre that isn't in the catalog, a genre-vs-mood clash, and a profile with no stated taste). Full terminal output:

```
Loaded songs: 20

Profile: High-Energy Pop
  genre=pop, mood=happy, energy=0.85, likes_acoustic=False
============================================================

1. Sunrise City by Neon Echo (pop/happy)
   Score: 5.94 / 6.00
     - mood match: happy (+2.0)
     - genre match: pop (+1.0)
     - energy 0.82 vs target 0.85 (+1.94)
     - non-acoustic sound: 0.18 (+1.0)

2. Gym Hero by Max Pulse (pop/intense)
   Score: 3.84 / 6.00
     - genre match: pop (+1.0)
     - energy 0.93 vs target 0.85 (+1.84)
     - non-acoustic sound: 0.05 (+1.0)

3. Rooftop Lights by Indigo Parade (indie pop/happy)
   Score: 3.82 / 6.00
     - mood match: happy (+2.0)
     - energy 0.76 vs target 0.85 (+1.82)

4. Fuego Nocturno by La Ola Roja (latin/passionate)
   Score: 2.98 / 6.00
     - energy 0.84 vs target 0.85 (+1.98)
     - non-acoustic sound: 0.27 (+1.0)

5. Storm Runner by Voltline (rock/intense)
   Score: 2.88 / 6.00
     - energy 0.91 vs target 0.85 (+1.88)
     - non-acoustic sound: 0.10 (+1.0)

Profile: Chill Lofi
  genre=lofi, mood=chill, energy=0.40, likes_acoustic=True
============================================================

1. Midnight Coding by LoRoom (lofi/chill)
   Score: 5.96 / 6.00
     - mood match: chill (+2.0)
     - genre match: lofi (+1.0)
     - energy 0.42 vs target 0.40 (+1.96)
     - acoustic sound: 0.71 (+1.0)

2. Library Rain by Paper Lanterns (lofi/chill)
   Score: 5.90 / 6.00
     - mood match: chill (+2.0)
     - genre match: lofi (+1.0)
     - energy 0.35 vs target 0.40 (+1.90)
     - acoustic sound: 0.86 (+1.0)

3. Spacewalk Thoughts by Orbit Bloom (ambient/chill)
   Score: 4.76 / 6.00
     - mood match: chill (+2.0)
     - energy 0.28 vs target 0.40 (+1.76)
     - acoustic sound: 0.92 (+1.0)

4. Focus Flow by LoRoom (lofi/focused)
   Score: 4.00 / 6.00
     - genre match: lofi (+1.0)
     - energy 0.40 vs target 0.40 (+2.00)
     - acoustic sound: 0.78 (+1.0)

5. Coffee Shop Stories by Slow Stereo (jazz/relaxed)
   Score: 2.94 / 6.00
     - energy 0.37 vs target 0.40 (+1.94)
     - acoustic sound: 0.89 (+1.0)

Profile: Deep Intense Rock
  genre=rock, mood=intense, energy=0.92, likes_acoustic=False
============================================================

1. Storm Runner by Voltline (rock/intense)
   Score: 5.98 / 6.00
     - mood match: intense (+2.0)
     - genre match: rock (+1.0)
     - energy 0.91 vs target 0.92 (+1.98)
     - non-acoustic sound: 0.10 (+1.0)

2. Gym Hero by Max Pulse (pop/intense)
   Score: 4.98 / 6.00
     - mood match: intense (+2.0)
     - energy 0.93 vs target 0.92 (+1.98)
     - non-acoustic sound: 0.05 (+1.0)

3. Neon Overdrive by Pulse Theory (edm/euphoric)
   Score: 2.92 / 6.00
     - energy 0.96 vs target 0.92 (+1.92)
     - non-acoustic sound: 0.03 (+1.0)

4. Iron Requiem by Black Cathedral (metal/angry)
   Score: 2.90 / 6.00
     - energy 0.97 vs target 0.92 (+1.90)
     - non-acoustic sound: 0.06 (+1.0)

5. Fuego Nocturno by La Ola Roja (latin/passionate)
   Score: 2.84 / 6.00
     - energy 0.84 vs target 0.92 (+1.84)
     - non-acoustic sound: 0.27 (+1.0)

Profile: Sad Banger (conflicting)
  genre=classical, mood=sad, energy=0.90, likes_acoustic=True
============================================================

1. Moonlit Sonata by Clara Whitfield (classical/peaceful)
   Score: 2.56 / 6.00
     - genre match: classical (+1.0)
     - energy 0.18 vs target 0.90 (+0.56)
     - acoustic sound: 0.97 (+1.0)

2. Dusty Road Home by Hollis Creek (country/nostalgic)
   Score: 2.24 / 6.00
     - energy 0.52 vs target 0.90 (+1.24)
     - acoustic sound: 0.81 (+1.0)

3. Midnight Coding by LoRoom (lofi/chill)
   Score: 2.04 / 6.00
     - energy 0.42 vs target 0.90 (+1.04)
     - acoustic sound: 0.71 (+1.0)

4. Focus Flow by LoRoom (lofi/focused)
   Score: 2.00 / 6.00
     - energy 0.40 vs target 0.90 (+1.00)
     - acoustic sound: 0.78 (+1.0)

5. Storm Runner by Voltline (rock/intense)
   Score: 1.98 / 6.00
     - energy 0.91 vs target 0.90 (+1.98)

Profile: K-Pop Fan (genre not in catalog)
  genre=k-pop, mood=happy, energy=0.80, likes_acoustic=False
============================================================

1. Sunrise City by Neon Echo (pop/happy)
   Score: 4.96 / 6.00
     - mood match: happy (+2.0)
     - energy 0.82 vs target 0.80 (+1.96)
     - non-acoustic sound: 0.18 (+1.0)

2. Rooftop Lights by Indigo Parade (indie pop/happy)
   Score: 3.92 / 6.00
     - mood match: happy (+2.0)
     - energy 0.76 vs target 0.80 (+1.92)

3. Concrete Crown by Verse Valley (hip-hop/confident)
   Score: 2.96 / 6.00
     - energy 0.78 vs target 0.80 (+1.96)
     - non-acoustic sound: 0.12 (+1.0)

4. Fuego Nocturno by La Ola Roja (latin/passionate)
   Score: 2.92 / 6.00
     - energy 0.84 vs target 0.80 (+1.92)
     - non-acoustic sound: 0.27 (+1.0)

5. Night Drive Loop by Neon Echo (synthwave/moody)
   Score: 2.90 / 6.00
     - energy 0.75 vs target 0.80 (+1.90)
     - non-acoustic sound: 0.22 (+1.0)

Profile: Metal Fan Who Wants Chill (genre vs mood)
  genre=metal, mood=chill, energy=0.50, likes_acoustic=False
============================================================

1. Midnight Coding by LoRoom (lofi/chill)
   Score: 3.84 / 6.00
     - mood match: chill (+2.0)
     - energy 0.42 vs target 0.50 (+1.84)

2. Library Rain by Paper Lanterns (lofi/chill)
   Score: 3.70 / 6.00
     - mood match: chill (+2.0)
     - energy 0.35 vs target 0.50 (+1.70)

3. Spacewalk Thoughts by Orbit Bloom (ambient/chill)
   Score: 3.56 / 6.00
     - mood match: chill (+2.0)
     - energy 0.28 vs target 0.50 (+1.56)

4. Iron Requiem by Black Cathedral (metal/angry)
   Score: 3.06 / 6.00
     - genre match: metal (+1.0)
     - energy 0.97 vs target 0.50 (+1.06)
     - non-acoustic sound: 0.06 (+1.0)

5. Night Drive Loop by Neon Echo (synthwave/moody)
   Score: 2.50 / 6.00
     - energy 0.75 vs target 0.50 (+1.50)
     - non-acoustic sound: 0.22 (+1.0)

Profile: No Stated Taste (energy only)
  genre=none, mood=none, energy=0.50, likes_acoustic=True
============================================================

1. Dusty Road Home by Hollis Creek (country/nostalgic)
   Score: 2.96 / 6.00
     - energy 0.52 vs target 0.50 (+1.96)
     - acoustic sound: 0.81 (+1.0)

2. Midnight Coding by LoRoom (lofi/chill)
   Score: 2.84 / 6.00
     - energy 0.42 vs target 0.50 (+1.84)
     - acoustic sound: 0.71 (+1.0)

3. Focus Flow by LoRoom (lofi/focused)
   Score: 2.80 / 6.00
     - energy 0.40 vs target 0.50 (+1.80)
     - acoustic sound: 0.78 (+1.0)

4. Coffee Shop Stories by Slow Stereo (jazz/relaxed)
   Score: 2.74 / 6.00
     - energy 0.37 vs target 0.50 (+1.74)
     - acoustic sound: 0.89 (+1.0)

5. Library Rain by Paper Lanterns (lofi/chill)
   Score: 2.70 / 6.00
     - energy 0.35 vs target 0.50 (+1.70)
     - acoustic sound: 0.86 (+1.0)
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

**Weight shift: double energy, halve genre.** Genre went from 1.0 to 0.5 points and energy from 2.0 to 4.0 points, so the maximum score moved from 6.0 to 7.5 (2.0 mood + 0.5 genre + 4.0 energy + 1.0 acoustic). I ran all seven profiles with the change and compared the top 5 with the baseline. I tested it by overriding the weight constants in a scratch script, so the code in `recommender.py` still uses the original weights.

- **Chill Lofi, Deep Intense Rock, K-Pop Fan, No Stated Taste:** the top 5 stayed in exactly the same order. These profiles already had mood, energy and acousticness all pointing the same way, so the weights barely mattered.
- **High-Energy Pop:** Rooftop Lights (indie pop, happy, energy 0.76) moved above Gym Hero (pop, intense, energy 0.93). That looks slightly more accurate for a "happy" listener, since Gym Hero's only extra point came from the genre label.
- **Sad Banger (conflicting):** the list changed completely. Moonlit Sonata (energy 0.18) dropped out and the top 5 became Storm Runner, Gym Hero, Neon Overdrive, Fuego Nocturno and Iron Requiem, all with energy above 0.84. This is more accurate to the requested energy 0.9, but it now ignores the classical/acoustic part of the request.
- **Metal Fan Who Wants Chill:** Iron Requiem, the only metal song, fell out of the top 5, because halving genre removed its main reason to rank. That is less accurate for someone who named metal as their genre.

Overall the change made the recommendations different, not clearly better: it helped the profile that asked for an energy the catalog could match, and hurt the one that depended on genre.

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



