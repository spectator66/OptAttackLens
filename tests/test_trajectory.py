from optattacklens.schema import AttackStep
from optattacklens.trajectory import group_by_run


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