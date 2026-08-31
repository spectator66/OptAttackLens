from optattacklens.schema import AttackStep
from optattacklens.summary import summarize_trace


def test_summarize_trace():
    steps = [
        AttackStep(
            run_id="run_001",
            step=0,
            queries=3,
            success=True,
        ),
        AttackStep(
            run_id="run_002",
            step=0,
            queries=8,
            success=True,
        ),
        AttackStep(
            run_id="run_003",
            step=0,
            queries=20,
            success=True,
        ),
        AttackStep(
            run_id="run_004",
            step=0,
            queries=25, 
            success=False,
        ),
    ]

    summary = summarize_trace(
        steps,
        budgets=[5, 10, 20],
    )

    assert summary["asr"] == 0.75
    assert summary["median_queries_to_success"] == 8.0

    assert summary["asr_at_5"] == 0.25
    assert summary["asr_at_10"] == 0.5
    assert summary["asr_at_20"] == 0.75
def test_summarize_trace_default_budgets():
    steps = [
        AttackStep(
            run_id="run_001",
            step=0,
            queries=3,
            success=True,
        )
    ]

    summary = summarize_trace(steps)

    assert "asr_at_5" in summary
    assert "asr_at_10" in summary
    assert "asr_at_20" in summary
def test_summarize_empty_trace():
    summary = summarize_trace([])

    assert summary["asr"] == 0.0
    assert summary["median_queries_to_success"] is None
    assert summary["asr_at_5"] == 0.0
