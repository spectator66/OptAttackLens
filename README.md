# OptAttackLens 🔍

A lightweight toolkit for profiling and analyzing optimization-based LLM attacks.

OptAttackLens focuses on a question that final attack success rate alone cannot answer:

> **How efficiently does an optimization-based attack reach success?**

Instead of looking only at final ASR, OptAttackLens analyzes query-budget efficiency and attack trajectories.

---

## Features

Current features include:

- Attack Success Rate (ASR)
- ASR under query budgets (ASR@k)
- Queries-to-Success
- Median Queries-to-Success
- JSONL trace loading
- JSON and CSV summary export
- ASR-vs-query-budget visualization
- Command-line interface
- Automated tests with GitHub Actions

---

## Installation

Clone the repository:

```bash
git clone https://github.com/spectator66/OptAttackLens.git
cd OptAttackLens
```

Install the project in editable mode:

```bash
pip install -e .
```

---

## Quick Start

Analyze the included demo trace:

```bash
optattacklens analyze examples/demo_trace.jsonl
```

Example output:

```text
OptAttackLens Summary

ASR:                       80.0%
Median Queries-to-Success: 13
ASR@5:                     20.0%
ASR@10:                    40.0%
ASR@20:                    60.0%
```

---

## Export Results

Save the summary as JSON:

```bash
optattacklens analyze examples/demo_trace.jsonl --json outputs/summary.json
```

Save the summary as CSV:

```bash
optattacklens analyze examples/demo_trace.jsonl --csv outputs/summary.csv
```

Generate an ASR-vs-query-budget curve:

```bash
optattacklens analyze examples/demo_trace.jsonl --plot outputs/asr_curve.png
```

Generate all outputs at once:

```bash
optattacklens analyze examples/demo_trace.jsonl --json outputs/summary.json --csv outputs/summary.csv --plot outputs/asr_curve.png
```

---

## Trace Format

OptAttackLens uses JSONL, where each line represents one optimization step.

Example:

```json
{"run_id":"run_001","step":0,"queries":1,"success":false,"score":0.10}
{"run_id":"run_001","step":1,"queries":2,"success":false,"score":0.30}
{"run_id":"run_001","step":2,"queries":3,"success":true,"score":0.92}
```

Core fields:

| Field | Type | Description |
|---|---|---|
| `run_id` | string | Identifier of an attack run |
| `step` | integer | Optimization step index |
| `queries` | integer | Number of queries used |
| `success` | boolean | Whether the attack succeeded |
| `score` | float or null | Optional optimization score |
| `prompt_tokens` | integer or null | Optional prompt token count |
| `completion_tokens` | integer or null | Optional completion token count |
| `candidate` | string or null | Optional attack candidate |

---

## Metrics

### Attack Success Rate

ASR measures the fraction of attack runs that eventually succeed.

### Queries-to-Success

Queries-to-Success records the earliest query count at which each attack run succeeds.

### Median Queries-to-Success

This summarizes the typical query cost among successful attack runs.

### ASR@k

ASR@k measures attack success rate under a fixed query budget `k`.

For example:

```text
ASR@5  = 20%
ASR@10 = 40%
ASR@20 = 60%
```

This helps distinguish attacks that achieve similar final ASR but require very different amounts of search.

---

## Project Structure

```text
OptAttackLens/
├── src/
│   └── optattacklens/
│       ├── cli.py
│       ├── export.py
│       ├── loader.py
│       ├── schema.py
│       ├── summary.py
│       ├── metrics/
│       │   ├── asr.py
│       │   └── queries.py
│       └── visualization/
│           └── asr_curve.py
├── tests/
├── examples/
├── outputs/
├── .github/
│   └── workflows/
│       └── tests.yml
├── pyproject.toml
└── README.md
```

---

## Development

Run tests:

```bash
pytest
```

GitHub Actions automatically runs the test suite on pushes and pull requests.

---

## Roadmap

### v0.1

- Standard attack trace schema
- JSONL loader
- ASR
- ASR@k
- Queries-to-Success
- Summary export
- ASR query-budget visualization
- CLI
- Automated tests

### Future

- Optimization trajectory visualization
- Plateau detection
- Candidate diversity metrics
- Stability analysis
- Framework adapters
- HTML reports

---

## Status

🚧 Early development.

The API and trace schema may change before the first stable release.

---

## License

MIT