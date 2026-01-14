from __future__ import annotations

import argparse

from sqlalchemy import select

from app.db import Base, Food, SessionLocal, engine
from app.openfoodfacts import search_food


def init_db() -> None:
    Base.metadata.create_all(engine)
    print("Database initialized.")


def list_foods() -> None:
    with SessionLocal() as session:
        foods = session.scalars(select(Food).order_by(Food.id)).all()

    if not foods:
        print("No foods found.")
        return

    for food in foods:
        print(f"{food.id}: {food.name}")


def _format_value(value: float | None, unit: str) -> str:
    if value is None:
        return "N/A"
    return f"{value:g}{unit}"


def search_foods(query: str) -> None:
    results = search_food(query)
    if not results:
        print("No matching foods found.")
        return

    for index, item in enumerate(results[:5], start=1):
        calories = _format_value(item.get("calories"), " kcal")
        protein = _format_value(item.get("protein"), " g")
        fat = _format_value(item.get("fat"), " g")
        carbs = _format_value(item.get("carbs"), " g")
        print(
            f"{index}. {item.get('product_name', 'Unknown')} - "
            f"calories: {calories}, protein: {protein}, fat: {fat}, carbs: {carbs}"
        )


def main() -> None:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("hello")
    subparsers.add_parser("init-db")
    subparsers.add_parser("list-foods")
    search_parser = subparsers.add_parser("search-food")
    search_parser.add_argument("query")

    args = parser.parse_args()

    if args.command == "hello":
        print("Health tracker is alive.")
    elif args.command == "init-db":
        init_db()
    elif args.command == "list-foods":
        list_foods()
    elif args.command == "search-food":
        search_foods(args.query)


if __name__ == "__main__":
    main()
