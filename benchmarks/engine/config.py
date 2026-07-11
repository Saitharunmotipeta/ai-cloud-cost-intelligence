from __future__ import annotations

import os
import uuid
from datetime import datetime, timezone


def benchmark_run_id() -> str:
    """
    Example:
    BM-20260712-4A8F32
    """
    return (
        "BM-"
        + datetime.now(timezone.utc).strftime("%Y%m%d")
        + "-"
        + uuid.uuid4().hex[:6].upper()
    )


def env(name: str, default: str = "") -> str:
    return os.getenv(name, default)


DEPLOYMENT = {

    "run_id": benchmark_run_id(),

    "timestamp": env("DEPLOYMENT_TIMESTAMP"),

    "commit_sha": env("COMMIT_SHA"),

    "branch": env("BRANCH_NAME"),

    "triggered_by": env("TRIGGERED_BY"),

    "deployment_duration_sec": env(
        "DEPLOYMENT_DURATION_SEC"
    ),

    "frontend_build_duration_sec": env(
        "FRONTEND_BUILD_DURATION_SEC"
    ),

    "backend_build_duration_sec": env(
        "BACKEND_BUILD_DURATION_SEC"
    ),

    "frontend_build_size_kb": env(
        "FRONTEND_BUILD_SIZE_KB"
    ),

    "containers_running": env(
        "CONTAINERS_RUNNING"
    ),

    "health_checks_total": env(
        "HEALTH_CHECKS_TOTAL"
    ),

    "health_checks_passed": env(
        "HEALTH_CHECKS_PASSED"
    ),

    "health_success_rate": env(
        "HEALTH_SUCCESS_RATE"
    ),

    "deployment_status": env(
        "DEPLOYMENT_STATUS",
        "SUCCESS",
    ),
}

# ==========================================================
# Runtime Metrics
# ==========================================================

RUNTIME_METRICS = [

    "ingestion_request_processing_ms",

    "analytics_queue_receive_ms",
    "analytics_processing_ms",
    "analytics_consumer_loop_ms",

    "context_retrieval_ms",
    "llm_reasoning_ms",
    "graph_execution_ms",
    "pipeline_processing_ms",

    "database_insert_ms",

    "graphql_query_execution_ms",

    "total_ai_pipeline_ms",
]

for metric in RUNTIME_METRICS:

    DEPLOYMENT[metric] = env(metric.upper())