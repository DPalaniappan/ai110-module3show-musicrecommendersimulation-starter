# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 999.0**  

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
My recommender generates a ranked list of the top-k songs for a listener. It scores each song using energy, valence, danceability, and acousticness, then adds a bonus for matching genre or mood. Each recommendation comes with a short explanation of why it was picked.

- What assumptions does it make about the user  
It assumes the user can state their own preferences, like target energy or whether they like acoustic music. It assumes those preferences stay fixed for the whole session. It does not account for listening history or how taste shifts with mood or context.

- Is this for real users or classroom exploration  
This is a classroom exploration built for a course project. It's meant to demonstrate how a simple, transparent scoring model works, not to serve real listeners.

---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
Each song has a genre, a mood, and four numeric traits: energy, valence, danceability, and acousticness.

- What user preferences are considered  
A user can set a favorite genre, a favorite mood, a target energy, and whether they like acoustic songs. They can also optionally set a target valence and a target danceability.

- How does the model turn those into a score  
For each numeric trait, the model checks how close the song is to the user's target and averages those closeness values, with energy counting for more than the others. Then it adds a small bonus if the song's genre matches the user's favorite genre, and another bonus if the mood matches. The result is a single score, and songs are ranked from highest to lowest score.

- What changes did you make from the starter logic  
I made energy count twice as much as before, since it felt like the trait that most defines a song's overall feel. I also lowered the genre match bonus and raised the mood match bonus, so mood has more influence than genre on the final ranking. I also built out the CLI in main.py to run several sample user profiles at once instead of just one, so I could compare recommendations side by side.


---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
The catalog has 18 songs.

- What genres or moods are represented  
There are 15 genres, including pop, lofi, rock, ambient, jazz, synthwave, hip hop, classical, folk, metal, R&B, reggae, country, and funk. There are 14 moods, like happy, chill, intense, sad, dreamy, angry, and romantic. Most genres and moods appear on only one or two songs each.

- Did you add or remove data  
No, I used the starter dataset as-is and didn't add or remove any songs.

- Are there parts of musical taste missing in the dataset  
Yes. With only 18 songs there and with msot songs only appearing once or twice the catelog cannot really capture how the genre/modd may vary in songs as songs can be multple genres and have different moods throughout the wohle song.

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
It gives reasonable results for users whose favorite genre and mood line up with their numeric targets. For the "High-Energy Pop" and "Chill Lofi" test profiles, the top result was a song that matched on genre, mood, and every numeric trait at once.

- Any patterns you think your scoring captures correctly  
When a user's numeric targets and their favorite genre/mood point to the same songs, those songs reliably rise to the top. The energy weight also does what I intended: songs with very different energy from the target consistently get pushed down the list, even when their mood matches.

- Cases where the recommendations matched your intuition  
"Sunrise City" topping the High-Energy Pop list and "Storm Runner" topping the Deep Intense Rock list both matched what I expected going in. In both cases the winning song matched genre and mood and stayed close on all four numeric traits, so it made sense as the clear best fit.

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

Prompts:  

- Features it does not consider  
Tempo is loaded from the CSV but never used in scoring, so two songs with the same energy and mood but wildly different tempos score identically. The model also ignores artist and title.

- Genres or moods that are underrepresented  
With 18 songs spread across 15 genres and 14 moods, almost every genre and mood is represented by just one or two songs. Genres like classical, folk, funk, and reggae each have exactly one song, so a fan of any of those gets almost no real choice.

- Cases where the system overfits to one preference  
When energy is a poor match, it can drag a song down even if everything else fits. In the "Metal but Low Energy" test, "Iron Fist Rising" matched the user's favorite genre and mood exactly, but its energy was almost the opposite of the target, so it only ranked third instead of first. The heavy energy weight can overrule a genre and mood match that would otherwise feel like the obvious pick.

- Ways the scoring might unintentionally favor some users  
Users who only set target_energy get a score driven almost entirely by that one trait, plus the genre and mood bonus, since there's nothing else to average it against. Users who fill in every optional field get a smoother average across four traits, which waters down how much any single trait, or the genre/mood bonus, can move their score. So the model can behave quite differently depending on how many preferences a user happens to provide.

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested  
I tested four main profiles: High-Energy Pop, Chill Lofi, Deep Intense Rock, and Metal but Low Energy. I also wrote a set of adversarial profiles in main.py, like an empty profile, a zero target_energy, an out-of-range target_energy, a negative target_valence, and mismatched-case genre/mood, to probe edge cases in score_song.

- What you looked for in the recommendations  
For each profile, I checked whether the top song actually matched the user's favorite genre and mood, and whether the ranking order made sense given how close each song's traits were to the targets.

- What surprised you  
The Metal but Low Energy profile surprised me. I expected the metal/angry song to come out on top since it matched both bonus categories, but it landed in third place because its energy was almost the exact opposite of the target. It showed me how much the energy weight can outweigh the genre and mood bonuses combined.

- Any simple tests or comparisons you ran  
I compared the top pick across profiles to see if it always matched genre and mood, and it did for High-Energy Pop, Chill Lofi, and Deep Intense Rock, but not for Metal but Low Energy. 

No need for numeric metrics unless you created some.

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  
