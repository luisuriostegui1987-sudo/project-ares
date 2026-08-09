---
id: ARES-ROADMAP-MASTER
title: PROJECT ARES — MASTER ROADMAP (OFFICIAL)
status: Official — normative North Star (merged to main via PR #6 with Luis's authorization)
version: 1.2.0
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

## 3. Completed Sprints 1–6

| Sprint | Delivered | Release |
|---|---|---|
| 1 | Research pipeline vertical slice (`ares analyze NVDA`) | — |
| 2 | Real SEC EDGAR ingestion; InstitutionalFact (ARES-FACT-001 subset); institutional comparability | v0.2.0 |
| 3 | Persistent PostgreSQL Fact store; point-in-time reconstruction; restatements; concurrency-safe migrations | v0.3.0 |
| 4 | Institutional FastAPI, ResearchService, append-only report persistence, web console, safe DOM/XSS hardening | v0.4.0 |
| 5 | Render production deployment (Blueprint, pre-deploy migrations, Basic Auth, DB health probe) | **v0.4.0 LIVE on Render** — PostgreSQL connected and healthy; production health check passing |
| 6 | Knowledge Library (specs, templates, analyst structures, roadmap) + Institutional Analyst Framework architecture — documentation only, zero code changes. PR #6 merged as `a57fbc2`; PR #7 merged as `8b911ef` | — (ARES remains v0.4.0; **v0.5.0 reserved for Sprint 7**) |

## 4. Current priority

**Resolve Phase 5 (Analyst Roadmap completion — §6 completed and approved).**
Sprint 7 — the implementation of the Institutional Knowledge Package
Framework (Phase 6 below) — is the next sprint, but it has **not started**
and may not begin until Phase 5 is resolved or a roadmap-order amendment is
formally approved per §10. Nothing else may interrupt this sequence.

### Current state (accurate as of this revision)

- Sprints 1–6: **complete and closed**.
- PR #6 (Knowledge Library) — **merged** to `main` as `a57fbc2`.
- PR #7 (Institutional Analyst Framework architecture) — **merged** to `main`
  as `8b911ef`.
- CTO review: **PASS** · CRO review: **PASS** · Luis authorization:
  **COMPLETE**.
- ARES remains **v0.4.0**; **v0.5.0 is reserved** for the executable
  Institutional Knowledge Package Framework delivered by Sprint 7. Sprint 7:
  **not started** — it may not begin until Phase 5 (Analyst Roadmap
  completion) is resolved or a roadmap-order amendment is formally approved
  per §10.
- The Institutional Knowledge Package architecture
  (ARES-ARCHITECTURE-ANALYST-FRAMEWORK-001) is **approved and must not be
  redesigned**. The Institutional Analyst Operating Contract
  (ARES-ANALYST-FRAMEWORK-001) remains a Preserved Verbatim Institutional
  Document with status **Research Draft — Pending Institutional Review**; its
  formal activation is a further gate before framework execution becomes
  effective.
- Investor research: **prohibited** until the executable framework exists and
  Luis explicitly authorizes the selected investor by name. Benjamin Cowen
  remains only the planned **first candidate** after framework completion and
  explicit authorization.

## 5. Phases 1–10

| # | Phase | Exit criterion | Status |
|---|---|---|---|
| 1 | Knowledge Library materialization | Structure, specs, templates published in a Draft PR | ✅ done |
| 2 | CTO Knowledge Library review | CTO approves architecture | ✅ done — CTO PASS |
| 3 | CRO methodology review | CRO approves methodology | ✅ done — CRO PASS |
| 4 | Luis authorization & merge | Knowledge Library on `main` | ✅ done — merged (PR #6 `a57fbc2`, PR #7 `8b911ef`) |
| 5 | Analyst Roadmap completion | §6 completed and approved | ✅ done — [ARES-ANALYST-ROADMAP-001.md](ARES-ANALYST-ROADMAP-001.md) completed; CTO reviewed and CRO reviewed (final reviews preserved in `docs/governance/phase-5/`); explicitly approved by Luis; closure materialized through the Phase 5 closure PR. Approval authorizes no research, no Sprint 7 start and no framework activation |
| 6 | Plug-in Analyst Framework | Framework implemented and validated (§7) | ⏳ pending — Sprint 7 scope (architecture approved and merged; implementation **not started**; v0.5.0 reserved; gated on Phase 5 resolution or a formally approved roadmap-order amendment per §10) |
| 7 | First Institutional Analyst | Candidate researched under full methodology; CTO implementation, CRO validation, Quant validation all pass (§8) | ⏳ pending |
| 8 | Production Analyst | First analyst active in production research | ⏳ pending |
| 9 | Analyst Council | Several independently validated analysts operating as a council (§9) | ⏳ pending |
| 10 | Autonomous agents 24/7 | Agents operate continuously ONLY after the Council is mature (§9) | ⏳ pending |

ARES OS and its applications (web, iPhone, Android, synchronization, AI
conversational interface, dashboards) follow their documented dependencies in
this directory's per-item documents and never precede the phases they depend
on.

## 6. Analyst Roadmap

> The detailed institutional Analyst Roadmap (15 controlled slots, cohorts,
> lifecycle, authority matrix) is designed in
> [ARES-ANALYST-ROADMAP-001.md](ARES-ANALYST-ROADMAP-001.md) — **Draft**;
> Phase 5 remains pending until it is reviewed, approved by Luis and merged.
> Its approval never authorizes research on any candidate.

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
