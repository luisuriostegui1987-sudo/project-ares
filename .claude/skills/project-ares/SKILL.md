---
name: project-ares
description: >
  Conventions and governance for Project ARES, an AI-native investment RESEARCH
  system (not a trading bot; paper-only). Use this whenever producing ARES
  research (a Research Note or investment thesis), scoring/ranking an asset, or
  writing/reviewing code in the ares-core repository. It enforces the ARES
  golden rules (human-only capital decisions, sourced facts, mandatory bear
  case, deterministic risk, RULE 17 knowledge classification).
---

# Project ARES — working conventions

ARES is an AI-native investment **research** system. It is **not** a trading bot.
v1 is **paper-only**. A human (Luis) makes every capital decision.

## Golden rules (never violate)
1. **No AI moves capital.** Any capital action needs explicit human approval.
2. **No number from memory.** Every fact is sourced + dated (a `Fact` object).
   If a required number is missing, output `MISSING: <fact>` — never invent it.
3. **Every thesis has a mandatory, steel-manned bear case + an invalidation.**
4. **Risk limits and scores are deterministic** (code/rubric), never LLM judgment.
5. **RULE 17 — classify every claim** as exactly one of: Verified Fact ·
   High Confidence · Reasonable Inference · Speculation · Opinion · Unknown.
   "Unknown" is a valid, respected answer. Never launder opinion into fact.
6. **Honest edge.** ARES claims only defensible edges (process/behavioral,
   neglected corners, synthesis speed) — not informational edge. On an efficient,
   over-covered name, the correct output is "no edge — watchlist," not a forced thesis.

## Producing a Research Note / thesis
Follow `reference/research_note_template.md`. Every note answers: question ·
evidence we have (Fact objects + RULE 17 class) · evidence missing · assumptions ·
analysis (base rates first) · confidence (RULE 17 + 0-100) · what would invalidate ·
research next. A thesis then uses the Constitution Sec 8 schema (bull/base/bear,
catalysts, invalidation, scores). No bear case or invalidation ⇒ rejected.

## Engineering conventions (ares-core repo)
- Python 3.12 · Pydantic v2 · modern typing (`list[str]`, `X | None`).
- Definition of Done: `pytest -q && ruff check . && mypy ares` all green.
- Conventional Commits (`feat:`, `fix:`, `refactor:`, `test:`, `docs:`); small PRs;
  never push to `main`; ≥1 human approval to merge. Details in CONTRIBUTING.md.

## Source of truth
- **GitHub** = all code/tests/CI. **Google Drive** = governance (Constitution,
  ADRs in ARES-999, ARES-### specs). Architectural decisions are ADRs in Drive,
  not code comments. If it isn't in the Decision Log, it doesn't officially exist.
