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
def extract_score_progression(
    steps: list[AttackStep],
) -> list[tuple[int, float]]:
    """Extract (step, score) pairs from a single attack run."""

    progression: list[tuple[int, float]] = []

    for step in steps:
        if step.score is None:
            continue

        progression.append((step.step, step.score))

    progression.sort(key=lambda item: item[0])

    return progression