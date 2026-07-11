from __future__ import annotations

import csv
import json

from benchmark_utils import (
    ensure_workspace,
    CSV_FILE,
    JSON_FILE,
)

from statistics_utils import (
    safe_float,
    is_numeric_column,
    calculate_statistics,
)


def generate_statistics():

    ensure_workspace()

    with open(
        CSV_FILE,
        "r",
        encoding="utf-8",
    ) as file:

        reader = list(csv.DictReader(file))

    deployment_count = len(reader)

    successful = sum(
        row["deployment_status"] == "SUCCESS"
        for row in reader
    )

    failed = deployment_count - successful

    success_rate = (
        round(
            (successful / deployment_count) * 100,
            2,
        )
        if deployment_count
        else 0
    )

    metrics = {}

    if deployment_count:

        headers = reader[0].keys()

        ignored = {

            "benchmark_run_id",
            "timestamp",
            "commit_sha",
            "branch",
            "triggered_by",
            "deployment_status",

        }

        for header in headers:

            if header in ignored:
                continue

            values = [

                row[header]

                for row in reader

            ]

            if not is_numeric_column(values):
                continue

            numeric_values = [

                safe_float(v)

                for v in values

                if safe_float(v) is not None

            ]

            metrics[header] = calculate_statistics(
                numeric_values
            )

    output = {

        "deployment_count": deployment_count,

        "successful_deployments": successful,

        "failed_deployments": failed,

        "success_rate": success_rate,

        "metrics": metrics,

    }

    with open(
        JSON_FILE,
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            output,
            file,
            indent=4,
        )

    print(
        "✅ Deployment statistics generated."
    )


if __name__ == "__main__":
    generate_statistics()