---
id: ARES-ANALYST-ROADMAP-001
title: Institutional Analyst Roadmap — first cohort of 15 controlled slots
status: Draft — Phase 5 artifact; pending Publishing Engineer verification, CTO review, CRO review and Luis's approval
version: 0.1.0
owner: CKO
governance: change only via pull request; merge only with Luis's authorization; approval of this roadmap does NOT authorize research on any candidate
---

# ARES-ANALYST-ROADMAP-001 — Institutional Analyst Roadmap

This document is the Phase 5 artifact required by
[MASTER-ROADMAP.md §5](MASTER-ROADMAP.md) (Phase 5 — "Analyst Roadmap
completion: §6 completed and approved"). It defines the planned first cohort
of **15 controlled analyst slots**, their institutional sequence, the
selection criteria that will eventually govern candidate choice, the
candidate lifecycle, the authority matrix and the future deliverables each
candidate must produce **after** individual research authorization.

> **RESEARCH STATUS: BLOCKED.** This roadmap is design only. It contains no
> investor research, no methodology summaries and no performance claims.
> Approval of this roadmap is **not** authorization to research any
> candidate: per [ARES-ANALYST-001 §1](../specifications/ARES-ANALYST-001.md),
> research on a given analyst begins only after all eight gates pass,
> including the executable framework (Sprint 7, not started) and Luis's
> explicit, named, per-analyst authorization.

## 1. Canonical evidence inventory

All statements in this roadmap derive exclusively from the repository state
at `main` = `31b0db2ef5748501d6e395175f7e593e339cde9f` (merge of PR #8).
No chat history, external notes or internet research were used.

| Repository statement | Canonical file | Section | Effect on roadmap |
|---|---|---|---|
| Phase 5 = "Analyst Roadmap completion — §6 completed and approved"; status pending | [MASTER-ROADMAP.md](MASTER-ROADMAP.md) | §5 (phase table) | This document is the artifact that resolves Phase 5, subject to review and Luis's approval |
| "Benjamin Cowen is only a CANDIDATE until every gate in ARES-ANALYST-001 §1 passes and Luis authorizes him by name. Chris Camillo, Peter Lynch and Terry Smith are subsequent candidates." | [MASTER-ROADMAP.md](MASTER-ROADMAP.md) | §6.1 | Slots 1–4 carry canonical names; all remain candidates only |
| Research pipeline: source inventory → claims → facts → principles → decision rules → contradiction ledger → validation | [MASTER-ROADMAP.md](MASTER-ROADMAP.md) | §6.2 | Future per-candidate deliverables (§8 below) follow this pipeline |
| Each analyst's knowledge base lives in `docs/analysts/<name>/` using the ten templates | [MASTER-ROADMAP.md](MASTER-ROADMAP.md) | §6.3 | Slot activation eventually produces a knowledge base in that layout; structure-only until gate 8 |
| Sprint 7 (framework implementation) not started; v0.5.0 reserved; gated on Phase 5 resolution | [MASTER-ROADMAP.md](MASTER-ROADMAP.md) | §4 | Roadmap approval precedes Sprint 7; nothing here starts Sprint 7 |
| Eight-gate authorization chain; gate 6 = Analyst Roadmap completed and approved; gate 7 = framework implemented and validated; gate 8 = Luis authorizes the analyst by name | [ARES-ANALYST-001](../specifications/ARES-ANALYST-001.md) | §1 | Lifecycle (§6 below) and cohort entry gates are built on these gates; no state may bypass them |
| Analyst directories contain ONLY structural READMEs until gate 8; populating templates before gate 8 is a governance violation | [ARES-ANALYST-001](../specifications/ARES-ANALYST-001.md) | §1 | This roadmap adds no content to `docs/analysts/`; roster is documentation only |
| Four analyst directories exist, all "BLOCKED — not started": benjamin-cowen, chris-camillo, peter-lynch, terry-smith | [docs/analysts/README.md](../analysts/README.md) | table | Confirms the four canonical names and their blocked status |
| Roles: CKO defines methodology; publishing engineer materializes/publishes; CTO reviews architecture; CRO reviews methodology; Luis authorizes every merge and every research start and makes every capital decision | [research-governance.md](../specifications/research-governance.md) | Roles / Flow | Authority matrix (§7 below) preserves these boundaries verbatim |
| Analyst lifecycle: `CANDIDATE → AUTHORIZED (gate 8) → RESEARCHED → PACKAGED → CTO-IMPLEMENTATION-REVIEWED → CRO-VALIDATED → QUANT-VALIDATED → PRODUCTION → DEPRECATED`; nothing is ever deleted | [ARES-ARCHITECTURE-ANALYST-FRAMEWORK-001](../architecture/ARES-ARCHITECTURE-ANALYST-FRAMEWORK-001.md) | §3 | Roster lifecycle (§6 below) maps onto this approved lifecycle; the architecture is not redesigned |
| Only Luis can set APPROVED; the engine never advances workflow status; reviewer functions own their transitions | [ARES-ARCHITECTURE-ANALYST-FRAMEWORK-001](../architecture/ARES-ARCHITECTURE-ANALYST-FRAMEWORK-001.md) | §3.1 | Transition ownership in §6 mirrors this reserved workflow |
| Analyst = declarative Institutional Knowledge Package (IKP); framework consumes IKPs and nothing else; execution requires an issued AssignmentRef | [ARES-ARCHITECTURE-ANALYST-FRAMEWORK-001](../architecture/ARES-ARCHITECTURE-ANALYST-FRAMEWORK-001.md) | §§2, 4.1 | Future deliverables (§8) culminate in a versioned IKP; none is created now |
| Operating contract ARES-ANALYST-FRAMEWORK-001 is a Preserved Verbatim Institutional Document, "Research Draft — Pending Institutional Review"; activation is a separate gate | [MASTER-ROADMAP.md](MASTER-ROADMAP.md) · [ARES-ANALYST-FRAMEWORK-001](../specifications/ARES-ANALYST-FRAMEWORK-001.md) | §4 · header | This roadmap does not activate the contract; SHA-256 preserved (§10 below) |
| Deviating from the roadmap sequence requires a formal amendment reviewed by CTO and CRO and authorized by Luis | [MASTER-ROADMAP.md](MASTER-ROADMAP.md) | §10 | Changes to this roster or its sequence follow the same amendment rule |
| RULE 17 epistemics; no number from memory; opinion never laundered into fact | [MASTER-ROADMAP.md](MASTER-ROADMAP.md) · [ARES-ANALYST-001](../specifications/ARES-ANALYST-001.md) | §2 · §3 | This roadmap asserts NOTHING about any candidate's methodology; all such fields are deferred to authorized research |

## 2. Scope and non-scope

**In scope:** roster structure, sequencing, selection criteria, lifecycle,
authority boundaries, future deliverables, Phase 5 Definition of Done.

**Out of scope (prohibited here):** research into any investor's
methodology; summaries of books, interviews, videos or portfolios;
performance evaluation or ranking; creation or population of knowledge
packages; any implementation (models, registries, primitives, engine,
AssignmentRef); Sprint 7 work; activation of ARES-ANALYST-FRAMEWORK-001;
version changes; investment recommendations; capital decisions.

## 3. Candidate roster — 15 controlled slots

Provenance rule: a name appears below **only** if it appears in canonical
`main` (evidence table, §1). Exactly four names have canonical provenance
(MASTER-ROADMAP §6.1). The remaining eleven slots are numbered `TBD` slots
and must not be filled from memory, popularity or internet research —
only by a Luis-approved decision preserved in GitHub.

Field semantics: `analytical_category` and `portfolio_role` are recorded as
`TBD — deferred to authorized research` for every slot, including named
candidates, because canonical `main` does not document any candidate's
methodology and this roadmap may not invent facts (RULE 17). Sequence among
slots 2–4 follows the listing order of MASTER-ROADMAP §6.1 and is
re-confirmable by Luis at each authorization gate.

| # | candidate_name | candidate_status | selection_basis | analytical_category | portfolio_role | dependencies | authorization_required | research_status | IKP_status | implementation_status | activation_status |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Benjamin Cowen | PLANNED | Named first candidate in MASTER-ROADMAP §6.1 | TBD — deferred to authorized research | TBD — deferred to authorized research | Gates 1–7 of ARES-ANALYST-001 §1 (incl. Sprint 7 framework) | Luis, explicit and by name (gate 8) | BLOCKED | NOT_CREATED | NOT_STARTED | NOT_ACTIVE |
| 2 | Chris Camillo | PLANNED | Named subsequent candidate in MASTER-ROADMAP §6.1 | TBD — deferred to authorized research | TBD — deferred to authorized research | Gates 1–7 + Cohort A entry gate (§5) | Luis, explicit and by name (gate 8) | BLOCKED | NOT_CREATED | NOT_STARTED | NOT_ACTIVE |
| 3 | Peter Lynch | PLANNED | Named subsequent candidate in MASTER-ROADMAP §6.1 | TBD — deferred to authorized research | TBD — deferred to authorized research | Gates 1–7 + Cohort A entry gate (§5) | Luis, explicit and by name (gate 8) | BLOCKED | NOT_CREATED | NOT_STARTED | NOT_ACTIVE |
| 4 | Terry Smith | PLANNED | Named subsequent candidate in MASTER-ROADMAP §6.1 | TBD — deferred to authorized research | TBD — deferred to authorized research | Gates 1–7 + Cohort B entry gate (§5) | Luis, explicit and by name (gate 8) | BLOCKED | NOT_CREATED | NOT_STARTED | NOT_ACTIVE |
| 5 | TBD-05 | TBD | No canonical provenance; requires Luis-approved selection preserved in GitHub | TBD — deferred to authorized research | TBD — deferred to authorized research | Gates 1–7 + Cohort B entry gate + slot naming decision | Luis (naming) then Luis (gate 8) | BLOCKED | NOT_CREATED | NOT_STARTED | NOT_ACTIVE |
| 6 | TBD-06 | TBD | No canonical provenance; requires Luis-approved selection preserved in GitHub | TBD — deferred to authorized research | TBD — deferred to authorized research | Gates 1–7 + Cohort B entry gate + slot naming decision | Luis (naming) then Luis (gate 8) | BLOCKED | NOT_CREATED | NOT_STARTED | NOT_ACTIVE |
| 7 | TBD-07 | TBD | No canonical provenance; requires Luis-approved selection preserved in GitHub | TBD — deferred to authorized research | TBD — deferred to authorized research | Gates 1–7 + Cohort C entry gate + slot naming decision | Luis (naming) then Luis (gate 8) | BLOCKED | NOT_CREATED | NOT_STARTED | NOT_ACTIVE |
| 8 | TBD-08 | TBD | No canonical provenance; requires Luis-approved selection preserved in GitHub | TBD — deferred to authorized research | TBD — deferred to authorized research | Gates 1–7 + Cohort C entry gate + slot naming decision | Luis (naming) then Luis (gate 8) | BLOCKED | NOT_CREATED | NOT_STARTED | NOT_ACTIVE |
| 9 | TBD-09 | TBD | No canonical provenance; requires Luis-approved selection preserved in GitHub | TBD — deferred to authorized research | TBD — deferred to authorized research | Gates 1–7 + Cohort C entry gate + slot naming decision | Luis (naming) then Luis (gate 8) | BLOCKED | NOT_CREATED | NOT_STARTED | NOT_ACTIVE |
| 10 | TBD-10 | TBD | No canonical provenance; requires Luis-approved selection preserved in GitHub | TBD — deferred to authorized research | TBD — deferred to authorized research | Gates 1–7 + Cohort C entry gate + slot naming decision | Luis (naming) then Luis (gate 8) | BLOCKED | NOT_CREATED | NOT_STARTED | NOT_ACTIVE |
| 11 | TBD-11 | TBD | No canonical provenance; requires Luis-approved selection preserved in GitHub | TBD — deferred to authorized research | TBD — deferred to authorized research | Gates 1–7 + Cohort D entry gate + slot naming decision | Luis (naming) then Luis (gate 8) | BLOCKED | NOT_CREATED | NOT_STARTED | NOT_ACTIVE |
| 12 | TBD-12 | TBD | No canonical provenance; requires Luis-approved selection preserved in GitHub | TBD — deferred to authorized research | TBD — deferred to authorized research | Gates 1–7 + Cohort D entry gate + slot naming decision | Luis (naming) then Luis (gate 8) | BLOCKED | NOT_CREATED | NOT_STARTED | NOT_ACTIVE |
| 13 | TBD-13 | TBD | No canonical provenance; requires Luis-approved selection preserved in GitHub | TBD — deferred to authorized research | TBD — deferred to authorized research | Gates 1–7 + Cohort D entry gate + slot naming decision | Luis (naming) then Luis (gate 8) | BLOCKED | NOT_CREATED | NOT_STARTED | NOT_ACTIVE |
| 14 | TBD-14 | TBD | No canonical provenance; requires Luis-approved selection preserved in GitHub | TBD — deferred to authorized research | TBD — deferred to authorized research | Gates 1–7 + Cohort D entry gate + slot naming decision | Luis (naming) then Luis (gate 8) | BLOCKED | NOT_CREATED | NOT_STARTED | NOT_ACTIVE |
| 15 | TBD-15 | TBD | No canonical provenance; requires Luis-approved selection preserved in GitHub | TBD — deferred to authorized research | TBD — deferred to authorized research | Gates 1–7 + Cohort D entry gate + slot naming decision | Luis (naming) then Luis (gate 8) | BLOCKED | NOT_CREATED | NOT_STARTED | NOT_ACTIVE |

Allowed `candidate_status` values: `PLANNED`, `PROPOSED`, `TBD`,
`REJECTED`, `DEFERRED`. Status changes follow the lifecycle in §6 and the
amendment rule of MASTER-ROADMAP §10.

## 4. Selection architecture — criteria for future candidate choice

These criteria govern how future candidates are proposed and selected for
**research authorization consideration**. They are neutral: applying them
requires no knowledge of any individual's methodology, and satisfying them
validates suitability for institutional research — never investment
performance. Evidence for each criterion must be gathered only after the
candidate's research is authorized; at selection time the criteria are
applied as documented expectations, with unknowns recorded as Unknown
(RULE 17).

1. **Analytical diversity** — the candidate adds an analytical lens not
   already covered by approved roster members.
2. **Time-horizon diversity** — the roster must span short-, medium- and
   long-horizon frameworks; a candidate's expected horizon must be
   documentable from primary sources during research.
3. **Asset-class coverage** — the roster collectively covers the asset
   classes ARES researches; overlap is a recorded, justified choice.
4. **Perspective coverage** — across the cohort: fundamental, quantitative,
   technical, behavioral and macro perspectives are all represented over
   time.
5. **Evidence availability** — sufficient primary, attributable sources
   plausibly exist (books, filings, published interviews, own writings) to
   support Grade A/B evidence per the
   [source hierarchy](../specifications/source-hierarchy.md).
6. **Methodology documentability** — the candidate's process appears
   documentable as claims → facts → principles under
   [ARES-ANALYST-001](../specifications/ARES-ANALYST-001.md) §2.
7. **Rule testability** — at least part of the methodology is plausibly
   expressible as deterministic decision rules (no LLM judgment).
8. **Falsifiability** — the methodology admits invalidation conditions;
   unfalsifiable narratives are grounds for rejection.
9. **Historical point-in-time reproducibility** — rules can eventually be
   backchecked against point-in-time data without lookahead (Quant gate,
   MASTER-ROADMAP §8).
10. **Conflict and overlap management** — expected contradictions with
    existing roster members are manageable via the contradiction ledger,
    not suppressed.
11. **Licensing and intellectual-property risk** — research can proceed on
    lawfully accessible sources with acceptable IP exposure; paywalled or
    restricted corpora are flagged before authorization.
12. **Suitability for deterministic implementation** — the eventual IKP can
    satisfy the validator (rules cite principles; principles cite
    claims/facts; total, deterministic rubric).
13. **Independence from popularity** — follower counts, virality or
    social-media influence are never selection evidence.
14. **Marginal value** — documented, expected value added relative to
    analysts already approved; duplication requires explicit justification.

A candidate proposal must address every criterion, using Unknown where
evidence does not yet exist. The criteria select candidates for future
research; they do not validate investment performance.

## 5. Cohort sequencing

The 15 slots are organized into four controlled cohorts. Cohorts are
strictly sequential: a cohort's entry gate cannot open until the preceding
cohort's exit criteria are met. Within any cohort, **at most one candidate
may be in `RESEARCH_IN_PROGRESS` at a time** (maximum concurrent research
assignments = 1), and every candidate requires an individual gate-8
authorization from Luis. It is therefore structurally impossible for all 15
candidates to be researched simultaneously, and approval of this roadmap is
not blanket approval to research the roster.

| Cohort | Slots | Purpose | Entry gate | Required prior framework capability | Max concurrent research | Review chain | Exit criteria | Pause / rejection conditions | Dependency |
|---|---|---|---|---|---|---|---|---|---|
| A | 1–3 | Prove the full research→IKP→validation pipeline end-to-end on the first canonical candidates | Phase 5 approved **and** Sprint 7 framework implemented and validated (gates 6–7) **and** Luis gate-8 authorization per candidate | Executable IKP framework v0.5.0: loader, validator, AssignmentRef intake, deterministic engine | 1 | CKO → Publishing Engineer → CTO → CRO → Quant (when applicable) → Luis | ≥1 Cohort A candidate reaches APPROVED with full validation chain; lessons recorded as continuous-improvement items | Validator failures without remediation path; unresolvable evidence gaps; CRO methodology rejection; Luis pause order | Phases 5–6 complete |
| B | 4–6 | First controlled expansion; test roster processes on a candidate mix including newly named slots | Cohort A exit criteria met **and** any Cohort A process gaps remediated **and** Luis gate-8 authorization per candidate | Framework proven by ≥1 approved IKP in production-eligible state | 1 | Same as Cohort A | ≥2 cumulative candidates APPROVED; naming decisions for slots 5–6 preserved in GitHub | Same as Cohort A, plus: unfilled TBD slots simply remain TBD (never rushed) | Cohort A |
| C | 7–10 | Broaden analytical, horizon and asset-class coverage per §4 criteria | Cohort B exit criteria met **and** coverage-gap review recorded **and** Luis gate-8 authorization per candidate | Framework stable across ≥2 heterogeneous IKPs | 1 (may rise to 2 only by explicit Luis decision preserved in GitHub) | Same as Cohort A | ≥4 cumulative candidates APPROVED; documented coverage improvement vs. §4 | Same as Cohort A, plus: coverage duplication without justification | Cohort B |
| D | 11–15 | Complete the first roster of 15; prepare Analyst Council maturity path (MASTER-ROADMAP §9) | Cohort C exit criteria met **and** Council-readiness review recorded **and** Luis gate-8 authorization per candidate | Framework operating with several validated analysts concurrently | 1 (may rise to 2 only by explicit Luis decision preserved in GitHub) | Same as Cohort A | Roster disposition complete: every slot APPROVED, DEFERRED or REJECTED with preserved rationale | Same as Cohort A, plus: council-scale operational risks flagged by CRO | Cohort C |

## 6. Candidate lifecycle (fail-closed)

Roster-level lifecycle for every slot:

```
TBD → PROPOSED → PLANNED → RESEARCH_AUTHORIZED → RESEARCH_IN_PROGRESS
    → IKP_DRAFTED → VALIDATED → APPROVED → IMPLEMENTED → ACTIVE
```

Non-linear states: `DEFERRED`, `REJECTED`, `SUSPENDED`, `SUPERSEDED`,
`DEPRECATED`.

This lifecycle is the roster-management view of the approved architecture
lifecycle
([ARES-ARCHITECTURE-ANALYST-FRAMEWORK-001 §3](../architecture/ARES-ARCHITECTURE-ANALYST-FRAMEWORK-001.md)):
`PLANNED` corresponds to `CANDIDATE`; `RESEARCH_AUTHORIZED` to
`AUTHORIZED (gate 8)`; `IKP_DRAFTED` spans `RESEARCHED → PACKAGED`;
`VALIDATED` spans `CTO-IMPLEMENTATION-REVIEWED → CRO-VALIDATED →
QUANT-VALIDATED`; `ACTIVE` corresponds to `PRODUCTION`. The approved
architecture is not redesigned by this mapping.

**No lifecycle state activates research or implementation automatically.**
Every forward transition is a human decision recorded in the repository;
the framework engine never advances any state.

| Transition | Required evidence | Authorized decision-maker | Mandatory review | Repository artifact | Reversible? | New version required? |
|---|---|---|---|---|---|---|
| TBD → PROPOSED | Proposal addressing every §4 criterion (Unknowns allowed) | Any role may propose; CKO curates | CKO completeness check | Proposal document in `docs/roadmap/` (PR) | Yes (withdraw → TBD) | No |
| PROPOSED → PLANNED | Luis's naming decision preserved in GitHub | **Luis** | CTO + CRO advisory review of the proposal | Merged PR updating this roster | Yes (→ DEFERRED/REJECTED) | Roadmap minor version |
| PLANNED → RESEARCH_AUTHORIZED | All ARES-ANALYST-001 §1 gates 1–7 green; explicit named authorization | **Luis only** (gate 8) | CKO gate checklist; Publishing Engineer verification | Authorization record merged to `main` | Yes (revoke → SUSPENDED) | No |
| RESEARCH_AUTHORIZED → RESEARCH_IN_PROGRESS | Issued AssignmentRef (assignment intake) | CKO (accepts assignment) | Publishing Engineer records intake | Research assignment record | Yes (pause → SUSPENDED) | No |
| RESEARCH_IN_PROGRESS → IKP_DRAFTED | Complete knowledge base per ARES-ANALYST-001 §2 + drafted IKP passing structural validation | CKO handoff (no self-approval) | Publishing Engineer preservation check | Knowledge base + versioned IKP manifest (Draft) | Yes (reopen research) | IKP draft version |
| IKP_DRAFTED → VALIDATED | CTO architecture review PASS + CRO methodology review PASS + Quant testability review PASS (when applicable) | Each reviewer for their own gate | CTO, CRO, Quant — all mandatory | Signed review records in the PR / docs | Yes (→ REVISION via reviewer) | No |
| VALIDATED → APPROVED | Full validation chain evidence | **Luis only** | None beyond the chain (Luis's decision) | Luis's approval preserved in GitHub | Yes (rescind → SUSPENDED) | No |
| APPROVED → IMPLEMENTED | Implementation behind the plug-in contract; CI green | CTO (engineering governance, after Luis's authorization) | CTO implementation review | Merged implementation PR | Yes (roll back) | Package semver per architecture §9 |
| IMPLEMENTED → ACTIVE | Production activation decision | **Luis** (activation decision) | CRO risk confirmation | Activation record merged to `main` | Yes (→ SUSPENDED/DEPRECATED) | No |
| any → DEFERRED | Recorded rationale | Luis (or CKO with Luis's confirmation) | CKO records | Roster update PR | Yes (reinstate) | Roadmap minor version |
| any → REJECTED | Recorded rationale (e.g., §4 criterion failure) | Luis | Reviewer that identified the deficiency | Roster update PR | Yes (new proposal restarts at PROPOSED) | Roadmap minor version |
| ACTIVE/any → SUSPENDED | Recorded cause | Luis, or the reviewer function that identified the issue | CRO risk note | Suspension record | Yes (resume needs Luis) | No |
| any → SUPERSEDED | Later approved version exists | CKO (registry governance) | Publishing Engineer verification | Version registry update | No (history retained) | Yes (successor version) |
| ACTIVE → DEPRECATED | Retirement decision | Luis | CTO + CRO | Deprecation record; nothing deleted | No (append-only) | No |

## 7. Authorization matrix

Legend: **D** = decides (final authority) · **R** = performs/executes ·
**A** = advisory review (mandatory where noted) · **V** = verifies/publishes
· — = no role. AI reviews and assessments are advisory in all cases;
confidence is not institutional approval, and institutional approval is not
capital authorization.

| Action | CKO | Publishing Engineer | CTO | CRO | Quant | Luis |
|---|--:|--:|--:|--:|--:|--:|
| Propose candidate | R | — | A | A | A | D |
| Select candidate (name a slot) | A | — | A | A | — | **D** |
| Authorize research (gate 8) | — | — | — | — | — | **D (only)** |
| Conduct research | R | V | — | — | — | — |
| Draft IKP | R | V | — | — | — | — |
| Review architecture | — | — | **R/A (mandatory)** | — | — | — |
| Review methodology | — | — | — | **R/A (mandatory)** | — | — |
| Review testability | — | — | — | — | **R/A (when applicable)** | — |
| Approve IKP | — | — | A | A | A | **D (only)** |
| Authorize implementation | — | — | A | — | — | **D** |
| Merge documentation | — | **R (executes merge)** | A | A | — | **D (authorizes every merge)** |
| Activate analyst | — | V | A | A | — | **D (only)** |
| Use output for a capital decision | — | — | — | — | — | **D (only; no other role ever)** |

Institutional boundaries preserved (per
[research-governance.md](../specifications/research-governance.md)): the CKO
constructs and preserves knowledge; the Publishing Engineer verifies and
publishes; the CTO reviews architecture and implementation; the CRO reviews
methodology, epistemics and institutional risk; Quant reviews testability
when applicable; Luis provides final merge authorization and is the only
capital decision-maker.

## 8. Required future deliverables (per candidate, post-authorization)

**All items below are FUTURE deliverables.** None exists today; none may be
created before the candidate's individual gate-8 authorization. They follow
the research pipeline of MASTER-ROADMAP §6.2 and the ten templates in
[docs/templates/](../templates/README.md).

| # | Future deliverable | Produced by | Gate it serves |
|---|---|---|---|
| 1 | Research assignment record (issued AssignmentRef) | Luis / delegated CKO intake | Entry to RESEARCH_IN_PROGRESS |
| 2 | Source manifest (tiered per source hierarchy) | CKO | Source inventory phase |
| 3 | Primary-source evidence package | CKO | Claim extraction |
| 4 | Methodology dossier (claims → facts → principles) | CKO | Principle synthesis |
| 5 | Claim–evidence matrix (RULE 17 classes, grades A–E) | CKO | Fact verification |
| 6 | Contradiction register | CKO | Contradiction ledger phase |
| 7 | Rule extraction ledger (deterministic rules only) | CKO | Decision-rule formalization |
| 8 | Primitive mapping (rules → framework primitives) | CKO with CTO advisory | IKP packaging |
| 9 | Golden test vectors | CKO with Quant advisory | Validator + backcheck |
| 10 | Limitations and abstention conditions | CKO | CRO review |
| 11 | CRO methodology review record | CRO | VALIDATED |
| 12 | Quant testability review record | Quant | VALIDATED |
| 13 | CTO architecture review record | CTO | VALIDATED |
| 14 | Luis activation decision record | Luis | APPROVED / ACTIVE |
| 15 | Versioned IKP manifest | CKO, verified by Publishing Engineer | IMPLEMENTED |

## 9. Phase 5 Definition of Done

Phase 5 may be marked complete **only** when all of the following are true:

1. The roadmap contains 15 controlled slots (§3). ✔ in this draft
2. Every named candidate has canonical provenance (§1, §3). ✔ in this draft
3. Every unapproved slot remains `TBD` (§3). ✔ in this draft
4. Selection criteria are documented (§4). ✔ in this draft
5. Cohort sequencing is documented (§5). ✔ in this draft
6. Candidate lifecycle is documented (§6). ✔ in this draft
7. Authority boundaries are documented (§7). ✔ in this draft
8. Research remains blocked (no research content anywhere in the PR).
9. Sprint 7 remains not started.
10. The preserved framework document remains byte-identical (§10).
11. CTO review passes.
12. CRO review passes.
13. Luis explicitly approves the roadmap.
14. The documentation PR is merged into `main` by the Publishing Engineer
    with Luis's authorization.

Items 11–14 are **outside** this working PR: Phase 5 remains `pending` and
this document remains `Draft` until they occur. Marking Phase 5 complete
inside this PR would be a governance violation.

## 10. Preservation attestations

- `docs/specifications/ARES-ANALYST-FRAMEWORK-001.md` (Preserved Verbatim
  Institutional Document) is untouched by this PR. SHA-256:
  `cac6ad75becd98e3702411c8cdefce64558a9bfeac95251a4217808498711df9`.
- `docs/analysts/` remains structure-only (READMEs only).
- ARES remains v0.4.0; `v0.5.0` remains reserved for Sprint 7.
- Sprint 7 remains **not started**.
- No production or test code is changed by this PR.
- Nothing in this document authorizes research, implementation, activation
  or any capital action.
