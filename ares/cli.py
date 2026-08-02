"""ARES command-line interface.

Sprint-1 goal command:

    ares analyze NVDA

Runs the research pipeline end to end and prints the structured report.
"""
from __future__ import annotations

import argparse
import logging
import sys

from ares.pipeline import ResearchPipeline, render_text


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="ares", description="Project ARES research CLI.")
    parser.add_argument("-v", "--verbose", action="store_true", help="Debug logging.")
    sub = parser.add_subparsers(dest="command", required=True)

    analyze = sub.add_parser("analyze", help="Run the research pipeline for one ticker.")
    analyze.add_argument("ticker", help="Ticker symbol, e.g. NVDA.")
    analyze.add_argument("--json", action="store_true", help="Print the full report as JSON.")
    analyze.add_argument("--out", metavar="FILE", help="Also write the JSON report to FILE.")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(levelname)s %(name)s: %(message)s",
        stream=sys.stderr,
    )
    if args.command == "analyze":
        try:
            report = ResearchPipeline().run(args.ticker)
        except (LookupError, ValueError) as exc:
            print(f"error: {exc}", file=sys.stderr)
            return 1
        payload = report.model_dump_json(indent=2)
        if args.out:
            with open(args.out, "w", encoding="utf-8") as fh:
                fh.write(payload + "\n")
            print(f"report written to {args.out}", file=sys.stderr)
        print(payload if args.json else render_text(report))
        return 0
    return 2  # pragma: no cover - argparse enforces the subcommand


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
