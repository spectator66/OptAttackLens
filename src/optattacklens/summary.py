from optattacklens.metrics.asr import calculate_asr, calculate_asr_at_k
from optattacklens.metrics.queries import median_queries_to_success
from optattacklens.schema import AttackStep
from optattacklens.trajectory import (
    group_by_run,
    longest_plateau,
    time_to_best,
)


def mean_time_to_best(
    steps: list[AttackStep],
) -> float | None:
    """Return the mean time-to-best across runs with available scores."""

    grouped = group_by_run(steps)
    values: list[int] = []

    for run_steps in grouped.values():
        value = time_to_best(run_steps)

        if value is not None:
            values.append(value)

    if not values:
        return None

    return sum(values) / len(values)


def mean_longest_plateau(
    steps: list[AttackStep],
) -> float | None:
    """Return the mean longest plateau across runs with available scores."""

    grouped = group_by_run(steps)
    values: list[int] = []

    for run_steps in grouped.values():
        has_score = any(step.score is not None for step in run_steps)

        if not has_score:
            continue

        values.append(longest_plateau(run_steps))

    if not values:
        return None

    return sum(values) / len(values)


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
        "mean_time_to_best": mean_time_to_best(steps),
        "mean_longest_plateau": mean_longest_plateau(steps),
    }

    for budget in budgets:
        summary[f"asr_at_{budget}"] = calculate_asr_at_k(
            steps,
            budget,
        )

    return summary
