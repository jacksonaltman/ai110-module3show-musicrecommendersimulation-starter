"""
Command line runner for the Music Recommender Simulation.

Loads the song catalog, then prints the top 5 recommendations for each
taste profile below: three typical listeners and four adversarial ones
designed to stress the scoring logic.
"""

from src.recommender import load_songs, recommend_songs, max_score

PROFILES = {
    # Typical listeners
    "High-Energy Pop": {"genre": "pop", "mood": "happy", "energy": 0.85, "likes_acoustic": False},
    "Chill Lofi": {"genre": "lofi", "mood": "chill", "energy": 0.40, "likes_acoustic": True},
    "Deep Intense Rock": {"genre": "rock", "mood": "intense", "energy": 0.92, "likes_acoustic": False},
    # Adversarial: conflicting, missing, or uninformative preferences
    "Sad Banger (conflicting)": {"genre": "classical", "mood": "sad", "energy": 0.90, "likes_acoustic": True},
    "K-Pop Fan (genre not in catalog)": {"genre": "k-pop", "mood": "happy", "energy": 0.80, "likes_acoustic": False},
    "Metal Fan Who Wants Chill (genre vs mood)": {"genre": "metal", "mood": "chill", "energy": 0.50, "likes_acoustic": False},
    "No Stated Taste (energy only)": {"genre": "none", "mood": "none", "energy": 0.50, "likes_acoustic": True},
}


def show(name: str, user_prefs: dict, songs: list) -> None:
    """Print the top 5 recommendations for one profile."""
    print(f"\nProfile: {name}")
    print(f"  genre={user_prefs['genre']}, mood={user_prefs['mood']}, "
          f"energy={user_prefs['energy']:.2f}, likes_acoustic={user_prefs['likes_acoustic']}")
    print("=" * 60)
    for rank, (song, score, explanation) in enumerate(recommend_songs(user_prefs, songs, k=5), start=1):
        print(f"\n{rank}. {song['title']} by {song['artist']} ({song['genre']}/{song['mood']})")
        print(f"   Score: {score:.2f} / {max_score():.2f}")
        for reason in explanation.split("; "):
            print(f"     - {reason}")


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")
    for name, user_prefs in PROFILES.items():
        show(name, user_prefs, songs)
    print()


if __name__ == "__main__":
    main()
