# CLAUDE.md — Working agreement for AI agents in this repo

> Read this first. It tells any AI (Claude Code, GitHub Action, or chat) how to
> work on Project ARES. The highest-ROI file in the repo — keep it accurate.

## What ARES is
An AI-native investment **research** system. **Not** a trading bot. Paper-only in
v1. A human (Luis) makes every capital decision.

## Source of truth
- **GitHub (this repo) is the single institutional source of truth** — code,
  tests, CI, governance, architecture, specifications, institutional research
  and project history.
- **`docs/` is the canonical Knowledge Library** (specifications, templates,
  analyst knowledge bases, architecture, roadmap).
- External files, chats and Google Drive documents are **non-canonical** until
  reviewed and merged into this repository via pull request.
- Institutional decisions must be preserved in repository documentation.
- No agent may treat chat history as more authoritative than `main`.

## Golden rules (from the Constitution — never violate)
1. No AI moves capital. Any capital action requires explicit human approval.
2. No number from memory. Every fact is sourced + dated (a `Fact` object).
3. Every thesis has a mandatory, steel-manned bear case + an invalidation.
4. Risk limits and scores are deterministic code, never LLM judgment.
5. Classify knowledge (RULE 17): Verified Fact / High Confidence / Reasonable
   Inference / Speculation / Opinion / Unknown. Never launder opinion into fact.

## Stack
Python 3.12 · Pydantic v2 · pytest · ruff · mypy. Modern typing (`list[str]`, `X | None`).

## Commands
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
pytest -q          # all tests must pass
ruff check .       # lint must be clean
mypy ares          # types must be clean
```

## Where things live
- `ares/models/` — domain models (Fact, Event, Signal, Evidence, Thesis, Decision, RiskResult).
- `tests/` — pytest suite (governance validators, invalid-input, serialization).
- `docs/` — canonical Knowledge Library (specifications, templates, analyst
  knowledge bases, architecture, roadmap).

## How to contribute (short form; full detail in CONTRIBUTING.md)
- Branch from `main`; small, focused changes.
- Conventional Commits (`feat:`, `fix:`, `refactor:`, `test:`, `docs:`).
- Open a PR; CI (pytest+ruff+mypy) must be green; **≥1 human approval** to merge.
- Never push directly to `main`. Never commit secrets.

## Decisions
Architectural/strategic decisions are **repository documentation** (`docs/` and
PR history), reviewed and merged via pull request — not code comments and not
chat. If a code change embodies a decision, reference the governing repository
document in the PR description. Rule: *if it isn't preserved in the repository,
it doesn't officially exist.*
