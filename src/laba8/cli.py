import argparse

import requests

from laba8.services.clubs_service import (
    DEFAULT_CLUBS_URL,
    fetch_remote_clubs,
    format_local_clubs,
    format_remote_clubs,
    get_local_clubs,
    search_clubs,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="laba8",
        description="LABA8: CLI with layered architecture (data + services)",
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
        clubs = get_local_clubs()
        for line in format_local_clubs(clubs):
            print(line)

    elif args.command == "search":
        clubs = get_local_clubs()
        results = search_clubs(clubs, args.query)

        if not results:
            print("No matches found")
            return

        for line in format_local_clubs(results):
            print(line)

    elif args.command == "fetch":
        try:
            league_name, clubs = fetch_remote_clubs(args.url, args.limit)
        except requests.RequestException as exc:
            print(f"Request failed: {exc}")
            return

        print(f"Source: {league_name}")
        print(f"Showing first {len(clubs)}: \n")

        for line in format_remote_clubs(clubs):
            print(line)

    else:
        parser.error("Unknown command")
