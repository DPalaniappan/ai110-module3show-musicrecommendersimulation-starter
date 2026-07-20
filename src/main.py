"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs


def print_recommendations(profile_name, user_prefs, recommendations) -> None:
    """Prints a user profile and its top recommendations in a clean CLI layout."""
    print("\n" + "=" * 50)
    print(f"USER PROFILE: {profile_name}")
    print("=" * 50)
    for key, value in user_prefs.items():
        print(f"   {key}: {value}")

    print("\n" + "=" * 50)
    print("TOP RECOMMENDATIONS")
    print("=" * 50)
    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        reasons = explanation.split("; ")
        print(f"\n{rank}. {song['title']}  (Score: {score:.2f})")
        print("-" * 50)
        for reason in reasons:
            print(f"   • {reason}")
    print()


def print_profile_recommendations(profiles, songs, k: int = 5) -> None:
    """Runs and prints recommendations for each profile in a {name: user_prefs} dict."""
    for profile_name, user_prefs in profiles.items():
        recommendations = recommend_songs(user_prefs, songs, k=k)
        print_recommendations(profile_name, user_prefs, recommendations)


def main() -> None:
    songs = load_songs("data/songs.csv")
    # Starter example profile
    user_prefs = {
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 0.8,
        "likes_acoustic": False,
    }
    # Example user preference profiles
    user_profiles = {
        "High-Energy Pop": {
            "favorite_genre": "pop",
            "favorite_mood": "happy",
            "target_energy": 0.9,
            "likes_acoustic": False,
            "target_valence": 0.8,
            "target_danceability": 0.85,
        },
        "Chill Lofi": {
            "favorite_genre": "lofi",
            "favorite_mood": "chill",
            "target_energy": 0.3,
            "likes_acoustic": True,
            "target_valence": 0.55,
            "target_danceability": 0.5,
        },
        "Deep Intense Rock": {
            "favorite_genre": "rock",
            "favorite_mood": "intense",
            "target_energy": 0.9,
            "likes_acoustic": False,
            "target_valence": 0.4,
            "target_danceability": 0.5,
        },
        "Metal but Low Energy": {
            "favorite_genre": "metal",
            "favorite_mood": "angry",
            "target_energy": 0.1,
            "likes_acoustic": False,
        },
    }

    print_profile_recommendations(user_profiles, songs)

    # Adversarial / edge-case profiles designed to probe weaknesses in score_song's
    # logic (see README/chat notes for what to look for in each one's output).
    adversarial_profiles = {
        "Empty Preferences": {},
        "Zero Energy (Falsy Value)": {
            "favorite_genre": "lofi",
            "favorite_mood": "chill",
            "target_energy": 0.0,
            "likes_acoustic": False,
        },
        "Out-of-Range Target Energy": {
            "favorite_genre": "pop",
            "favorite_mood": "happy",
            "target_energy": 5.0,
            "likes_acoustic": False,
        },
        "Negative Target Valence": {
            "favorite_genre": "hip hop",
            "favorite_mood": "sad",
            "target_energy": 0.4,
            "likes_acoustic": False,
            "target_valence": -3.0,
        },
        "Case-Mismatched Genre/Mood": {
            "favorite_genre": "Pop",
            "favorite_mood": "Happy",
            "target_energy": 0.8,
            "likes_acoustic": False,
        },
        "Nonexistent Genre/Mood": {
            "favorite_genre": "polka",
            "favorite_mood": "euphoric",
            "target_energy": 0.6,
            "likes_acoustic": False,
        },
        "Single-Factor Extreme (Energy Only)": {
            "favorite_genre": "",
            "favorite_mood": "",
            "target_energy": 0.9,
            "likes_acoustic": None,
        },
        "Bonus-Overrides-Mismatch (Metal but Low Energy)": {
            "favorite_genre": "metal",
            "favorite_mood": "angry",
            "target_energy": 0.1,
            "likes_acoustic": False,
        },
        "Impossible Combo (Max Everything + No Acoustic)": {
            "favorite_genre": "pop",
            "favorite_mood": "happy",
            "target_energy": 1.0,
            "likes_acoustic": False,
            "target_valence": 1.0,
            "target_danceability": 1.0,
        },
        "Trailing Whitespace Genre": {
            "favorite_genre": "pop ",
            "favorite_mood": "happy",
            "target_energy": 0.8,
            "likes_acoustic": False,
        },
    }
    print("\n" + "=" * 50)
    print("ADVERSARIAL / EDGE CASE PROFILES")
    print("=" * 50)
    #print_profile_recommendations(adversarial_profiles, songs)


if __name__ == "__main__":
    main()
