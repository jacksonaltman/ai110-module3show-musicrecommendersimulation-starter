# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name

**VibeMatch 1.0**

---

## 2. Goal and Intended Use

**Goal.** The model suggests songs a listener will probably like. It picks the top 5 songs from a small catalog. It scores each song against a taste profile.

**A taste profile has four parts:**
- favorite genre
- favorite mood
- target energy (0 to 1)
- whether the listener likes acoustic sound

**Intended use.**
- Classroom learning about how recommenders work.
- Trying out ideas, like changing weights and seeing what happens.
- Showing how a simple score can explain its picks.

**Not intended for.**
- Real music apps or real users.
- Judging anyone's taste or personality.
- Any choice that matters, like what a company should promote or pay for.

The catalog is tiny and the numbers are made up. The model also knows nothing about other listeners.

---

## 3. How the Model Works

Every song gets points. The points add up to a score out of 6.

- **Mood match:** 2 points if the song's mood is the one the listener wants.
- **Genre match:** 1 point if the genre is the one the listener wants.
- **Energy:** up to 2 points. The closer the song's energy is to the target, the more points it gets.
- **Acoustic sound:** 1 point if the song fits what the listener likes. Acoustic fans get it for acoustic songs. Everyone else gets it for non-acoustic songs.

Then the songs are sorted from best to worst. The top 5 are shown. Each song comes with reasons, like "mood match: chill (+2.0)". Tempo, valence and danceability are in the data. They are not used in the score yet.

---

## 4. Data

- The catalog has **20 songs** in `data/songs.csv`.
- I started with 10 songs. I added 10 more to cover new genres and moods.
- There are 17 genres and 16 moods.
- Most genres have only one song. Lofi has three. Pop has two.
- Each song has genre, mood, energy, tempo, valence, danceability and acousticness.
- The numbers are made up. They are not measured from real songs.

**Limits.**
- No lyrics, language, artist fame or release year.
- No data about what other people listen to.
- Many kinds of music are missing, like K-pop, blues and gospel.

---

## 5. Strengths

- It works well for clear tastes. Chill Lofi, High-Energy Pop and Deep Intense Rock all got the songs I would pick by hand.
- It can tell opposite listeners apart. The lofi list and the rock list share no songs.
- It explains itself. Every pick has reasons you can read.
- It is easy to change. You can edit one weight and rerun it.

---

## 6. Limitations and Bias

**Bonus points can beat the energy match.**
- I tested a "Sad Banger" profile. It wanted classical music at energy 0.9, and it likes acoustic sound.
- The top song was Moonlit Sonata, which has energy 0.18. That is the calmest song in the catalog.
- It won because genre and acoustic bonuses gave it 2 points. Its big energy gap only cost about 1.4 points.
- The system never warns that the result goes against the request.

**Other problems.**
- If a mood or genre is not in the catalog, those points are lost. "Sad" matched nothing.
- Genre is all or nothing. "Indie pop" gets no credit for a pop fan.
- The catalog is skewed. Lofi fans get a full list of good matches. Most other fans get one good match and then weaker ones.
- Energy and acoustic sound move together, so calm songs get rewarded twice.
- The acoustic bonus has a hard cutoff. A song at 0.59 gets nothing and a song at 0.61 gets a full point.

---

## 7. Evaluation

**How I tested it.** I ran seven profiles and looked at the top 5 for each.

- Three typical listeners: High-Energy Pop, Chill Lofi, Deep Intense Rock.
- Four tricky ones:
  - **Sad Banger:** classical, mood "sad", energy 0.9, likes acoustic.
  - **K-Pop Fan:** a genre that is not in the catalog.
  - **Metal Fan Who Wants Chill:** metal genre but a chill mood.
  - **No Stated Taste:** unknown genre and mood, energy 0.5.

The full output is in the README.

**Do the results feel right?** For the typical profiles, yes. Sunrise City was first for pop with 5.94 out of 6. It matched on mood, genre, energy and non-acoustic sound.

**What surprised me.**
- Gym Hero was second for both pop and rock. It fits pop by genre. It fits rock by mood and energy.
- Sad Banger got the lowest-energy song first.

**Weight experiment.** I doubled the energy weight and halved the genre weight.
- Four of seven profiles did not change.
- Sad Banger changed a lot. It got high-energy songs, which fits its energy request better.
- Metal Fan got worse. The only metal song dropped out of the top 5.
- So the change made results different, not clearly better.

**Comparing pairs of profiles.**
- **Pop vs Lofi:** no songs in common. Pop gets bright, loud songs. Lofi gets quiet, acoustic ones. That makes sense because every feature points the other way.
- **Pop vs Rock:** both want loud songs, so they share Gym Hero and Fuego Nocturno. Mood splits them. Pop keeps happy songs. Rock gets intense ones.
- **Lofi vs Rock:** totally different lists. Their top scores are almost equal, so neither is favored.
- **Pop vs K-Pop Fan:** three of five songs are the same. The K-pop point can never be earned, so Sunrise City drops from 5.94 to 4.96.
- **Rock vs Sad Banger:** both want energy of 0.9 or more. Sad Banger got quiet songs because genre and acoustic points won.
- **Lofi vs Metal Fan Who Wants Chill:** the top three are the same chill songs. The only metal song came fourth. Mood is worth more than genre.
- **Lofi vs No Stated Taste:** with no genre or mood, only energy and acoustic sound count. Dusty Road Home won because its energy is 0.52.

---

## 8. Ideas for Improvement

1. **Give partial credit for close moods and genres.** Chill, relaxed and focused are close. Pop and indie pop are close.
2. **Add valence as a target.** This would split dark intense songs from happy intense ones, like Iron Requiem and Neon Overdrive.
3. **Warn when the top song fits poorly.** For example, say so if the best song has a big energy gap. Also add more songs so every genre has a few.

---

## 9. Personal Reflection

**Biggest learning moment.** I thought the hard part would be the math. It was not. The hard part was seeing how weights shape results. The Sad Banger profile showed it. Bonus points for genre and acoustic sound beat a huge energy mismatch. The scores looked fine, but the answer was wrong.

**How AI helped, and when I double-checked.**
- It sped up the boring parts: loading the CSV, writing the scoring function, and making test profiles.
- I still had to check it. The starter code imported `recommender` in a way that failed under `python -m src.main`. I only found out by running it.
- The output had a hard-coded "out of 6.00". That would have been wrong for the weight experiment, so I made it follow the weights.
- One of the comparison notes said two lists were "nearly the same". They shared three of five songs. I fixed the wording after checking the numbers.

**What surprised me.** A few additions and one sort felt like a real recommendation. The reasons for each pick helped most. A plain list of points made the results feel smart.

**What I would try next.**
- Partial credit for close moods and genres.
- A valence target.
- Profiles that can hold more than one taste.
- A warning when the best match is still a poor one.
