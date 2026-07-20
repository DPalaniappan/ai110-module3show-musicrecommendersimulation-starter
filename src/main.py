"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv")
    

    # Starter example profile
    user_prefs = {
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 0.8,
        "likes_acoustic": False,
    }

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("\n" + "=" * 50)
    print("USER PROFILE")
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


if __name__ == "__main__":
    main()
