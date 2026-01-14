from __future__ import annotations

import argparse

from sqlalchemy import select

from app.db import Base, Food, SessionLocal, engine


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


def main() -> None:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("hello")
    subparsers.add_parser("init-db")
    subparsers.add_parser("list-foods")

    args = parser.parse_args()

    if args.command == "hello":
        print("Health tracker is alive.")
    elif args.command == "init-db":
        init_db()
    elif args.command == "list-foods":
        list_foods()


if __name__ == "__main__":
    main()
