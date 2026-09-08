from optattacklens.metrics.queries import queries_to_success
from optattacklens.schema import AttackStep


def calculate_asr(steps: list[AttackStep]) -> float:
    """Calculate attack success rate across runs."""

    if not steps:
        return 0.0

    run_success: dict[str, bool] = {}

    for step in steps:
        if step.run_id not in run_success:
            run_success[step.run_id] = False

        if step.success:
            run_success[step.run_id] = True

    successful_runs = sum(run_success.values())
    total_runs = len(run_success)

    return successful_runs / total_runs


def calculate_asr_at_k(
    steps: list[AttackStep],
    k: int,
) -> float:
    """Calculate ASR under a query budget k."""

    if k < 0:
        raise ValueError("k must be non-negative")

    results = queries_to_success(steps)

    if not results:
        return 0.0

    successful_within_budget = sum(
        queries is not None and queries <= k for queries in results.values()
    )

    return successful_within_budget / len(results)
