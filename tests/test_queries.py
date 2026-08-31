from optattacklens.metrics.queries import (
    median_queries_to_success,
    queries_to_success,
)
from optattacklens.schema import AttackStep


def test_queries_to_success():
    steps = [
        AttackStep(
            run_id="run_001",
            step=0,
            queries=1,
            success=False,
        ),
        AttackStep(
            run_id="run_001",
            step=1,
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
            run_id="run_002",
            step=1,
            queries=2,
            success=False,
        ),
    ]

    result = queries_to_success(steps)

    assert result["run_001"] == 3
    assert result["run_002"] is None

def test_queries_to_success_uses_earliest_success():
    steps = [
        AttackStep(
            run_id="run_001",
            step=2,
            queries=7,
            success=True,
        ),
        AttackStep(
            run_id="run_001",
            step=1,
            queries=3,
            success=True,
        ),
    ]

    result = queries_to_success(steps)

    assert result["run_001"] == 3
def test_median_queries_to_success():
    steps = [
        AttackStep(
            run_id="a",
            step=0,
            queries=2,
            success=True,
        ),
        AttackStep(
            run_id="b",
            step=0,
            queries=6,
            success=True,
        ),
        AttackStep(
            run_id="c",
            step=0,
            queries=10,
            success=True,
        ),
    ]

    assert median_queries_to_success(steps) == 6.0
def test_median_queries_to_success_no_success():
    steps = [
        AttackStep(
            run_id="a",
            step=0,
            queries=1,
            success=False,
        ),
    ]

    assert median_queries_to_success(steps) is None