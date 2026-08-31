from optattacklens.schema import AttackStep


def test_attack_step_creation():
    step = AttackStep(
        run_id="run_001",
        step=0,
        queries=1,
        success=False,
    )

    assert step.run_id == "run_001"
    assert step.step == 0
    assert step.queries == 1
    assert step.success is False
    assert step.score is None
