from __future__ import annotations

import statistics
from typing import Iterable


def safe_float(value: str):

    if value is None:
        return None

    value = str(value).strip()

    if value == "":
        return None

    try:
        return float(value)
    except ValueError:
        return None


def is_numeric_column(values: Iterable[str]) -> bool:

    for value in values:

        if safe_float(value) is not None:
            return True

    return False


def calculate_statistics(values: list[float]):

    if not values:

        return {
            "count": 0,
            "average": 0,
            "median": 0,
            "minimum": 0,
            "maximum": 0,
        }

    return {

        "count": len(values),

        "average": round(
            statistics.mean(values),
            2,
        ),

        "median": round(
            statistics.median(values),
            2,
        ),

        "minimum": round(
            min(values),
            2,
        ),

        "maximum": round(
            max(values),
            2,
        ),
    }