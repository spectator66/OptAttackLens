from optattacklens.schema import AttackStep
from optattacklens.summary import (
    mean_longest_plateau,
    mean_time_to_best,  
    summarize_trace,
)

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

def test_mean_time_to_best():
    steps = [
        AttackStep(
            run_id="run_001",
            step=0,
            queries=1,
            success=False,
            score=0.10,
        ),
        AttackStep(
            run_id="run_001",
            step=2,
            queries=3,
            success=True,
            score=0.90,
        ),
        AttackStep(
            run_id="run_002",
            step=0,
            queries=1,
            success=False,
            score=0.20,
        ),
        AttackStep(
            run_id="run_002",
            step=4,
            queries=5,
            success=True,
            score=0.80,
        ),
    ]

    assert mean_time_to_best(steps) == 3.0

def test_mean_longest_plateau():
    steps = [
        AttackStep(
            run_id="run_001",
            step=0,
            queries=1,
            success=False,
            score=0.10,
        ),
        AttackStep(
            run_id="run_001",
            step=1,
            queries=2,
            success=False,
            score=0.40,
        ),
        AttackStep(
            run_id="run_001",
            step=2,
            queries=3,
            success=False,
            score=0.30,
        ),
        AttackStep(
            run_id="run_001",
            step=3,
            queries=4,
            success=True,
            score=0.50,
        ),
        AttackStep(
            run_id="run_002",
            step=0,
            queries=1,
            success=False,
            score=0.20,
        ),
        AttackStep(
            run_id="run_002",
            step=1,
            queries=2,
            success=False,
            score=0.20,
        ),
        AttackStep(
            run_id="run_002",
            step=2,
            queries=3,
            success=False,
            score=0.10,
        ),
    ]

    assert mean_longest_plateau(steps) == 1.5
