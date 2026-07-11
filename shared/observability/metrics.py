from __future__ import annotations

from time import perf_counter
from typing import Any

from shared.events.base_event import BaseEvent


def start_timer() -> float:
    """
    Start a high-resolution timer.
    """
    return perf_counter()


def stop_timer(start: float) -> float:
    """
    Stop timer and return elapsed time in milliseconds.
    """
    return (perf_counter() - start) * 1000


def record_metric(
    event: BaseEvent,
    service: str,
    metric: str,
    value: Any,
) -> None:
    """
    Record a runtime metric inside the event metadata.

    Example:

    metadata = {
        "metrics": {
            "ingestion": {
                "request_processing_ms": 18.42
            }
        }
    }
    """

    if event.metadata is None:
        event.metadata = {}

    metrics = event.metadata.setdefault(
        "metrics",
        {}
    )

    service_metrics = metrics.setdefault(
        service,
        {}
    )

    if isinstance(value, (int, float)):
        value = round(value, 2)

    service_metrics[metric] = value