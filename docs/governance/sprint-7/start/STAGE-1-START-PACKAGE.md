# Sprint 7 — Stage 1 Start Package (WU-0)

**Institutional record.** Luis resolved **L-1** (staged implementation; Stage 1
minimum authorized frozen scope) and **L-3** (start authorization, Gate 4),
after `GATE 2 PASS` (CTO) and `GATE 3 CONDITIONAL PASS — NON-BLOCKING CONTROLS
REMAIN` (CRO). Decision and review texts are preserved verbatim in this
directory. **WU-0 materializes the start; functional implementation
(WU-1…WU-9) begins only after the authorized merge of this Start Package.**

## State transition

`Sprint 7: not started → started — Stage 1 under frozen scope`

Phase 6 (Plug-in Analyst Framework) remains **`pending`** until the complete
framework is implemented and validated. Sprint 7 remains the canonical Phase 6
sprint; staging does not divide or reorder MASTER-ROADMAP phases (**L-2
amendment: NOT REQUIRED** — confirmed objectively at Gate 2 and ratified at
Gate 3).

## Stage 1 Frozen Scope (authorized by L-1, exactly as decided)

**MUST IMPLEMENT** — D1 lifecycle enums (sources exclusively roadmap §6 +
architecture §3; Workflow Status §3.1 EXCLUDED; homonyms separated by
provenance/type) · D2 transition matrix (14 canonical transitions; strict
whitelist; every unauthorized pair fail-closed) · D3 roster schema (12
canonical fields; `candidate_status` treated exclusively as a projection
derived from the event log per §5B.12; no second source of truth) · D4
invariants I-1…I-17 + authority vocabulary (roles, incompatibilities,
separation of functions, verifiable identity/authority) · D5 append-only
event log (institutional source of truth of state; deterministic ordering;
referential integrity; idempotency; duplicates; out-of-order; revocations as
events; fail-closed reconciliation; **no DB persistence in this stage**) ·
D6 independent-verification record per §5C (evidence and authority separated;
verification does not equal transition) · D7 test suite **T-1R…T-24**
(including T-20 exhaustive ordered-pair closure, T-21 transition-row
ablation, T-22/T-23 preservation/identity controls, and T-24 below) · D8
minimum implementation documentation · D9 framework compatibility attestation
(preserve the approved framework identity; no architecture redesign) · D10
institutional dossier/evidence package for later gates.

**MAY IMPLEMENT** — CI check for T-14 (framework SHA-256); strictly necessary
internal fixtures/helpers in `tests/analysts/`; the minimum post-Phase-5
documentary consistency fix (MASTER-ROADMAP §4, §6; roadmap README) —
materialized together with this Start Package.

**EXCLUDED — NOT AUTHORIZED IN STAGE 1** — Workflow Status §3.1 ·
`InstitutionalKnowledgePackageValidator` · loader · AssignmentRef intake ·
deterministic engine · AnalystRegistry/discovery · AnalystService/API ·
assessment persistence · DB migration 0003 · Quant harness · primitive
vocabulary v1 · research of any analyst · real IKP content · Benjamin Cowen
research · any gate-8 authorization · framework activation · `v0.5.0` ·
signals · operations · capital.

**DEFERRED** — every remaining Phase 6 component executes in later stages of
the **same Sprint 7**, each subject to a new express authorization from Luis
and its corresponding gates.

## T-24 — Stage 1 Research-Start Impossibility (contractual specification)

Binding part of **D7** (specification only; implementation lands with the
suite in WU-7). T-24 must demonstrate that **Stage 1 cannot start research by
construction**, verifying at minimum:

- **(A)** no input constructible through Stage 1 production paths can satisfy
  the transition `RESEARCH_AUTHORIZED → RESEARCH_IN_PROGRESS`;
- **(B)** absence of AssignmentRef intake/resolver ⇒ the required
  AssignmentRef evidence is an **unresolvable reference** in Stage 1;
- **(C)** an unresolvable reference ⇒ the transition is **rejected
  fail-closed** (explicit error; never a default);
- **(D)** no test mock/fixture can accidentally become production authority
  (mocks live only under `tests/`; production code contains no resolver, no
  test hook, no injection point that accepts test doubles);
- **(E)** any double needed to exercise the transition row remains confined
  to tests (and is itself asserted to be non-importable from `ares/`);
- **(F)** the D10 dossier must demonstrate this separation explicitly.

Result: even with D1–D6 fully implemented, advancing any slot into research
is structurally impossible until a later stage — separately authorized by
Luis — implements the intake, and the per-candidate **gate-8** authorization
(reserved exclusively to Luis) is granted.

## RG3 Controls (CRO Gate 3 — binding)

| ID | Control | Gate |
|---|---|---|
| RG3-1 | The rows `any → DEFERRED`, `any → REJECTED`, `any → SUSPENDED`, `any → SUPERSEDED` must be expanded explicitly, deterministically and finitely **before T-20**; an unexpanded rule means `NO TRANSITION PERMITTED` | INTERNAL — verified G6/G7 |
| RG3-2 | T-24 mandatory before G6; CRO verifies at G8 | INTERNAL — G6/G8 |
| RG3-3 | Preserve L-1, Gate 2, Gate 3 and L-3 | **CLOSED IN WU-0** (this directory) |
| RG3-4 | Minimum post-Phase-5 documentary reconciliation | **CLOSED IN WU-0** (roadmap edits in this PR) |
| RG3-5 | D8 must declare: `GitHub remains the institutional system of record.` The Stage 1 event log validates the discipline but does NOT replace the institutional registry | DEFERRED — G9 (D8) |

## N-1 / N-2 (closed at Gate 2, ratified at Gate 3)

**N-1:** `candidate_status` is exclusively a projection derived from the event
log and never a second source of truth (I-16/T-17); no modification of the
Active roadmap was required. **N-2:** the crosswalk gaps — including
`APPROVED`/`IMPLEMENTED` — are represented explicitly as
`NO MAPPING — FAIL CLOSED`; a correspondence is never invented.

## L-3 DOES NOT AUTHORIZE

- analyst research; - Benjamin Cowen research; - gate-8 for any candidate;
- IKP population; - Workflow Status §3.1; - framework activation;
- Phase 6 completion; - `v0.5.0`; - signals; - operations; - capital.

The framework (`docs/specifications/ARES-ANALYST-FRAMEWORK-001.md`) remains a
Preserved Verbatim Institutional Document, "Research Draft — Pending
Institutional Review", byte-identical
(`cac6ad75becd98e3702411c8cdefce64558a9bfeac95251a4217808498711df9`), and
inactive. Research remains **BLOCKED**. Canonical version remains **0.4.0**.
