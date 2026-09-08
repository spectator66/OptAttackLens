import json
from pathlib import Path

from optattacklens.schema import AttackStep


def load_trace(path: str | Path) -> list[AttackStep]:
    """Load an attack trace from a JSONL file."""

    trace_path = Path(path)
    steps: list[AttackStep] = []

    with trace_path.open("r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()

            if not line:
                continue

            data = json.loads(line)

            step = AttackStep(
                run_id=data["run_id"],
                step=data["step"],
                queries=data["queries"],
                success=data["success"],
                score=data.get("score"),
                prompt_tokens=data.get("prompt_tokens"),
                completion_tokens=data.get("completion_tokens"),
                candidate=data.get("candidate"),
            )

            steps.append(step)

    return steps
