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

Output of `python -m src.main` for the default taste profile (lofi, chill, energy 0.40, likes acoustic):

```
Loaded songs: 20

Profile: lofi / chill / energy 0.40 / acoustic

Top recommendations:
============================================================

1. Midnight Coding by LoRoom
   Score: 5.96 / 6.00
   Why:
     - mood match: chill (+2.0)
     - genre match: lofi (+1.0)
     - energy 0.42 vs target 0.40 (+1.96)
     - acoustic sound: 0.71 (+1.0)

2. Library Rain by Paper Lanterns
   Score: 5.90 / 6.00
   Why:
     - mood match: chill (+2.0)
     - genre match: lofi (+1.0)
     - energy 0.35 vs target 0.40 (+1.90)
     - acoustic sound: 0.86 (+1.0)

3. Spacewalk Thoughts by Orbit Bloom
   Score: 4.76 / 6.00
   Why:
     - mood match: chill (+2.0)
     - energy 0.28 vs target 0.40 (+1.76)
     - acoustic sound: 0.92 (+1.0)

4. Focus Flow by LoRoom
   Score: 4.00 / 6.00
   Why:
     - genre match: lofi (+1.0)
     - energy 0.40 vs target 0.40 (+2.00)
     - acoustic sound: 0.78 (+1.0)

5. Coffee Shop Stories by Slow Stereo
   Score: 2.94 / 6.00
   Why:
     - energy 0.37 vs target 0.40 (+1.94)
     - acoustic sound: 0.89 (+1.0)
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

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



