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


def _validate_single_run(steps: list[AttackStep]) -> None:
    """Ensure that all steps belong to the same attack run."""

    run_ids = {step.run_id for step in steps}

    if len(run_ids) > 1:
        raise ValueError("steps must belong to a single run")


def extract_score_progression(
    steps: list[AttackStep],
) -> list[tuple[int, float]]:
    """Extract (step, score) pairs from a single attack run."""

    _validate_single_run(steps)

    progression: list[tuple[int, float]] = []

    for step in steps:
        if step.score is None:
            continue

        progression.append((step.step, step.score))

    progression.sort(key=lambda item: item[0])

    return progression


def initial_score(
    steps: list[AttackStep],
) -> float | None:
    """Return the first available score in a trajectory."""

    progression = extract_score_progression(steps)

    if not progression:
        return None

    return progression[0][1]


def final_score(
    steps: list[AttackStep],
) -> float | None:
    """Return the last available score in a trajectory."""

    progression = extract_score_progression(steps)

    if not progression:
        return None

    return progression[-1][1]


def best_score(
    steps: list[AttackStep],
) -> float | None:
    """Return the highest score reached in a trajectory."""

    progression = extract_score_progression(steps)

    if not progression:
        return None

    return max(score for _, score in progression)


def time_to_best(
    steps: list[AttackStep],
) -> int | None:
    """Return the first step at which the best score is reached."""

    progression = extract_score_progression(steps)

    if not progression:
        return None

    best = max(score for _, score in progression)

    for step, score in progression:
        if score == best:
            return step

    return None


def longest_plateau(
    steps: list[AttackStep],
) -> int:
    """Return the longest number of consecutive steps without a new best score."""

    progression = extract_score_progression(steps)

    if not progression:
        return 0

    best_so_far = progression[0][1]
    current_plateau = 0
    longest = 0

    for _, score in progression[1:]:
        if score > best_so_far:
            best_so_far = score
            current_plateau = 0
        else:
            current_plateau += 1
            longest = max(longest, current_plateau)

    return longest


def total_improvement(
    steps: list[AttackStep],
) -> float | None:
    """Return the difference between final and initial score."""

    start = initial_score(steps)
    end = final_score(steps)

    if start is None or end is None:
        return None

    return end - start
