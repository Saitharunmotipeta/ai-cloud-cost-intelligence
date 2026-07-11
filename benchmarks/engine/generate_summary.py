from __future__ import annotations

import json

from benchmark_utils import (
    ensure_workspace,
    JSON_FILE,
    SUMMARY_FILE,
)


def title(text: str) -> str:
    """
    Convert:

    llm_reasoning_ms

    into

    LLM Reasoning (ms)
    """

    text = text.replace("_ms", " (ms)")
    text = text.replace("_sec", " (sec)")
    text = text.replace("_kb", " (KB)")
    text = text.replace("_", " ")

    return text.title()


def generate_summary():

    ensure_workspace()

    with open(
        JSON_FILE,
        "r",
        encoding="utf-8",
    ) as file:

        data = json.load(file)

    lines = []

    lines.append("# AI Cloud Cost Intelligence")
    lines.append("")
    lines.append("## Deployment Benchmark Report")
    lines.append("")

    lines.append(
        f"**Deployments :** {data['deployment_count']}"
    )

    lines.append(
        f"**Successful :** {data['successful_deployments']}"
    )

    lines.append(
        f"**Failed :** {data['failed_deployments']}"
    )

    lines.append(
        f"**Success Rate :** {data['success_rate']}%"
    )

    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Metric Statistics")
    lines.append("")

    metrics = data.get("metrics", {})

    for metric, stats in metrics.items():

        lines.append(f"### {title(metric)}")
        lines.append("")

        lines.append(
            f"- Samples : {stats['count']}"
        )

        lines.append(
            f"- Average : {stats['average']}"
        )

        lines.append(
            f"- Median : {stats['median']}"
        )

        lines.append(
            f"- Minimum : {stats['minimum']}"
        )

        lines.append(
            f"- Maximum : {stats['maximum']}"
        )

        lines.append("")

    lines.append("---")
    lines.append("")
    lines.append(
        "Generated automatically by the AI Cloud Cost Intelligence Benchmark Engine."
    )

    SUMMARY_FILE.write_text(
        "\n".join(lines),
        encoding="utf-8",
    )

    print(
        "✅ Benchmark summary generated."
    )


if __name__ == "__main__":
    generate_summary()