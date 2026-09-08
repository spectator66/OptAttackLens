from dataclasses import dataclass


@dataclass
class AttackStep:
    """A single step in an optimization-based attack trajectory."""

    run_id: str
    step: int
    queries: int
    success: bool

    score: float | None = None
    prompt_tokens: int | None = None
    completion_tokens: int | None = None
    candidate: str | None = None
