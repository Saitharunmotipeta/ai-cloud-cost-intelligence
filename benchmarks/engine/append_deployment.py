import csv

from config import (
    DEPLOYMENT,
    RUNTIME_METRICS,
)

from benchmark_utils import (
    ensure_workspace,
    CSV_FILE,
)


def append_deployment():

    ensure_workspace()

    # --------------------------------------------------
    # Prevent duplicate deployment entries
    # --------------------------------------------------

    with open(
        CSV_FILE,
        "r",
        encoding="utf-8",
    ) as file:

        reader = csv.DictReader(file)

        for row in reader:

            if row["commit_sha"] == DEPLOYMENT["commit_sha"]:

                print(
                    "⚠️ Deployment already recorded."
                )

                return

    # --------------------------------------------------
    # Append deployment
    # --------------------------------------------------

    with open(
        CSV_FILE,
        "a",
        newline="",
        encoding="utf-8",
    ) as file:

        writer = csv.writer(file)

        writer.writerow([

            # ==========================================
            # Deployment Information
            # ==========================================

            DEPLOYMENT["run_id"],
            DEPLOYMENT["timestamp"],
            DEPLOYMENT["commit_sha"],
            DEPLOYMENT["branch"],
            DEPLOYMENT["triggered_by"],

            # ==========================================
            # Deployment Metrics
            # ==========================================

            DEPLOYMENT["deployment_duration_sec"],
            DEPLOYMENT["frontend_build_duration_sec"],
            DEPLOYMENT["backend_build_duration_sec"],
            DEPLOYMENT["frontend_build_size_kb"],
            DEPLOYMENT["containers_running"],
            DEPLOYMENT["health_checks_total"],
            DEPLOYMENT["health_checks_passed"],
            DEPLOYMENT["health_success_rate"],
            *[
                DEPLOYMENT.get(
                    metric,
                    ""
                )
                for metric in RUNTIME_METRICS
            ],
            # ==========================================
            # Final Status
            # ==========================================

            DEPLOYMENT["deployment_status"],

        ])

    print(
        "✅ Deployment benchmark appended successfully."
    )


if __name__ == "__main__":
    append_deployment()