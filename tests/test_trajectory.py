import pytest
from optattacklens.schema import AttackStep
from optattacklens.trajectory import (
    best_score,
    extract_score_progression,
    final_score,
    group_by_run,
    initial_score,
    total_improvement,
)


def test_group_by_run():
    steps = [
        AttackStep(
            run_id="run_001",
            step=2,
            queries=3,
            success=True,
        ),
        AttackStep(
            run_id="run_002",
            step=0,
            queries=1,
            success=False,
        ),
        AttackStep(
            run_id="run_001",
            step=0,
            queries=1,
            success=False,
        ),
        AttackStep(
            run_id="run_001",
            step=1,
            queries=2,
            success=False,
        ),
    ]

    grouped = group_by_run(steps)

    assert len(grouped) == 2

    assert len(grouped["run_001"]) == 3
    assert len(grouped["run_002"]) == 1

    assert grouped["run_001"][0].step == 0
    assert grouped["run_001"][1].step == 1
    assert grouped["run_001"][2].step == 2

def test_group_by_run_empty():
    assert group_by_run([]) == {}

def test_extract_score_progression():
    steps = [
        AttackStep(
            run_id="run_001",
            step=2,
            queries=3,
            success=False,
            score=0.55,
        ),
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
            score=None,
        ),
        AttackStep(
            run_id="run_001",
            step=3,
            queries=4,
            success=True,
            score=0.91,
        ),
    ]

    progression = extract_score_progression(steps)

    assert progression == [
        (0, 0.10),
        (2, 0.55),
        (3, 0.91),
    ]

def test_extract_score_progression_keeps_zero_score():
    steps = [
        AttackStep(
            run_id="run_001",
            step=0,
            queries=1,
            success=False,
            score=0.0,
        ),
    ]

    progression = extract_score_progression(steps)

    assert progression == [(0, 0.0)]

def test_extract_score_progression_rejects_multiple_runs():
    steps = [
        AttackStep(
            run_id="run_001",
            step=0,
            queries=1,
            success=False,
            score=0.10,
        ),
        AttackStep(
            run_id="run_002",
            step=1,
            queries=2,
            success=False,
            score=0.20,
        ),
    ]

    with pytest.raises(
        ValueError,
        match="steps must belong to a single run",
    ):
        extract_score_progression(steps)

def test_basic_trajectory_metrics():
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
            score=0.45,
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
            score=0.80,
        ),
    ]

    assert initial_score(steps) == 0.10
    assert final_score(steps) == 0.80
    assert best_score(steps) == 0.80
    assert total_improvement(steps) == pytest.approx(0.70)

def test_basic_trajectory_metrics_without_scores():
    steps = [
        AttackStep(
            run_id="run_001",
            step=0,
            queries=1,
            success=False,
            score=None,
        ),
    ]

    assert initial_score(steps) is None
    assert final_score(steps) is None
    assert best_score(steps) is None
    assert total_improvement(steps) is None

