"""ARES command-line interface.

Sprint-1 goal command:

    ares analyze NVDA

Runs the research pipeline end to end and prints the structured report.
"""

from __future__ import annotations

import argparse
import logging
import sys

from ares.pipeline import DataMode, ResearchPipeline, render_text


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="ares", description="Project ARES research CLI.")
    parser.add_argument("-v", "--verbose", action="store_true", help="Debug logging.")
    sub = parser.add_subparsers(dest="command", required=True)

    analyze = sub.add_parser("analyze", help="Run the research pipeline for one ticker.")
    analyze.add_argument("ticker", help="Ticker symbol, e.g. NVDA.")
    analyze.add_argument("--json", action="store_true", help="Print the full report as JSON.")
    analyze.add_argument("--out", metavar="FILE", help="Also write the JSON report to FILE.")
    analyze.add_argument(
        "--data-mode",
        choices=["mock", "live"],
        default="mock",
        help="mock: labeled sample data (default). live: real SEC EDGAR data; "
        "fails loudly on error, never falls back to mocks.",
    )

    serve = sub.add_parser("serve", help="Run the ARES institutional API (the single entry point).")
    serve.add_argument("--host", default="127.0.0.1")
    serve.add_argument("--port", type=int, default=8000)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(levelname)s %(name)s: %(message)s",
        stream=sys.stderr,
    )
    if args.command == "analyze":
        from ares.providers.edgar import EdgarError

        try:
            mode = DataMode(args.data_mode.upper())
            report = ResearchPipeline(data_mode=mode).run(args.ticker)
        except EdgarError as exc:
            print(f"error: live EDGAR retrieval failed — {exc}", file=sys.stderr)
            print("note: live mode never falls back to mock data.", file=sys.stderr)
            return 1
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
    if args.command == "serve":
        try:
            import uvicorn

            from ares.api import create_app
        except ImportError as exc:  # pragma: no cover - requires missing extra
            print(f"error: the API requires the 'api' extra ({exc}).", file=sys.stderr)
            print("install with: pip install 'ares-core[api]'", file=sys.stderr)
            return 1
        uvicorn.run(create_app(), host=args.host, port=args.port)
        return 0
    return 2  # pragma: no cover - argparse enforces the subcommand


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
