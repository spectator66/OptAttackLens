from pathlib import Path

import matplotlib.pyplot as plt

from optattacklens.metrics.asr import calculate_asr_at_k
from optattacklens.schema import AttackStep


def calculate_asr_curve(
    steps: list[AttackStep],
    budgets: list[int],
) -> list[float]:
    """Calculate ASR values across query budgets."""

    return [
        calculate_asr_at_k(steps, budget)
        for budget in budgets
    ]


def save_asr_curve(
    steps: list[AttackStep],
    path: str | Path,
    budgets: list[int] | None = None,
) -> None:
    """Save an ASR-vs-query-budget curve."""

    if budgets is None:
        budgets = [1, 5, 10, 20, 50]

    asr_values = calculate_asr_curve(
        steps,
        budgets,
    )

    fig, ax = plt.subplots()

    ax.plot(
        budgets,
        asr_values,
        marker="o",
    )

    ax.set_xlabel("Query Budget")
    ax.set_ylabel("Attack Success Rate")
    ax.set_title("ASR vs Query Budget")

    ax.set_ylim(0.0, 1.0)

    fig.tight_layout()

    output_path = Path(path)

    fig.savefig(
        output_path,
        dpi=150,
    )

    plt.close(fig)