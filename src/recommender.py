import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, asdict

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

MOOD_POINTS = 2.0
GENRE_POINTS = 1.0
ENERGY_POINTS = 2.0
ACOUSTIC_POINTS = 1.0
ACOUSTIC_HIGH = 0.6
ACOUSTIC_LOW = 0.3


class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return the top k songs for the user, best match first."""
        prefs = _profile_to_prefs(user)
        ranked = sorted(self.songs, key=lambda s: score_song(prefs, asdict(s))[0], reverse=True)
        return ranked[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Explain in one line why the song matches the user's profile."""
        _, reasons = score_song(_profile_to_prefs(user), asdict(song))
        return "; ".join(reasons) if reasons else "No strong matches with your profile"


def _profile_to_prefs(user: UserProfile) -> Dict:
    """Convert a UserProfile into the dict format used by score_song."""
    return {
        "genre": user.favorite_genre,
        "mood": user.favorite_mood,
        "energy": user.target_energy,
        "likes_acoustic": user.likes_acoustic,
    }


def load_songs(csv_path: str) -> List[Dict]:
    """Read songs.csv into a list of dicts, converting numeric columns to int/float."""
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            row["id"] = int(row["id"])
            row["tempo_bpm"] = int(row["tempo_bpm"])
            for key in ("energy", "valence", "danceability", "acousticness"):
                row[key] = float(row[key])
            songs.append(row)
    return songs


def max_score() -> float:
    """Return the highest score a song can earn under the current weights."""
    return MOOD_POINTS + GENRE_POINTS + ENERGY_POINTS + ACOUSTIC_POINTS


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score one song against user preferences, returning (score, reasons)."""
    score = 0.0
    reasons = []

    if song["mood"] == user_prefs["mood"]:
        score += MOOD_POINTS
        reasons.append(f"mood match: {song['mood']} (+{MOOD_POINTS:.1f})")

    if song["genre"] == user_prefs["genre"]:
        score += GENRE_POINTS
        reasons.append(f"genre match: {song['genre']} (+{GENRE_POINTS:.1f})")

    closeness = 1 - abs(song["energy"] - user_prefs["energy"])
    energy_points = ENERGY_POINTS * closeness
    score += energy_points
    reasons.append(
        f"energy {song['energy']:.2f} vs target {user_prefs['energy']:.2f} (+{energy_points:.2f})"
    )

    acousticness = song["acousticness"]
    if user_prefs["likes_acoustic"] and acousticness > ACOUSTIC_HIGH:
        score += ACOUSTIC_POINTS
        reasons.append(f"acoustic sound: {acousticness:.2f} (+{ACOUSTIC_POINTS:.1f})")
    elif not user_prefs["likes_acoustic"] and acousticness < ACOUSTIC_LOW:
        score += ACOUSTIC_POINTS
        reasons.append(f"non-acoustic sound: {acousticness:.2f} (+{ACOUSTIC_POINTS:.1f})")

    return score, reasons


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Score every song, then return the top k as (song, score, explanation), best first."""
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        scored.append((song, score, "; ".join(reasons)))
    return sorted(scored, key=lambda item: item[1], reverse=True)[:k]
