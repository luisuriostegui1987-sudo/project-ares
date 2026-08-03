---
id: ARES-ROADMAP-MASTER
title: PROJECT ARES — MASTER ROADMAP (OFFICIAL)
status: Official — normative North Star (recorded via Draft PR #6; merge pending Luis's authorization)
version: 1.0.0
owner: Luis
governance: change only via pull request; merge only with Luis's authorization
---

# PROJECT ARES — MASTER ROADMAP (OFFICIAL)

This document is the **normative North Star and principal sequencing
authority** for Project ARES. Every plan, sprint and priority derives from
it. Deviations require an explicit roadmap amendment authorized by Luis —
see the CTO directive in §10.

## 1. Mission

Build ARES: an AI-native investment **research** operating system that
accumulates institutional knowledge with full provenance, so that Luis makes
every capital decision with the best defensible evidence available. ARES is
not a trading bot; v1 remains paper-only.

## 2. Non-negotiable principles

1. **No AI moves capital.** Any capital action requires Luis's explicit
   decision.
2. **No number from memory.** Every fact is sourced, dated and graded.
3. **Every thesis carries a steel-manned bear case and an invalidation.**
4. **Risk limits, scores and signals are deterministic code — never LLM
   judgment.**
5. **RULE 17 epistemics everywhere**; Unknown is a valid answer; opinion is
   never laundered into fact.
6. **Honest edge only** — process, neglect and synthesis speed; never claimed
   informational advantage.
7. **Append-only memory** — facts, reports and knowledge are never silently
   rewritten.

## 3. Completed Sprints 1–5

| Sprint | Delivered | Release |
|---|---|---|
| 1 | Research pipeline vertical slice (`ares analyze NVDA`) | — |
| 2 | Real SEC EDGAR ingestion; InstitutionalFact (ARES-FACT-001 subset); institutional comparability | v0.2.0 |
| 3 | Persistent PostgreSQL Fact store; point-in-time reconstruction; restatements; concurrency-safe migrations | v0.3.0 |
| 4 | Institutional FastAPI, ResearchService, append-only report persistence, web console, safe DOM/XSS hardening | v0.4.0 |
| 5 | Render production deployment (Blueprint, pre-deploy migrations, Basic Auth, DB health probe) | **v0.4.0 LIVE on Render** — PostgreSQL connected and healthy; production health check passing |

## 4. Current priority

**The Knowledge Library approval pipeline (Phases 1–4 below).** Nothing else
may interrupt it.

### Current state (accurate as of this revision)

- Phase 1 — Knowledge Library: **materialized and published** (Draft PR #6).
- Phase 2 — CTO Knowledge Library review: **APPROVED FOR CRO REVIEW**, with
  one condition: Luis performs a complete reading of ARES-KNOWLEDGE-001 and
  ARES-ANALYST-001 before the final merge.
- CRO methodology review: **in progress**.
- Luis reading of the two core specifications and approval: **pending**.
- Merge: **blocked**.
- Investor research: **blocked**.

## 5. Phases 1–10

| # | Phase | Exit criterion | Status |
|---|---|---|---|
| 1 | Knowledge Library materialization | Structure, specs, templates published in a Draft PR | ✅ done |
| 2 | CTO Knowledge Library review | CTO approves architecture | ✅ approved for CRO review |
| 3 | CRO methodology review | CRO approves methodology | 🔄 in review |
| 4 | Luis authorization & merge | Knowledge Library on `main` | ⛔ blocked |
| 5 | Analyst Roadmap completion | §6 completed and approved | ⏳ pending |
| 6 | Plug-in Analyst Framework | Framework implemented and validated (§7) | ⏳ pending |
| 7 | First Institutional Analyst | Candidate researched under full methodology; CTO implementation, CRO validation, Quant validation all pass (§8) | ⏳ pending |
| 8 | Production Analyst | First analyst active in production research | ⏳ pending |
| 9 | Analyst Council | Several independently validated analysts operating as a council (§9) | ⏳ pending |
| 10 | Autonomous agents 24/7 | Agents operate continuously ONLY after the Council is mature (§9) | ⏳ pending |

ARES OS and its applications (web, iPhone, Android, synchronization, AI
conversational interface, dashboards) follow their documented dependencies in
this directory's per-item documents and never precede the phases they depend
on.

## 6. Analyst Roadmap

1. Candidate selection — **Benjamin Cowen is only a CANDIDATE** until every
   gate in ARES-ANALYST-001 §1 passes and Luis authorizes him by name.
   Chris Camillo, Peter Lynch and Terry Smith are subsequent candidates.
2. Source inventory → claim extraction → fact verification → principle
   synthesis → decision-rule formalization → contradiction ledger →
   validation (per ARES-ANALYST-001 phases).
3. Each analyst's knowledge base lives in `docs/analysts/<name>/` using the
   ten templates; no shortcuts, no invented content.

## 7. Plug-in Analyst Framework

Before any analyst is researched, ARES implements the framework that makes
analysts pluggable: a uniform contract for loading an analyst's principles
and decision rules into the research pipeline, so adding analyst N+1 is
configuration plus documented knowledge — never new architecture.

## 8. First Institutional Analyst — validation chain

- **CTO implementation**: the analyst's deterministic rules implemented in
  code behind the plug-in contract, reviewed for architecture.
- **CRO validation**: methodology audit — provenance, grades, RULE 17
  compliance, contradiction handling.
- **Quant validation**: deterministic rules backchecked against historical
  point-in-time data (no lookahead) before any production use.
- Only after all three: promotion to **Production Analyst** (Phase 8).

## 9. Analyst Council and autonomous agents

- The **Analyst Council** matures only when SEVERAL validated production
  analysts exist; a council of one is not a council.
- **Autonomous agents working 24/7** (continuous research, monitoring and
  report generation) begin ONLY after the Council is mature — never before.
- Agents inherit every principle in §2 unchanged; autonomy never extends to
  capital.

## 10. Permanent rules

### Permanent continuous-improvement principle

Improvement is a standing principle, not a phase: every phase ends with
review gates; every gap becomes a recorded item; methodology and code follow
the Draft → Reviewed → Active → Superseded lifecycle. Nothing is finished —
only currently unimproved.

### Permanent development sequence

Branch → Draft/PR → CTO architecture review → CRO methodology review →
**Luis authorizes merge**. No direct pushes to `main`, ever.

### CTO directive against roadmap deviations

New ideas, extras and opportunistic scope belong in the appropriate future
phase or the backlog. **They cannot interrupt the current milestone.**
Deviating from this roadmap's sequence requires an explicit amendment to this
document, reviewed by CTO and CRO and authorized by Luis, before any work
begins.
