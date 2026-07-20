import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool
    target_valence: Optional[float] = None
    target_danceability: Optional[float] = None

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """Loads songs from a CSV file into a list of dicts."""
    int_fields = {"id"}
    float_fields = {"energy", "tempo_bpm", "valence", "danceability", "acousticness"}

    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            for field in int_fields:
                row[field] = int(row[field])
            for field in float_fields:
                row[field] = float(row[field])
            songs.append(row)
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Scores a song against user preferences, returning a score and list of reasons."""
    weights = {"energy": 2.0, "valence": 1.0, "danceability": 1.0, "acousticness": 1.0}
    reasons: List[str] = []
    weighted_sum = 0.0
    total_weight = 0.0

    target_energy = user_prefs.get("target_energy")
    if target_energy is not None:
        closeness = 1 - abs(song["energy"] - target_energy)
        weighted_sum += weights["energy"] * closeness
        total_weight += weights["energy"]
        reasons.append(f"Energy is a {closeness:.0%} match (song: {song['energy']:.2f}, target: {target_energy:.2f})")

    target_valence = user_prefs.get("target_valence")
    if target_valence is not None:
        closeness = 1 - abs(song["valence"] - target_valence)
        weighted_sum += weights["valence"] * closeness
        total_weight += weights["valence"]
        reasons.append(f"Valence is a {closeness:.0%} match (song: {song['valence']:.2f}, target: {target_valence:.2f})")

    target_danceability = user_prefs.get("target_danceability")
    if target_danceability is not None:
        closeness = 1 - abs(song["danceability"] - target_danceability)
        weighted_sum += weights["danceability"] * closeness
        total_weight += weights["danceability"]
        reasons.append(f"Danceability is a {closeness:.0%} match (song: {song['danceability']:.2f}, target: {target_danceability:.2f})")

    likes_acoustic = user_prefs.get("likes_acoustic")
    if likes_acoustic is not None:
        target_acousticness = 0.8 if likes_acoustic else 0.2
        closeness = 1 - abs(song["acousticness"] - target_acousticness)
        weighted_sum += weights["acousticness"] * closeness
        total_weight += weights["acousticness"]
        reasons.append(f"Acousticness is a {closeness:.0%} match (song: {song['acousticness']:.2f}, target: {target_acousticness:.2f})")

    numeric_score = weighted_sum / total_weight if total_weight > 0 else 0.0

    bonus = 0.0
    favorite_genre = user_prefs.get("favorite_genre")
    if favorite_genre and song.get("genre") == favorite_genre:
        bonus += 0.3
        reasons.append(f"Genre matches your favorite genre: {favorite_genre}")

    favorite_mood = user_prefs.get("favorite_mood")
    if favorite_mood and song.get("mood") == favorite_mood:
        bonus += 0.3
        reasons.append(f"Mood matches your favorite mood: {favorite_mood}")

    score = numeric_score + bonus

    if not reasons:
        reasons.append("No preferences provided to compare against.")

    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Returns the top-k songs sorted by score, each paired with its score and explanation."""
    scored = sorted(
        ((song, *score_song(user_prefs, song)) for song in songs),
        key=lambda result: result[1],
        reverse=True,
    )
    return [(song, score, "; ".join(reasons)) for song, score, reasons in scored[:k]]
