from __future__ import annotations

import argparse

from sqlalchemy import select

from app.db import Base, Food, SessionLocal, engine
from app.openfoodfacts import search_food

LAST_SEARCH_RESULTS: list[dict] = []

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
    global LAST_SEARCH_RESULTS
    results = search_food(query)
    LAST_SEARCH_RESULTS = results
    if not results:
        print("No matching foods found.")
        return

    for index, item in enumerate(results[:10], start=1):
        calories = _format_value(item.get("calories"), " kcal")
        protein = _format_value(item.get("protein"), " g")
        fat = _format_value(item.get("fat"), " g")
        carbs = _format_value(item.get("carbs"), " g")
        print(
            f"{index}. {item.get('product_name', 'Unknown')} - "
            f"calories: {calories}, protein: {protein}, fat: {fat}, carbs: {carbs}"
        )


def import_food(index: int) -> None:
    if not LAST_SEARCH_RESULTS:
        print("No search results available. Run search-food first.")
        return

    if index < 1 or index > len(LAST_SEARCH_RESULTS):
        print(f"Invalid index. Choose between 1 and {len(LAST_SEARCH_RESULTS)}.")
        return

    item = LAST_SEARCH_RESULTS[index - 1]
    name = item.get("product_name", "Unknown")

    with SessionLocal() as session:
        existing = session.query(Food).filter_by(name=name).first()
        if existing:
            print(f"Food already exists: {existing.name}")
            return

        food = Food(name=name)
        session.add(food)
        session.commit()

    print(f"Imported food: {name}")


def import_food(query: str, index: int) -> None:
    results = search_food(query)

    if not results:
        print("No matching foods found.")
        return

    if index < 1 or index > len(results):
        print(f"Invalid index. Choose between 1 and {len(results)}.")
        return

    item = results[index - 1]
    name = item.get("product_name", "Unknown")

    with SessionLocal() as session:
        existing = session.query(Food).filter_by(name=name).first()
        if existing:
            print(f"Food already exists: {existing.name}")
            return

        food = Food(name=name)
        session.add(food)
        session.commit()

    print(f"Imported food: {name}")


def main() -> None:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("hello")
    subparsers.add_parser("init-db")
    subparsers.add_parser("list-foods")
    search_parser = subparsers.add_parser("search-food")
    search_parser.add_argument("query")

    import_parser = subparsers.add_parser("import-food")
    import_parser.add_argument("query")
    import_parser.add_argument("index", type=int)

    args = parser.parse_args()

    if args.command == "hello":
        print("Health tracker is alive.")
    elif args.command == "init-db":
        init_db()
    elif args.command == "list-foods":
        list_foods()
    elif args.command == "search-food":
        search_foods(args.query)
    elif args.command == "import-food":
        import_food(args.query, args.index)


if __name__ == "__main__":
    main()