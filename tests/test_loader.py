from optattacklens.loader import load_trace


def test_load_trace():
    steps = load_trace("examples/demo_trace.jsonl")

    assert len(steps) == 3

    assert steps[0].run_id == "run_001"
    assert steps[0].step == 0
    assert steps[0].success is False

    assert steps[2].step == 2
    assert steps[2].success is True
    assert steps[2].score == 0.91