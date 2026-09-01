from optattacklens.schema import AttackStep


def group_by_run(
    steps: list[AttackStep],
) -> dict[str, list[AttackStep]]:
    """Group attack steps by run ID."""

    grouped: dict[str, list[AttackStep]] = {}

    for step in steps:
        if step.run_id not in grouped:
            grouped[step.run_id] = []

        grouped[step.run_id].append(step)

    for run_steps in grouped.values():
        run_steps.sort(key=lambda item: item.step)

    return grouped