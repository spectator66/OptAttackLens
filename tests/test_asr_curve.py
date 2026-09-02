from optattacklens.schema import AttackStep
from optattacklens.visualization.asr_curve import (
    calculate_asr_curve,
    save_asr_curve,
)


def test_calculate_asr_curve():
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
            success=False,
        ),
    ]

    values = calculate_asr_curve(
        steps,
        budgets=[1, 5, 10],
    )

    assert values == [
        0.0,
        1 / 3,
        2 / 3,
    ]


def test_save_asr_curve(tmp_path):
    steps = [
        AttackStep(
            run_id="run_001",
            step=0,
            queries=3,
            success=True,
        )
    ]

    output_path = tmp_path / "curve.png"

    save_asr_curve(
        steps,
        output_path,
    )

    assert output_path.exists()
