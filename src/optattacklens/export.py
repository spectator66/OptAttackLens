import csv
import json
from pathlib import Path


def save_summary_json(
    summary: dict[str, float | None],
    path: str | Path,
) -> None:
    """Save a summary dictionary as JSON."""

    output_path = Path(path)

    with output_path.open("w", encoding="utf-8") as file:
        json.dump(
            summary,
            file,
            indent=2,
        )


def save_summary_csv(
    summary: dict[str, float | None],
    path: str | Path,
) -> None:
    """Save a summary dictionary as CSV."""

    output_path = Path(path)

    with output_path.open(
        "w",
        encoding="utf-8",
        newline="",
    ) as file:
        writer = csv.writer(file)

        writer.writerow(["metric", "value"])

        for metric, value in summary.items():
            writer.writerow([metric, value])
