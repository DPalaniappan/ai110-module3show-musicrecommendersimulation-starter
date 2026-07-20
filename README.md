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

Explain your design in plain language.

Some prompts to answer:

- What features does each `Song` use in your system
  - For example: genre, mood, energy, tempo
- What information does your `UserProfile` store
- How does your `Recommender` compute a score for each song
- How do you choose which songs to recommend

You can include a simple diagram or bullet list if helpful.

### Song Features

- `genre`, `mood` — categorical, exact-match bonus
- `energy`, `valence`, `danceability`, `acousticness` (each 0–1) — numeric, compared to the user's targets
- `tempo_bpm` — stored, not currently used in scoring
- `id`, `title`, `artist` — identifying info only, not used in scoring

### UserProfile Features

- `favorite_genre`, `favorite_mood` — matched exactly against the song for a flat bonus
- `target_energy`, `target_valence`, `target_danceability` — numeric targets compared to the matching song feature
- `likes_acoustic` (bool) — converted to an implied target (`~0.8` if `True`, `~0.2` if `False`) and compared to `song.acousticness`

### Scoring Rule/Algorithm Recipe (one song at a time)

1. For each numeric feature, flip the gap into a 0–1 closeness score: `closeness = 1 - |song_value - target_value|`.
2. Weighted average across the four: `energy=2, valence=1, danceability=1, acousticness=1`.
3. Add `+0.3` if genre matches, `+0.3` if mood matches → `final_score`.

**Some biases might be the fact that genere and mood bonuses could drown out the numeric fit of the rtecommendation system meaning that if it doesnt fit that well with the numbers but has the right genre and mood then the song will be able to outscore other songs that have a greater numerical fit but dont have the right genre**

### Ranking Rule (the whole list)

Score every song, sort by `final_score` descending, return the top `k`.

Kept separate on purpose: scoring judges one song alone; ranking decides ordering/cutoff across all of them.

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

Paste a sample of your recommender's output here as a text block so a reader can see what it produces:

```
==================================================
USER PROFILE
==================================================
   favorite_genre: pop
   favorite_mood: happy
   target_energy: 0.8
   likes_acoustic: False

==================================================
TOP RECOMMENDATIONS
==================================================

1. Sunrise City  (Score: 1.58)
--------------------------------------------------
   • Energy is a 98% match (song: 0.82, target: 0.80)
   • Acousticness is a 98% match (song: 0.18, target: 0.20)
   • Genre matches your favorite genre: pop
   • Mood matches your favorite mood: happy

2. Rooftop Lights  (Score: 1.22)
--------------------------------------------------
   • Energy is a 96% match (song: 0.76, target: 0.80)
   • Acousticness is a 85% match (song: 0.35, target: 0.20)
   • Mood matches your favorite mood: happy

3. Gym Hero  (Score: 1.16)
--------------------------------------------------
   • Energy is a 87% match (song: 0.93, target: 0.80)
   • Acousticness is a 85% match (song: 0.05, target: 0.20)
   • Genre matches your favorite genre: pop

4. Night Drive Loop  (Score: 0.96)
--------------------------------------------------
   • Energy is a 95% match (song: 0.75, target: 0.80)
   • Acousticness is a 98% match (song: 0.22, target: 0.20)

5. Funk Machine  (Score: 0.95)
--------------------------------------------------
   • Energy is a 97% match (song: 0.83, target: 0.80)
   • Acousticness is a 90% match (song: 0.10, target: 0.20)
```

### Adversarial / Edge Case Profile Output

These profiles (defined in `adversarial_profiles` in `src/main.py`) are designed to probe weaknesses in the scoring logic rather than represent realistic users. See the notes after each block for what to look for.

**Empty Preferences** — no fields at all; checks that the code doesn't crash and falls back gracefully.

```
==================================================
USER PROFILE: Empty Preferences
==================================================

==================================================
TOP RECOMMENDATIONS
==================================================

1. Sunrise City  (Score: 0.00)
--------------------------------------------------
   • No preferences provided to compare against.

2. Midnight Coding  (Score: 0.00)
--------------------------------------------------
   • No preferences provided to compare against.

3. Storm Runner  (Score: 0.00)
--------------------------------------------------
   • No preferences provided to compare against.

4. Library Rain  (Score: 0.00)
--------------------------------------------------
   • No preferences provided to compare against.

5. Gym Hero  (Score: 0.00)
--------------------------------------------------
   • No preferences provided to compare against.
```

**Zero Energy (Falsy Value)** — `target_energy: 0.0`, a falsy-but-valid value; passed, confirming the code checks `is not None` rather than truthiness.

```
==================================================
USER PROFILE: Zero Energy (Falsy Value)
==================================================
   favorite_genre: lofi
   favorite_mood: chill
   target_energy: 0.0
   likes_acoustic: False

==================================================
TOP RECOMMENDATIONS
==================================================

1. Midnight Coding  (Score: 1.15)
--------------------------------------------------
   • Energy is a 58% match (song: 0.42, target: 0.00)
   • Acousticness is a 49% match (song: 0.71, target: 0.20)
   • Genre matches your favorite genre: lofi
   • Mood matches your favorite mood: chill

2. Library Rain  (Score: 1.15)
--------------------------------------------------
   • Energy is a 65% match (song: 0.35, target: 0.00)
   • Acousticness is a 34% match (song: 0.86, target: 0.20)
   • Genre matches your favorite genre: lofi
   • Mood matches your favorite mood: chill

3. Spacewalk Thoughts  (Score: 0.87)
--------------------------------------------------
   • Energy is a 72% match (song: 0.28, target: 0.00)
   • Acousticness is a 28% match (song: 0.92, target: 0.20)
   • Mood matches your favorite mood: chill

4. Focus Flow  (Score: 0.84)
--------------------------------------------------
   • Energy is a 60% match (song: 0.40, target: 0.00)
   • Acousticness is a 42% match (song: 0.78, target: 0.20)
   • Genre matches your favorite genre: lofi

5. Broken Streetlights  (Score: 0.70)
--------------------------------------------------
   • Energy is a 58% match (song: 0.42, target: 0.00)
   • Acousticness is a 95% match (song: 0.25, target: 0.20)
```

**Out-of-Range Target Energy** — `target_energy: 5.0`, above the valid `0–1` range; produces negative scores and nonsensical percentages like "-318% match" because `closeness` is never clamped.

```
==================================================
USER PROFILE: Out-of-Range Target Energy
==================================================
   favorite_genre: pop
   favorite_mood: happy
   target_energy: 5.0
   likes_acoustic: False

==================================================
TOP RECOMMENDATIONS
==================================================

1. Sunrise City  (Score: -1.19)
--------------------------------------------------
   • Energy is a -318% match (song: 0.82, target: 5.00)
   • Acousticness is a 98% match (song: 0.18, target: 0.20)
   • Genre matches your favorite genre: pop
   • Mood matches your favorite mood: happy

2. Gym Hero  (Score: -1.46)
--------------------------------------------------
   • Energy is a -307% match (song: 0.93, target: 5.00)
   • Acousticness is a 85% match (song: 0.05, target: 0.20)
   • Genre matches your favorite genre: pop

3. Rooftop Lights  (Score: -1.58)
--------------------------------------------------
   • Energy is a -324% match (song: 0.76, target: 5.00)
   • Acousticness is a 85% match (song: 0.35, target: 0.20)
   • Mood matches your favorite mood: happy

4. Iron Fist Rising  (Score: -1.74)
--------------------------------------------------
   • Energy is a -303% match (song: 0.97, target: 5.00)
   • Acousticness is a 83% match (song: 0.03, target: 0.20)

5. Storm Runner  (Score: -1.76)
--------------------------------------------------
   • Energy is a -309% match (song: 0.91, target: 5.00)
   • Acousticness is a 90% match (song: 0.10, target: 0.20)
```

**Negative Target Valence** — `target_valence: -3.0`; same clamping problem, drags an otherwise strong genre/mood/energy match (Broken Streetlights) down to barely positive, and everything below it goes negative.

```
==================================================
USER PROFILE: Negative Target Valence
==================================================
   favorite_genre: hip hop
   favorite_mood: sad
   target_energy: 0.4
   likes_acoustic: False
   target_valence: -3.0

==================================================
TOP RECOMMENDATIONS
==================================================

1. Broken Streetlights  (Score: 0.76)
--------------------------------------------------
   • Energy is a 98% match (song: 0.42, target: 0.40)
   • Valence is a -225% match (song: 0.25, target: -3.00)
   • Acousticness is a 95% match (song: 0.25, target: 0.20)
   • Genre matches your favorite genre: hip hop
   • Mood matches your favorite mood: sad

2. Velvet Whisper  (Score: -0.02)
--------------------------------------------------
   • Energy is a 88% match (song: 0.52, target: 0.40)
   • Valence is a -266% match (song: 0.66, target: -3.00)
   • Acousticness is a 82% match (song: 0.38, target: 0.20)

3. Midnight Coding  (Score: -0.03)
--------------------------------------------------
   • Energy is a 98% match (song: 0.42, target: 0.40)
   • Valence is a -256% match (song: 0.56, target: -3.00)
   • Acousticness is a 49% match (song: 0.71, target: 0.20)

4. Focus Flow  (Score: -0.04)
--------------------------------------------------
   • Energy is a 100% match (song: 0.40, target: 0.40)
   • Valence is a -259% match (song: 0.59, target: -3.00)
   • Acousticness is a 42% match (song: 0.78, target: 0.20)

5. Wildflower Roads  (Score: -0.05)
--------------------------------------------------
   • Energy is a 100% match (song: 0.40, target: 0.40)
   • Valence is a -259% match (song: 0.58, target: -3.00)
   • Acousticness is a 38% match (song: 0.82, target: 0.20)
```

**Case-Mismatched Genre/Mood** — `"Pop"` / `"Happy"` against the CSV's lowercase `"pop"` / `"happy"`; the exact-match bonus is case-sensitive, so no genre/mood bonus is ever applied even though a human would call this a match.

```
==================================================
USER PROFILE: Case-Mismatched Genre/Mood
==================================================
   favorite_genre: Pop
   favorite_mood: Happy
   target_energy: 0.8
   likes_acoustic: False

==================================================
TOP RECOMMENDATIONS
==================================================

1. Sunrise City  (Score: 0.98)
--------------------------------------------------
   • Energy is a 98% match (song: 0.82, target: 0.80)
   • Acousticness is a 98% match (song: 0.18, target: 0.20)

2. Night Drive Loop  (Score: 0.96)
--------------------------------------------------
   • Energy is a 95% match (song: 0.75, target: 0.80)
   • Acousticness is a 98% match (song: 0.22, target: 0.20)

3. Funk Machine  (Score: 0.95)
--------------------------------------------------
   • Energy is a 97% match (song: 0.83, target: 0.80)
   • Acousticness is a 90% match (song: 0.10, target: 0.20)

4. Rooftop Lights  (Score: 0.92)
--------------------------------------------------
   • Energy is a 96% match (song: 0.76, target: 0.80)
   • Acousticness is a 85% match (song: 0.35, target: 0.20)

5. Storm Runner  (Score: 0.89)
--------------------------------------------------
   • Energy is a 89% match (song: 0.91, target: 0.80)
   • Acousticness is a 90% match (song: 0.10, target: 0.20)
```

**Nonexistent Genre/Mood** — `"polka"` / `"euphoric"`, values not present anywhere in the catalog; no crash, simply no bonus ever applied, as expected.

```
==================================================
USER PROFILE: Nonexistent Genre/Mood
==================================================
   favorite_genre: polka
   favorite_mood: euphoric
   target_energy: 0.6
   likes_acoustic: False

==================================================
TOP RECOMMENDATIONS
==================================================

1. Island Sway  (Score: 0.91)
--------------------------------------------------
   • Energy is a 97% match (song: 0.63, target: 0.60)
   • Acousticness is a 78% match (song: 0.42, target: 0.20)

2. Night Drive Loop  (Score: 0.89)
--------------------------------------------------
   • Energy is a 85% match (song: 0.75, target: 0.60)
   • Acousticness is a 98% match (song: 0.22, target: 0.20)

3. Velvet Whisper  (Score: 0.89)
--------------------------------------------------
   • Energy is a 92% match (song: 0.52, target: 0.60)
   • Acousticness is a 82% match (song: 0.38, target: 0.20)

4. Broken Streetlights  (Score: 0.86)
--------------------------------------------------
   • Energy is a 82% match (song: 0.42, target: 0.60)
   • Acousticness is a 95% match (song: 0.25, target: 0.20)

5. Sunrise City  (Score: 0.85)
--------------------------------------------------
   • Energy is a 78% match (song: 0.82, target: 0.60)
   • Acousticness is a 98% match (song: 0.18, target: 0.20)
```

**Single-Factor Extreme (Energy Only)** — only `target_energy` set, no valence/danceability/acoustic/genre/mood; the numeric score is diluted only by the energy weight (2.0) instead of being averaged against 4-5 factors like other profiles, so its scores aren't on the same scale as a fully-specified profile's.

```
==================================================
USER PROFILE: Single-Factor Extreme (Energy Only)
==================================================
   favorite_genre: 
   favorite_mood: 
   target_energy: 0.9
   likes_acoustic: None

==================================================
TOP RECOMMENDATIONS
==================================================

1. Storm Runner  (Score: 0.99)
--------------------------------------------------
   • Energy is a 99% match (song: 0.91, target: 0.90)

2. Gym Hero  (Score: 0.97)
--------------------------------------------------
   • Energy is a 97% match (song: 0.93, target: 0.90)

3. Iron Fist Rising  (Score: 0.93)
--------------------------------------------------
   • Energy is a 93% match (song: 0.97, target: 0.90)

4. Funk Machine  (Score: 0.93)
--------------------------------------------------
   • Energy is a 93% match (song: 0.83, target: 0.90)

5. Sunrise City  (Score: 0.92)
--------------------------------------------------
   • Energy is a 92% match (song: 0.82, target: 0.90)
```

**Bonus-Overrides-Mismatch (Metal but Low Energy)** — wants very low energy (`0.1`) but favorites the highest-energy genre/mood in the catalog; "Iron Fist Rising" wins #1 with only a 13% energy match, purely because the flat `+0.6` genre+mood bonus outweighs a terrible numeric fit.

```
==================================================
USER PROFILE: Bonus-Overrides-Mismatch (Metal but Low Energy)
==================================================
   favorite_genre: metal
   favorite_mood: angry
   target_energy: 0.1
   likes_acoustic: False

==================================================
TOP RECOMMENDATIONS
==================================================

1. Iron Fist Rising  (Score: 0.96)
--------------------------------------------------
   • Energy is a 13% match (song: 0.97, target: 0.10)
   • Acousticness is a 83% match (song: 0.03, target: 0.20)
   • Genre matches your favorite genre: metal
   • Mood matches your favorite mood: angry

2. Broken Streetlights  (Score: 0.77)
--------------------------------------------------
   • Energy is a 68% match (song: 0.42, target: 0.10)
   • Acousticness is a 95% match (song: 0.25, target: 0.20)

3. Velvet Whisper  (Score: 0.66)
--------------------------------------------------
   • Energy is a 58% match (song: 0.52, target: 0.10)
   • Acousticness is a 82% match (song: 0.38, target: 0.20)

4. Moonlit Sonata Dreams  (Score: 0.65)
--------------------------------------------------
   • Energy is a 85% match (song: 0.25, target: 0.10)
   • Acousticness is a 24% match (song: 0.96, target: 0.20)

5. Spacewalk Thoughts  (Score: 0.64)
--------------------------------------------------
   • Energy is a 82% match (song: 0.28, target: 0.10)
   • Acousticness is a 28% match (song: 0.92, target: 0.20)
```

**Impossible Combo (Max Everything + No Acoustic)** — every numeric target maxed at `1.0`; no song can score a perfect closeness, and yet the top score still reaches `1.45`, showing the final score has no fixed upper bound.

```
==================================================
USER PROFILE: Impossible Combo (Max Everything + No Acoustic)
==================================================
   favorite_genre: pop
   favorite_mood: happy
   target_energy: 1.0
   likes_acoustic: False
   target_valence: 1.0
   target_danceability: 1.0

==================================================
TOP RECOMMENDATIONS
==================================================

1. Sunrise City  (Score: 1.45)
--------------------------------------------------
   • Energy is a 82% match (song: 0.82, target: 1.00)
   • Valence is a 84% match (song: 0.84, target: 1.00)
   • Danceability is a 79% match (song: 0.79, target: 1.00)
   • Acousticness is a 98% match (song: 0.18, target: 0.20)
   • Genre matches your favorite genre: pop
   • Mood matches your favorite mood: happy

2. Gym Hero  (Score: 1.17)
--------------------------------------------------
   • Energy is a 93% match (song: 0.93, target: 1.00)
   • Valence is a 77% match (song: 0.77, target: 1.00)
   • Danceability is a 88% match (song: 0.88, target: 1.00)
   • Acousticness is a 85% match (song: 0.05, target: 0.20)
   • Genre matches your favorite genre: pop

3. Rooftop Lights  (Score: 1.10)
--------------------------------------------------
   • Energy is a 76% match (song: 0.76, target: 1.00)
   • Valence is a 81% match (song: 0.81, target: 1.00)
   • Danceability is a 82% match (song: 0.82, target: 1.00)
   • Acousticness is a 85% match (song: 0.35, target: 0.20)
   • Mood matches your favorite mood: happy

4. Funk Machine  (Score: 0.86)
--------------------------------------------------
   • Energy is a 83% match (song: 0.83, target: 1.00)
   • Valence is a 85% match (song: 0.85, target: 1.00)
   • Danceability is a 88% match (song: 0.88, target: 1.00)
   • Acousticness is a 90% match (song: 0.10, target: 0.20)

5. Storm Runner  (Score: 0.77)
--------------------------------------------------
   • Energy is a 91% match (song: 0.91, target: 1.00)
   • Valence is a 48% match (song: 0.48, target: 1.00)
   • Danceability is a 66% match (song: 0.66, target: 1.00)
   • Acousticness is a 90% match (song: 0.10, target: 0.20)
```

**Trailing Whitespace Genre** — `"pop "` with a trailing space; reproduces the same exact-match fragility as the case-mismatch profile, dropping the genre bonus entirely.

```
==================================================
USER PROFILE: Trailing Whitespace Genre
==================================================
   favorite_genre: pop 
   favorite_mood: happy
   target_energy: 0.8
   likes_acoustic: False

==================================================
TOP RECOMMENDATIONS
==================================================

1. Sunrise City  (Score: 1.28)
--------------------------------------------------
   • Energy is a 98% match (song: 0.82, target: 0.80)
   • Acousticness is a 98% match (song: 0.18, target: 0.20)
   • Mood matches your favorite mood: happy

2. Rooftop Lights  (Score: 1.22)
--------------------------------------------------
   • Energy is a 96% match (song: 0.76, target: 0.80)
   • Acousticness is a 85% match (song: 0.35, target: 0.20)
   • Mood matches your favorite mood: happy

3. Night Drive Loop  (Score: 0.96)
--------------------------------------------------
   • Energy is a 95% match (song: 0.75, target: 0.80)
   • Acousticness is a 98% match (song: 0.22, target: 0.20)

4. Funk Machine  (Score: 0.95)
--------------------------------------------------
   • Energy is a 97% match (song: 0.83, target: 0.80)
   • Acousticness is a 90% match (song: 0.10, target: 0.20)

5. Storm Runner  (Score: 0.89)
--------------------------------------------------
   • Energy is a 89% match (song: 0.91, target: 0.80)
   • Acousticness is a 90% match (song: 0.10, target: 0.20)
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
Raising the energy weight from 2.0 to 4.0 made energy-mismatched songs drop in rank even when they matched the user's favorite genre and mood.

- What happened when you added tempo or valence to the score
Adding target_valence and target_danceability as optional fields let profiles like "High-Energy Pop" pick songs that felt more specifically upbeat, not just high-energy.

- How did your system behave for different types of users
Across the four test profiles, genre and mood bonuses only produced the "expected" top pick when the numeric targets also lined up with that song.

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
With 18 songs spread across 15 genres, most niche tastes only have one or two real options to recommend.

- It does not understand lyrics or language
It scores songs purely on numeric traits and tags, so it has no idea what a song is actually about.

- It might over favor one genre or mood
The heavy energy weight can override a genre and mood match, so it doesn't always favor genre/mood the way a user might expect.

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
I learned that recommenders turn data into predicitons by assinged weights to the numeric traites that the designer specifically wants for their recommendation system. I realized that it really depends what the design is and how you want to go about. Weights allow teh ddesigner to manipulate what gets recommended to the user meaning that the designer and boost certain data they want to be seen vs certain data they don't want to be seen.

- about where bias or unfairness could show up in systems like this
As stated above bias and unfairness can show up based on what the designer of the sytem wants. For example the companys recommendation system (lets call it a simple system like music recommender) could have a hidden weight thats added to their own content vs content from other parties. This means that the recommendation ssystem will follow the user preferences but the top spots will most likely be original content from the company.



