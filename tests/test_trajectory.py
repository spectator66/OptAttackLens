import pytest
from optattacklens.schema import AttackStep
from optattacklens.trajectory import (
    best_score,
    extract_score_progression,
    final_score,
    group_by_run,
    initial_score,
    time_to_best,
    total_improvement,
    longest_plateau,
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

def test_time_to_best_returns_first_best_step():
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
            score=0.90,
        ),
        AttackStep(
            run_id="run_001",
            step=2,
            queries=3,
            success=False,
            score=0.60,
        ),
        AttackStep(
            run_id="run_001",
            step=3,
            queries=4,
            success=True,
            score=0.90,
        ),
    ]

    assert time_to_best(steps) == 1

def test_longest_plateau():
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
            score=0.40,
        ),
        AttackStep(
            run_id="run_001",
            step=3,
            queries=4,
            success=False,
            score=0.35,
        ),
        AttackStep(
            run_id="run_001",
            step=4,
            queries=5,
            success=True,
            score=0.41,
        ),
    ]

    assert longest_plateau(steps) == 2

def test_longest_plateau_with_continuous_improvement():
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
            score=0.20,
        ),
        AttackStep(
            run_id="run_001",
            step=2,
            queries=3,
            success=True,
            score=0.30,
        ),
    ]

    assert longest_plateau(steps) == 0


def test_longest_plateau_without_scores():
    steps = [
        AttackStep(
            run_id="run_001",
            step=0,
            queries=1,
            success=False,
            score=None,
        ),
    ]

    assert longest_plateau(steps) == 0

    