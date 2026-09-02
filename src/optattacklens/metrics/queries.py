from optattacklens.schema import AttackStep


def queries_to_success(
    steps: list[AttackStep],
) -> dict[str, int | None]:
    """Return the first successful query count for each run."""

    result: dict[str, int | None] = {}

    for step in steps:
        if step.run_id not in result:
            result[step.run_id] = None

        if step.success:
            current = result[step.run_id]

            if current is None or step.queries < current:
                result[step.run_id] = step.queries

    return result


def median_queries_to_success(
    steps: list[AttackStep],
) -> float | None:
    """Return the median query count among successful runs."""

    results = queries_to_success(steps)

    successful_queries = [
        queries for queries in results.values() if queries is not None
    ]

    if not successful_queries:
        return None

    successful_queries.sort()

    n = len(successful_queries)
    middle = n // 2

    if n % 2 == 1:
        return float(successful_queries[middle])

    return (successful_queries[middle - 1] + successful_queries[middle]) / 2
