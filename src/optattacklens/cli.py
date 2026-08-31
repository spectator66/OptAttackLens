import argparse

from optattacklens.loader import load_trace
from optattacklens.summary import summarize_trace


def main() -> None:
    """Entry point for the OptAttackLens command-line interface."""

    parser = argparse.ArgumentParser(
        prog="optattacklens",
        description="Analyze optimization-based LLM attack traces.",
    )

    subparsers = parser.add_subparsers(dest="command")

    analyze_parser = subparsers.add_parser(
        "analyze",
        help="Analyze an attack trace.",
    )

    analyze_parser.add_argument(
        "path",
        help="Path to a JSONL attack trace.",
    )

    args = parser.parse_args()

    if args.command == "analyze":
        steps = load_trace(args.path)
        summary = summarize_trace(steps)

        print("OptAttackLens Summary")
        print()
        print(f"ASR:                       {summary['asr']:.1%}")

        median = summary["median_queries_to_success"]

        if median is None:
            print("Median Queries-to-Success: N/A")
        else:
            print(f"Median Queries-to-Success: {median:g}")

        print(f"ASR@5:                     {summary['asr_at_5']:.1%}")
        print(f"ASR@10:                    {summary['asr_at_10']:.1%}")
        print(f"ASR@20:                    {summary['asr_at_20']:.1%}")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()