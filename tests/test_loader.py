from optattacklens.loader import load_trace


def test_load_trace(tmp_path):
    trace_path = tmp_path / "trace.jsonl"

    trace_path.write_text(
        "\n".join(
            [
                '{"run_id":"run_001","step":0,"queries":1,"success":false}',
                '{"run_id":"run_001","step":1,"queries":2,"success":false}',
                '{"run_id":"run_001","step":2,"queries":3,"success":true}',
            ]
        ),
        encoding="utf-8",
    )

    steps = load_trace(trace_path)

    assert len(steps) == 3

    assert steps[0].run_id == "run_001"
    assert steps[0].step == 0
    assert steps[0].success is False

    assert steps[2].step == 2
    assert steps[2].success is True