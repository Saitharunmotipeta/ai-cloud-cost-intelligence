from pathlib import Path
import csv
import json

ROOT = Path(__file__).resolve().parent.parent

DATA_DIR = ROOT / "data"
REPORTS_DIR = ROOT / "reports"

CSV_FILE = DATA_DIR / "deployment_history.csv"
JSON_FILE = DATA_DIR / "deployment_statistics.json"
SUMMARY_FILE = REPORTS_DIR / "benchmark_summary.md"

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


CSV_HEADERS = [

    "benchmark_run_id",

    "timestamp",

    "commit_sha",

    "branch",

    "triggered_by",

    "deployment_duration_sec",

    "frontend_build_duration_sec",

    "backend_build_duration_sec",

    "frontend_build_size_kb",

    "containers_running",

    "health_checks_total",

    "health_checks_passed",

    "health_success_rate",

    *RUNTIME_METRICS,

    "deployment_status",
]
def ensure_workspace():

    DATA_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    REPORTS_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    if not CSV_FILE.exists():

        with open(
            CSV_FILE,
            "w",
            newline="",
            encoding="utf-8",
        ) as file:

            writer = csv.writer(file)
            writer.writerow(CSV_HEADERS)

    if not JSON_FILE.exists():

        with open(
            JSON_FILE,
            "w",
            encoding="utf-8",
        ) as file:

            json.dump(
                {},
                file,
                indent=4,
            )

    if not SUMMARY_FILE.exists():

        SUMMARY_FILE.write_text(
            """# Deployment Benchmark Summary

This report is generated automatically.

No deployment history available yet.
""",
            encoding="utf-8",
        )