import argparse
from typing import List, Dict


CLUBS: List[Dict[str, str]] = [
    {"name": "FC Barcelona", "city": "Barcelona"},
    {"name": "Manchester United", "city": "Manchester"},
    {"name": "Ajax", "city": "Amsterdam"},
    {"name": "PSV", "city": "Eindhoven"},
    {"name": "Bayern Munich", "city": "Munich"},
]


def cmd_list() -> None:
    for club in CLUBS:
        print(f'{club["name"]} — {club["city"]}')


def cmd_search(query: str) -> None:
    query_lower = query.lower()

    results = []
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


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="laba8",
        description="Простые аргпарсы",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("list", help="Все клубы")

    search_parser = subparsers.add_parser(
        "search", help="Клуб по названию или городу")
    search_parser.add_argument("query", help="Название или город")

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "list":
        cmd_list()
    elif args.command == "search":
        cmd_search(args.query)
    else:
        parser.error("Unknown command")


if __name__ == "__main__":
    main()
