from optattacklens.metrics.asr import calculate_asr, calculate_asr_at_k
from optattacklens.schema import AttackStep
import pytest

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

def test_calculate_asr_at_k():
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

    assert calculate_asr_at_k(steps, 5) == 0.25
    assert calculate_asr_at_k(steps, 10) == 0.5
    assert calculate_asr_at_k(steps, 20) == 0.75
    
def test_calculate_asr_at_k_rejects_negative_budget():
    steps = []

    with pytest.raises(ValueError):
        calculate_asr_at_k(steps, -1)