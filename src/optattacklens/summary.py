from optattacklens.metrics.asr import calculate_asr, calculate_asr_at_k
from optattacklens.metrics.queries import median_queries_to_success
from optattacklens.schema import AttackStep


def summarize_trace(
    steps: list[AttackStep],
    budgets: list[int] | None = None,
) -> dict[str, float | None]:
    """Summarize key metrics for an attack trace."""

    if budgets is None:
        budgets = [5, 10, 20]

    summary: dict[str, float | None] = {
        "asr": calculate_asr(steps),
        "median_queries_to_success": median_queries_to_success(steps),
    }

    for budget in budgets:
        summary[f"asr_at_{budget}"] = calculate_asr_at_k(
            steps,
            budget,
        )

    return summary