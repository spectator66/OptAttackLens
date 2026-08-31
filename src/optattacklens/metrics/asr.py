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