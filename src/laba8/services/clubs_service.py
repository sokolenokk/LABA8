from typing import Any, Dict, List, Tuple

from laba8.data.http_client import fetch_json

Club = Dict[str, str]

DEFAULT_CLUBS_URL = (
    "https://cdn.jsdelivr.net/npm/football.json@1.0.0/2015-16/en.1.clubs.json"
)


def get_local_clubs() -> List[Club]:
    return [
        {"name": "FC Barcelona", "city": "Barcelona"},
        {"name": "Manchester United", "city": "Manchester"},
        {"name": "Ajax", "city": "Amsterdam"},
        {"name": "PSV", "city": "Eindhoven"},
        {"name": "Bayern Munich", "city": "Munich"},
    ]


def search_clubs(clubs: List[Club], query: str) -> List[Club]:
    q = query.lower()
    results: List[Club] = []

    for club in clubs:
        name = club.get("name", "").lower()
        city = club.get("city", "").lower()

        if q in name or q in city:
            results.append(club)

    return results


def fetch_remote_clubs(url: str, limit: int) -> Tuple[str, List[Dict[str, Any]]]:
    data = fetch_json(url)

    league_name = str(data.get("name", "Unknown league"))
    clubs = data.get("clubs", [])
    if not isinstance(clubs, list):
        clubs = []

    return league_name, clubs[: max(0, limit)]


def format_local_clubs(clubs: List[Club]) -> List[str]:
    lines: List[str] = []
    for club in clubs:
        lines.append(f'{club["name"]} — {club["city"]}')
    return lines


def format_remote_clubs(clubs: List[Dict[str, Any]]) -> List[str]:
    lines: List[str] = []
    for club in clubs:
        name = str(club.get("name", "Unknown club"))
        code = str(club.get("code", "-"))
        country = str(club.get("country", "-"))
        lines.append(f"{name} ({code}) — {country}")
    return lines
