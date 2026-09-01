from optattacklens.schema import AttackStep
from optattacklens.trajectory import (
    extract_score_progression,
    group_by_run,
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

