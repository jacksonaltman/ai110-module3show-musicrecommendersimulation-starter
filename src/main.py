"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    # Taste profile: a chill, acoustic-leaning lofi listener
    user_prefs = {
        "genre": "lofi",
        "mood": "chill",
        "energy": 0.40,
        "likes_acoustic": True,
    }

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print(f"\nProfile: {user_prefs['genre']} / {user_prefs['mood']} / "
          f"energy {user_prefs['energy']:.2f} / "
          f"{'acoustic' if user_prefs['likes_acoustic'] else 'non-acoustic'}")
    print("\nTop recommendations:")
    print("=" * 60)
    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"\n{rank}. {song['title']} by {song['artist']}")
        print(f"   Score: {score:.2f} / 6.00")
        print("   Why:")
        for reason in explanation.split("; "):
            print(f"     - {reason}")
    print()


if __name__ == "__main__":
    main()
