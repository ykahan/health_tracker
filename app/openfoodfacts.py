from __future__ import annotations

from typing import Any

import requests


SEARCH_URL = "https://world.openfoodfacts.org/cgi/search.pl"


def _get_nutrient_value(nutriments: dict[str, Any], key: str) -> float | None:
    value = nutriments.get(key)
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def search_food(query: str) -> list[dict]:
    response = requests.get(
        SEARCH_URL,
        params={
            "search_terms": query,
            "search_simple": 1,
            "action": "process",
            "json": 1,
            "page_size": 5,
        },
        timeout=10,
    )
    response.raise_for_status()
    data = response.json()
    results = []

    for product in data.get("products", []):
        nutriments = product.get("nutriments", {})
        results.append(
            {
                "product_name": product.get("product_name")
                or product.get("product_name_en")
                or "Unknown",
                "calories": _get_nutrient_value(nutriments, "energy-kcal_100g"),
                "protein": _get_nutrient_value(nutriments, "proteins_100g"),
                "fat": _get_nutrient_value(nutriments, "fat_100g"),
                "carbs": _get_nutrient_value(nutriments, "carbohydrates_100g"),
            }
        )

    return results
