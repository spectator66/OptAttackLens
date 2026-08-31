from optattacklens.metrics.asr import calculate_asr
from optattacklens.schema import AttackStep


def test_calculate_asr():
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
            queries=2,
            success=True,
        ),
        AttackStep(
            run_id="run_002",
            step=0,
            queries=1,
            success=False,
        ),
    ]

    assert calculate_asr(steps) == 0.5


def test_calculate_asr_empty():
    assert calculate_asr([]) == 0.0