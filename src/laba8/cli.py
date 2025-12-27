import argparse
from typing import Dict, List

import requests


CLUBS: List[Dict[str, str]] = [
    {"name": "FC Barcelona", "city": "Barcelona"},
    {"name": "Manchester United", "city": "Manchester"},
    {"name": "Ajax", "city": "Amsterdam"},
    {"name": "PSV", "city": "Eindhoven"},
    {"name": "Bayern Munich", "city": "Munich"},
]

DEFAULT_CLUBS_URL = (
    "https://cdn.jsdelivr.net/npm/football.json@1.0.0/2015-16/en.1.clubs.json"
)


def cmd_list() -> None:
    for club in CLUBS:
        print(f'{club["name"]} — {club["city"]}')


def cmd_search(query: str) -> None:
    query_lower = query.lower()

    results: List[Dict[str, str]] = []
    for club in CLUBS:
        name = club["name"].lower()
        city = club["city"].lower()

        if query_lower in name or query_lower in city:
            results.append(club)

    if not results:
        print("No matches found")
        return

    for club in results:
        print(f'{club["name"]} — {club["city"]}')


def cmd_fetch(url: str, limit: int) -> None:
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.RequestException as exc:
        print(f"Request failed: {exc}")
        return

    data = response.json()

    league_name = data.get("name", "Unknown league")
    clubs = data.get("clubs", [])

    print(f"Source: {league_name}")
    print(f"Total clubs: {len(clubs)}")
    print(f"Showing first {min(limit, len(clubs))}: \n")

    for club in clubs[:limit]:
        club_name = club.get("name", "Unknown club")
        code = club.get("code", "-")
        country = club.get("country", "-")
        print(f"{club_name} ({code}) — {country}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="laba8",
        description="LABA8: CLI on argparse + requests",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("list", help="Show all local clubs")

    search_parser = subparsers.add_parser(
        "search",
        help="Search local clubs by text",
    )
    search_parser.add_argument(
        "query",
        help="Text to search in club name or city",
    )

    fetch_parser = subparsers.add_parser(
        "fetch",
        help="Fetch clubs list from the internet (requests)",
    )
    fetch_parser.add_argument(
        "--url",
        default=DEFAULT_CLUBS_URL,
        help="JSON URL to fetch clubs from",
    )
    fetch_parser.add_argument(
        "--limit",
        type=int,
        default=5,
        help="How many clubs to print",
    )

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "list":
        cmd_list()
    elif args.command == "search":
        cmd_search(args.query)
    elif args.command == "fetch":
        cmd_fetch(args.url, args.limit)
    else:
        parser.error("Unknown command")


if __name__ == "__main__":
    main()
