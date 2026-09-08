import json

from optattacklens.export import (
    save_summary_csv,
    save_summary_json,
)


def test_save_summary_json(tmp_path):
    summary = {
        "asr": 0.75,
        "median_queries_to_success": 5.0,
    }

    output_path = tmp_path / "summary.json"

    save_summary_json(summary, output_path)

    with output_path.open("r", encoding="utf-8") as file:
        saved = json.load(file)

    assert saved == summary


def test_save_summary_csv(tmp_path):
    summary = {
        "asr": 0.75,
        "median_queries_to_success": 5.0,
    }

    output_path = tmp_path / "summary.csv"

    save_summary_csv(summary, output_path)

    content = output_path.read_text(encoding="utf-8")

    assert "metric,value" in content
    assert "asr,0.75" in content
