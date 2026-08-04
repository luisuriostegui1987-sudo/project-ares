---
id: ARES-ARCHITECTURE-ANALYST-FRAMEWORK-001
title: Analyst Framework — implementation architecture
status: Active — CTO and CRO reviews passed; merged to main via PR #7 with Luis's authorization; approved architecture (do not redesign); implementation reserved for Sprint 7
version: 1.4
owner: CTO implementation engineering
governance: architecture only — no implementation until CTO approval; change only via pull request; merge only with Luis's authorization
---

# ARES Analyst Framework — implementation architecture

This document is the technical contract between the institutional
specifications (ARES-ANALYST-001, ARES-KNOWLEDGE-001, ARES-FACT-001, the
methodology standards) and the software that will host **hundreds of
institutional analysts**. It contains **no implementation** — Sprint 6 is
architecture only.

## 0. Verified current state and dependencies

Inspected directly from the repository (not from prior conversation):

- **Layering in force** (must be respected):
  `ares/models` ← `ares/facts` · `ares/reports` ← `ares/pipeline` ·
  `ares/providers` ← `ares/service` ← `ares/api`. Lower layers never import
  upward.
- **Domain models available**: `InstitutionalFact` (ARES-FACT-001 subset:
  frozen, deterministic `fact_key`/`content_hash`, structured `Basis`),
  `Signal` (deterministic, `rule_version`), `Claim`/`Evidence` (RULE 17,
  weakest-link), append-only status events; `Thesis`/`Decision`/`Risk`
  exist but are dormant (Sprint-1 vintage) and are NOT dependencies here.
- **Persistence**: append-only `FactRepository` and `ReportRepository`
  protocols with memory + PostgreSQL implementations, point-in-time queries,
  advisory-locked migrations. The framework must consume these, not extend
  them.
- **Execution surface**: `ResearchService` is the single business-logic
  entry point; the FastAPI app is the single client entry point. The
  framework plugs UNDER the service layer, never beside it.
- **Institutional inputs**: ARES-ANALYST-001 (methodology + 8-gate
  authorization), ARES-KNOWLEDGE-001 (Knowledge Library layout), the
  methodology standards (signals, sources, uncertainty), MASTER-ROADMAP §§6–9
  (sequencing: Framework = Phase 6; Council = Phase 9; 24/7 agents = Phase 10).
- **Institutional dependency (RESOLVED)**: the CKO-authored Institutional
  Analyst Operating Contract is preserved verbatim at
  [`docs/specifications/ARES-ANALYST-FRAMEWORK-001.md`](../specifications/ARES-ANALYST-FRAMEWORK-001.md),
  **Version 1.0, Status: Research Draft — Pending Institutional Review**
  (sha256 `cac6ad75…711df9`). This architecture is revalidated against that
  exact contract in §0.1 below and must be revalidated again if the contract
  version changes. Supporting bases: MASTER-ROADMAP §7 and
  ARES-ANALYST-001 v0.2.0.
- **Branch dependency (RESOLVED)**: the specifications this document cites
  were merged to `main` via PR #6 (`a57fbc2`); this document was merged to
  `main` via PR #7 (`8b911ef`) in the approved institutional order. All cited
  specifications and this architecture now live on `main`.
- **Operational state (for accuracy; out of Sprint-6 scope)**: ARES v0.4.0
  is LIVE on Render; PostgreSQL is connected and healthy; the production
  health check passes. Deployment is complete and is not part of this
  sprint.

### 0.1 Revalidation against ARES-ANALYST-FRAMEWORK-001 v1.0 — compatibility matrix

Axis-by-axis revalidation against the preserved contract (§ numbers refer to
the contract). Verdicts: **COMPATIBLE** (architecture satisfies the axis as
designed), **COMPATIBLE (split)** (the axis is satisfied jointly by this
architecture and the documentary process/Knowledge Library, with the split
stated), **RESOLVED (v1.3)** (a former gap closed by a CTO-authorized
Required Change in this revision).

| # | Contract axis | Verdict | Basis / proposed smallest correction |
|---|---|---|---|
| 1 | Institutional Identity (§3) | COMPATIBLE | Analyst = declarative Institutional Knowledge Package with no deployment, write or approval authority; the engine executes, the service persists. The package structurally CANNOT deploy code, approve anything, or conceal uncertainty (ABSTAIN/contradictions are engine-enforced). |
| 2 | Authority Granted (§6) | COMPATIBLE | Granted powers are exactly what packages express: attributed claims, verified-fact consumption, labeled interpretations, candidate principles/rules/signals, escalatable unknowns — all as data for institutional review. |
| 3 | Authority Withheld (§7) | COMPATIBLE | No recommendation output type exists; packages cannot write to any store (the service appends assessments); no production-approval field exists for an analyst to set; merging/deployment are outside the framework entirely. |
| 4 | Required Inputs (§8) | **RESOLVED (v1.3)** | CTO Required Change #2 adopted: `AnalystInput` now requires an `AssignmentRef` (Assignment ID, Request Origin, Research Question, Scope, Evidence Standard, Requested Deliverables, Requested Reviewer Chain) and **the framework refuses execution without it** — see §4.1. |
| 5 | Analytical Lifecycle (§9) | COMPATIBLE (split) | Phases 1–4 (intake, design, acquisition, extraction) are the documentary research process (ARES-ANALYST-001 + Library templates) that BUILDS the knowledge base; phases 5–9 have mechanical counterparts in the engine (evaluation, classification, contradiction/uncertainty surfacing, synthesis into the assessment); phase 10 handoff = institutional review of packages and assessments. No phase is skipped; the split is by design. |
| 6 | Knowledge Classes (§5.3) | COMPATIBLE (mapping) | Verified Fact/Claim → existing models; Signal/Rule → candidate signals + package rules (research-only); Uncertainty → missing_evidence + unknowns; Contradiction → contradiction records. **Interpretation** maps to claims classed Reasonable Inference with mandatory reasoning — the mapping table will be normative in the contract types; no semantic change required. |
| 7 | Evidence Obligations (§10) | COMPATIBLE (split) | Sourcing, independence and staleness assessment are research-time obligations (Library standards, grades A–E, tiers T1–T5); the engine enforces the runtime consequences: only graded/usable facts reach rules, everything else surfaces as insufficient — "Insufficient evidence" is a first-class outcome. |
| 8 | Confidence & Workflow Status (§11) | **RESOLVED (v1.3, reserved)** | CTO Required Change #3 adopted: the Workflow Status lifecycle (REQUESTED→…→SUPERSEDED) is architecturally RESERVED with explicit ownership of every transition (§3.1) — documented only, not implemented; the engine never advances a status. The deterministic rubric→(High/Medium/Low/Unknown) confidence mapping remains a documented design element for the implementation phase. |
| 9 | Candidate Signals & Rules (§12) | **RESOLVED (v1.3)** | CTO Required Change #4 adopted: the generic **Institutional Candidate** concept (§8.1) is the parent of candidate signals/rules/metrics/indicators/heuristics/filters/transformations; every family carries the contract's §12 obligations and the status `Research Candidate — Not Production` until the full validation chain completes. The InstitutionalKnowledgePackageValidator rejects any rule/signal lacking a complete candidate record in the knowledge base. |
| 10 | Contradiction Protocol (§13) | COMPATIBLE (split) | Record richness (dates, regime changes, attempted reconciliations, owner) lives in the Library's contradiction template; the engine guarantees propagation, preservation of both sides, downgrades, and that resolution never happens by preference (only a new documented record resolves). |
| 11 | Unknowns & Missing Information (§14) | COMPATIBLE | ABSTAIN outcomes + missing_evidence entries name exactly what is missing; no gap is ever filled with an unstated assumption (packages cannot express assumptions outside declared parameters). |
| 12 | Required Deliverables (§15) | COMPATIBLE (split) | The §15 handoff package is the documentary deliverable (templates cover every listed artifact); the runtime deliverable (assessment) contains the machine-side subset with full attribution and citations. |
| 13 | Quality Gates (§16) | COMPATIBLE (split) | Mechanically checkable gates (classification separation, integrity of ids/links, governance status present, reproducibility metadata) are enforced by the InstitutionalKnowledgePackageValidator and assessment invariants; judgment gates (scope, independence, currency assessment) remain human review, as the contract intends. |
| 14 | Institutional Interfaces (§17) | COMPATIBLE | The architecture's validation chain (CTO implementation → CRO validation → Quant validation → Luis) and the publishing flow match §17's sequence verbatim; the framework adds no interface that bypasses any function's retained authority. |
| 15 | Escalation Requirements (§18) | COMPATIBLE (split) | The engine's fail-closed behaviors (refusal on contract mismatch, ABSTAIN on missing evidence, contradiction records) are the runtime form of "stop and escalate"; human escalation triggers (ambiguity, conflicts of interest, advice requests) belong to the documentary process and are unimpeded. |
| 16 | Version Control (§19) | COMPATIBLE | Semver on contract/package/vocabulary; append-only registry events record change, author and review linkage; git preserves history; a semantic change forces a NEW version/id everywhere — historical versions always preserved. |
| 17 | Completion Standard (§20) | COMPATIBLE (split) | Documentary completion is gated before packaging; the architecture adds the machine guarantee that an assessment is reproducible bit-for-bit without interviewing anyone (input digest + pinned versions). |
| 18 | Breach of Contract (§21) | COMPATIBLE | Several breaches become structurally impossible (fabricated evidence — packages cannot invent inputs; presenting candidates as approved — no approval field is analyst-writable; recommendations — no such output type); the rest remain detectable via append-only audit trails. |
| 19 | Effective-State Notice (§23) | COMPATIBLE | This architecture treats the contract as Research Draft; nothing becomes effective until the contract is approved and merged. (State reconciliation: this document passed CTO and CRO review and was merged to `main` via PR #7; implementation remains gated on Sprint 7 authorization by Luis AND on the formal activation of ARES-ANALYST-FRAMEWORK-001, whose preserved status remains Research Draft — Pending Institutional Review.) |

**Summary (v1.3)**: **19 of 19 axes compatible** — 7 via the explicitly
stated engine/documentary split, and the three former gaps RESOLVED by the
CTO's authorized Required Changes: #2 AssignmentRef (§4.1), #3 reserved
Workflow Status with transition ownership (§3.1), #4 Institutional
Candidate with mandatory candidate-record linkage and Research-Candidate
labeling (§8.1). No axis required reinterpreting the institutional
contract.

## 1. What is an Analyst inside the software?

**Institutional rule (normative, CTO-refined):**

> Analyst methodology is declarative by default. Institutional Knowledge
> Packages may not ship arbitrary executable business logic. New executable
> primitives, adapters or calculation operators require separate
> framework-level architecture review, versioning, tests and governance
> approval.

An Analyst is therefore a versioned, immutable **Institutional Knowledge
Package (IKP)** — declarative data derived from the analyst's
`docs/analysts/<name>/` knowledge base. The Institutional Knowledge Package
is the **primary architectural unit loaded by ARES**; the Execution Engine
consumes Institutional Knowledge Packages and nothing else. Its minimum
composition:

```
Institutional Knowledge Package =
    AnalystDescriptor          (identity, semver, provenance, authorization ref)
  + Knowledge Assets           (principle records with knowledge-base doc refs)
  + Institutional Metadata     (owner, status, review lineage, governance refs)
  + Evidence Requirements      (grades, tiers and comparability each rule demands)
  + Rule Definitions           (deterministic rules as DATA:
                                primitive-id@version + typed parameters + citations)
  + Signal Definitions         (Institutional Candidate signals: definition,
                                inputs, thresholds, fail-closed conditions)
  + Confidence Rubric          (deterministic scoring table)
  + Capability Matrix          (RESERVED — future declaration of which
                                primitive families the package may use)
  + Version Metadata           (package semver, contract-version range,
                                vocabulary-version pin)
  + Changelog                  (append-only change record per §19 of the
                                institutional contract)
```

Rules reference a **closed vocabulary of rule primitives** implemented once
inside the framework. Adding analyst N+1 is therefore *configuration plus
documented knowledge, never new architecture* (MASTER-ROADMAP §7) — and
never new business logic to review.

### 1.1 The declarative boundary and primitive governance

**What belongs in declarative analyst configuration** — identity and
provenance metadata; principle records citing knowledge-base documents; rule
instances, each exactly `(primitive_id@version, typed parameters, input
requirements, citations)`; confidence rubric tables; thresholds and metric
references. Nothing else: no expressions, no formulas, no code in any form.

**What belongs in the generic execution engine** — input-snapshot
construction, rule scheduling, primitive dispatch, epistemic bookkeeping
(weakest-link classes, downgrades, ABSTAIN handling), assessment assembly,
deterministic explanation rendering, persistence handoff. The engine is
analyst-agnostic by construction.

**What qualifies as a framework primitive** — a named, semver-versioned,
side-effect-free, deterministic operator implemented inside the framework
(`primitives/`), with: a typed parameter schema, declared input-fact
requirements (including comparability constraints), explicit ABSTAIN
conditions, an explanation template, and exhaustive tests with golden
vectors. Primitives are framework code and receive framework-level review —
never analyst-package content.

**How specialized methodologies request a new primitive** — quantitative,
technical, macro or on-chain methodologies that need an operator the
vocabulary lacks submit a **Primitive Proposal**: motivation citing the
analyst's documented methodology, a formal deterministic definition,
parameter schema, input requirements, failure modes, and test vectors. The
proposal passes CTO architecture review, CRO methodology review and
governance approval before implementation and registration. Until the
primitive exists, dependent rules ABSTAIN with a missing-capability record —
they never inline a workaround.

**How primitive additions preserve determinism and backward compatibility** —
primitives are pure functions over typed inputs; additions are new registry
entries that cannot alter existing behavior; a semantic change to an
existing primitive is FORBIDDEN — changed behavior is a NEW primitive id.
Packages pin exact `primitive_id@version` pairs, so an addition can never
reinterpret an existing rule.

**How Institutional Knowledge Packages are prevented from executing arbitrary code** —
packages are pure data validated against a closed schema at load time; the
loader rejects any field outside the schema; there is no eval/exec/import
path from package content; primitives are resolved exclusively by id from
the in-repo registry; the package's content hash is pinned at registration,
so post-validation tampering is detectable.

**How the primitive registry is versioned append-only** — the registry is an
event log of registrations `(primitive_id, version, definition hash,
review record)`; deprecation is an event, removal does not exist; the
vocabulary version increases monotonically and is recorded on every
assessment.

**How existing analysts remain reproducible after primitive upgrades** —
every assessment records the Institutional Knowledge Package version, the contract version,
and the exact `primitive_id@version` used per rule, plus the input digest;
historical primitive versions remain resolvable forever, so any past
assessment can be re-executed bit-for-bit.

## 2. Interfaces every analyst must satisfy (conceptual contract)

Described here as contracts; Python Protocols will be written only after CTO
approval.

- **AnalystDescriptor**: `analyst_id`, `semver`, `contract_version` range,
  `knowledge_base_ref` (path + git commit of the docs it was derived from),
  `authorization_ref` (record of Luis's gate-8 authorization).
- **AnalystContract**: one operation —
  `evaluate(AnalystInput) -> AnalystAssessment`. Pure: no I/O, no clock, no
  randomness; everything arrives in the input.
- **InstitutionalKnowledgePackageValidator**: structural + methodological validation at
  registration time (every rule cites principle ids; every principle cites
  claim/fact document ids; rubric is total and deterministic).

## 3. Analyst lifecycle

`CANDIDATE → AUTHORIZED (gate 8) → RESEARCHED (knowledge base complete) →
PACKAGED (Institutional Knowledge Package built + validated) → CTO-IMPLEMENTATION-REVIEWED
→ CRO-VALIDATED → QUANT-VALIDATED (point-in-time backcheck, no lookahead) →
PRODUCTION → DEPRECATED`

Deprecation retires an analyst version from execution; **nothing is ever
deleted** (append-only philosophy). Every state transition is a recorded
event with actor and date.

### 3.1 Workflow Status (RESERVED — documented only, not implemented)

Per the institutional contract (§11.2), every material analytical output
will eventually carry a workflow status. This architecture RESERVES the
lifecycle and its transition ownership; **no implementation exists or may
exist until separately approved**:

```
REQUESTED → RESEARCHING → UNDER_REVIEW → CRO_REVIEW → QUANT_REVIEW
          → APPROVED → PRODUCTION → SUPERSEDED
```

| Transition | Owner of the transition |
|---|---|
| (create) → REQUESTED | Requester via assignment intake (AssignmentRef issued; Luis or delegated CKO intake) |
| REQUESTED → RESEARCHING | CKO (accepts the assignment; analyst work begins under the operating contract) |
| RESEARCHING → UNDER_REVIEW | Analyst handoff (§9 Phase 10 of the contract — no self-approval); publishing engineer verifies preservation |
| UNDER_REVIEW → CRO_REVIEW | CKO (research package complete and preserved) |
| CRO_REVIEW → QUANT_REVIEW | CRO (methodology approved; risk acceptance recorded) |
| QUANT_REVIEW → APPROVED | Quant Research validates → **Luis grants approval** (only Luis can set APPROVED) |
| APPROVED → PRODUCTION | CTO (implementation/deployment under engineering governance, after Luis's authorization) |
| any → SUPERSEDED | Registry governance (CKO) when a later APPROVED version replaces it; the superseded record is retained forever |
| any → REJECTED / REVISION_REQUIRED (contract §11.2) | The reviewer function that identified the deficiency; rationale preserved |

Reverse transitions never erase history: every movement is an append-only
event with actor and date. The engine itself NEVER advances a workflow
status — status transitions belong exclusively to the institutional
functions above.

## 4. Input contract

`AnalystInput` (immutable snapshot):

- `assignment_ref` (**required — see §4.1**)
- `entity` (canonical Entity)
- `evaluation_time` (decision time — ALL reads are as-of this instant)
- `facts`: graded `InstitutionalFact`s obtained via
  `FactRepository.current_facts_as_of(evaluation_time)` — the framework
  never receives facts newer than evaluation_time (no lookahead, mirroring
  the Quant-validation requirement)
- `prior_reports`: relevant `ResearchReport`s via `ReportRepository`
  (read-only, as-of filtered)
- `framework_context`: contract version, comparability predicate version

### 4.1 AssignmentRef (required for every execution)

Every analyst execution carries an **AssignmentRef** — the institutional
assignment envelope required by the operating contract (§8 of
ARES-ANALYST-FRAMEWORK-001). It contains:

- **Assignment ID** (unique research/assignment identifier)
- **Request Origin** (who requested the work and in what capacity)
- **Research Question** (the defined question and decision context)
- **Scope** (boundaries and explicit exclusions)
- **Evidence Standard** (the applicable standard for this assignment)
- **Requested Deliverables** (expected outputs and destination)
- **Requested Reviewer Chain** (the review path and accountable owner)

**The framework refuses execution without a complete AssignmentRef** — the
architectural mirror of the contract's "pause and request clarification"
duty: a consequential assumption is never chosen silently. Every persisted
`AnalystAssessment` records its AssignmentRef for full attribution.

**Provenance, not just completeness (CRO Required Correction, v1.4)**: the
Assignment ID MUST resolve to a recorded, append-only institutional intake
event (the intake defined in §3.1, "(create) → REQUESTED"); the framework
MUST refuse execution when the AssignmentRef cannot be resolved to such a
record. A syntactically complete but never-issued AssignmentRef is therefore
not executable. (Architecture only; no implementation in this sprint.)

## 5. Output contract

`AnalystAssessment` (immutable, append-only once persisted):

- `analyst_id` + `analyst_version` + `contract_version` (full attribution)
- `rule_outcomes`: one per executed rule — `FIRED | NOT_FIRED | ABSTAINED`,
  with cited input fact ids and parameters used
- `signals`: domain `Signal` objects (rule_version = analyst-scoped id)
- `claims`: RULE 17-classed claims citing fact ids
- `contradictions`, `missing_evidence`, `explanations`, `confidence`
  (structures defined in §§9–12)
- `input_digest`: hash of the input snapshot for reproducibility audits

## 6. Consuming Institutional Facts

Read-only, through the existing `FactRepository` protocol with the
point-in-time API — never raw SQL, never mutation. Only facts passing the
calculation gate (RULE 17 usable classes + VALID status) and the
comparability predicate reach rules; everything else surfaces as
missing/unusable evidence, not as silent input.

## 7. Consuming Research Reports

Read-only through `ReportRepository`. Prior reports are evidence about past
ARES output (e.g., signal history), never authority: a rule may cite a prior
report id but may not treat report prose as fact.

## 8. Producing Signals

Via the existing `Signal` domain model and the signal standards: rules are
deterministic, versioned per Institutional Knowledge Package
(`<analyst_id>/<rule_id>@<semver>` as `rule_version`), fail closed on
missing or non-comparable inputs, and always cite `source_fact_ids`.
The framework owns execution; the package owns parameters. No new signal
model is introduced.

### 8.1 Institutional Candidate (generic parent concept)

The narrow concept "Candidate Signal" is replaced by the generic
institutional concept **Institutional Candidate**: any analyst-proposed,
research-only artifact awaiting the institutional validation chain. It is
the parent concept for the future families:

- Candidate Signals
- Candidate Rules
- Candidate Metrics
- Candidate Indicators
- Candidate Heuristics
- Candidate Filters
- Candidate Transformations

Every Institutional Candidate, regardless of family, shares the same
contract obligations (§12 of ARES-ANALYST-FRAMEWORK-001): unique id and
version, exact definition, documented evidence for and against,
falsification conditions, and the status
**`Research Candidate — Not Production`** until CRO review, CTO feasibility,
Quant validation and Luis's authorization complete. The engine treats every
family identically: deterministic evaluation, fail-closed inputs, full
citation — a new family never requires new architecture, only (at most) new
reviewed primitives. (Concept only; no implementation in this sprint.)

## 9. Propagating Contradictions

When rules of one analyst conflict internally, when an analyst's claim
conflicts with a graded fact, or when (later) Council members disagree, the
framework emits Contradiction records (per the uncertainty specification):
both sides cited by id, never silently resolved, with weakest-link
downgrades applied to affected outputs. Contradictions travel inside the
assessment AND are persisted append-only so they survive into reports.

## 10. Propagating Missing Evidence

Every rule declares its required inputs. An unmet requirement produces an
`ABSTAINED` outcome plus a `missing_evidence` entry naming exactly what was
missing (metric, period, grade). Missing evidence is a first-class,
publishable result — a missing signal is a valid outcome; a guessed one is
not.

## 11. Explanations

Deterministic template rendering ONLY: each rule primitive carries an
explanation template; the rendered explanation interpolates rule id,
parameters, cited fact ids and values. An explanation is reproducible from
the assessment record alone. No free-text generation at evaluation time.

## 12. Confidence

`confidence = (rule17_class, score_0_100 | None, rubric_ref)` where the
score exists only if the Institutional Knowledge Package defines a deterministic
ConfidenceRubric, the class obeys weakest-link inheritance, and the rubric
reference makes the number auditable. No rubric ⇒ class only. Never LLM
judgment.

### 12.1 Normative confidence crosswalk (CRO Required Correction, v1.4)

The institutional contract (ARES-ANALYST-FRAMEWORK-001 §11.1) expresses
confidence as **High / Medium / Low / Unknown**; ARES expresses it as
**RULE 17 knowledge class + evidence grade (A–E)**. The following mapping is
the **authoritative, normative crosswalk** between the two vocabularies and
is frozen input to the implementation phase (contract types will encode it
verbatim):

| §11.1 level | Minimum ARES requirement (deterministic) |
|---|---|
| **High** | Verified Fact (grade A), OR High Confidence with grade A **and** recorded independent corroboration; in both cases no unresolved material contradiction |
| **Medium** | High Confidence (grade A–B) not meeting the High row |
| **Low** | Reasonable Inference (grade ≤ C); any Speculation or Opinion (grades D–E always cap here) |
| **Unknown** | Knowledge class Unknown, or evidence insufficient to assign a defensible grade |

Normative rules:

1. **Knowledge may NEVER become stronger than its weakest supporting
   evidence, regardless of vocabulary.** Weakest-link inheritance applies on
   both sides of the crosswalk: a derived statement takes the minimum of its
   supports' RULE 17 classes AND the minimum of their §11.1 levels.
2. An unresolved material contradiction caps the statement at **Low** —
   consistent with the uncertainty standard's downgrade to at most
   Reasonable Inference (CONFLICTED).
3. The mapping is total and surjective: every classified statement resolves
   to exactly one §11.1 level; no statement may carry a §11.1 level that the
   table does not derive from its class and grade.
4. Movement up the table requires new evidence meeting the higher row's
   requirement, documented per §5.4 of the institutional contract — never
   relabeling.

## 13. Registration

An **append-only AnalystRegistry**: registering a package records
(descriptor, package content hash, validation events). Same-content
re-registration is idempotent (content-hash dedup, like the Fact store);
a changed package REQUIRES a new version. Registry state is derived from its
event log — no mutable "current" flag stored.

## 14. Plugin discovery

Phase 6 (initial): declarative — packages live in a versioned in-repo
location; the registry loads an explicit manifest list (no filesystem
scanning, no import side effects). Later phases MAY add Python entry-point
discovery behind the same registry interface; discovery mechanism is an
implementation detail hidden behind `AnalystRegistry`, so nothing upstream
changes.

## 15. Dependency injection

Constructor injection, exactly like the existing services: the future
`AnalystService` receives `FactRepository`, `ReportRepository` and
`AnalystRegistry` instances (explicit selection semantics, never silent
fallbacks — the Gate-2 doctrine applies unchanged). Rule primitives receive
everything through `AnalystInput`; they can touch nothing else.

## 16. Versioning

Three independent axes:

1. **Framework contract version** (semver): the shape of
   AnalystInput/Assessment.
2. **Institutional Knowledge Package version** (semver per analyst): knowledge content.
3. **Rule primitive vocabulary version**: additions are minor; changes to
   an existing primitive's semantics are MAJOR and forbidden — a changed
   behavior is a NEW primitive id (append-only vocabulary).

Every assessment records all three, so any historical output is
reconstructible.

## 17. Upgrades

An analyst upgrade is a NEW package version registered alongside the old
one. Old versions remain executable for reproduction of historical
assessments. Promotion of a new version to production repeats the validation
chain (CTO/CRO/Quant) — versions never mutate in place.

## 18. Backward compatibility

- Contract changes: additive-only within a major version; packages declare a
  compatible contract range; the registry refuses execution outside it
  (fail closed, no adaptation shims).
- Primitive vocabulary: append-only (§16).
- Persisted assessments: schema versioned like ResearchReport; old records
  remain readable forever (canonical JSON + model validation, the proven
  Fact-store pattern).

## 19. Analyst Council execution (Phase 9 — designed for, not built)

The Council is an orchestrator ABOVE the framework: it executes N analysts
against the SAME `AnalystInput` snapshot (identical evaluation_time; trivially
parallelizable because `evaluate` is pure), then aggregates assessments into
a CouncilReport that preserves per-analyst attribution. Disagreement between
analysts becomes recorded Contradictions — never averaged away, never
majority-voted into false certainty. The Council introduces no new analyst
contract; maturity requires several validated production analysts
(MASTER-ROADMAP §9), and 24/7 agents come only after that (§10).

## 20. One hundred analysts without framework changes

Guaranteed structurally: analysts are data (no per-analyst code), the
primitive vocabulary is closed and append-only, the registry is O(1) per
registration, execution is pure and parallel, and every extension point
(discovery mechanism, storage backend, execution topology) hides behind a
protocol. The framework changes only when the CONTRACT changes — which is
versioned and additive.

---

## A. Component diagram (text)

```
            ┌────────────────────────────────────────────────┐
            │                 ares/api (FastAPI)             │
            └───────────────────────┬────────────────────────┘
                                    │
            ┌───────────────────────▼────────────────────────┐
            │   ares/service  (ResearchService, future       │
            │   AnalystService, future CouncilService)       │
            └──────┬──────────────────┬───────────────┬──────┘
                   │                  │               │
     ┌─────────────▼──────┐  ┌────────▼─────────┐  ┌──▼───────────────────┐
     │ ares/pipeline      │  │ future           │  │ ares/providers       │
     │ (research stages)  │  │ ares/analysts    │  │ (EDGAR, ...)         │
     │                    │  │  contract        │  └──┬───────────────────┘
     └──────┬─────────────┘  │  registry        │     │
            │                │  primitives      │     │
            │                │  loader          │     │
            │                └────────┬─────────┘     │
     ┌──────▼──────────────────────── ▼───────────────▼──────┐
     │ ares/facts (FactRepository)  ares/reports (ReportRepo)│
     └──────────────────────────┬────────────────────────────┘
                                │
     ┌──────────────────────────▼────────────────────────────┐
     │ ares/models (InstitutionalFact, Signal, Claim, ...)   │
     └───────────────────────────────────────────────────────┘
```

Arrows point downward only (import direction). `ares/analysts` is a NEW
sibling of `ares/pipeline`, below `ares/service`, above the repositories.

## B. Sequence diagram (text) — one evaluation

```
Caller            AnalystService      Registry        FactRepo/ReportRepo     Engine(package)
  │ evaluate(entity,   │                 │                    │                    │
  │  analyst_id, t)    │                 │                    │                    │
  ├───────────────────>│ resolve(id,ver) │                    │                    │
  │                    ├────────────────>│ package+descriptor │                    │
  │                    │<────────────────┤ (contract checked) │                    │
  │                    │ current_facts_as_of(t) / reports(t)  │                    │
  │                    ├─────────────────────────────────────>│                    │
  │                    │<─────────────────────────────────────┤ immutable snapshot │
  │                    │ build AnalystInput(entity, t, facts, reports)             │
  │                    ├──────────────────────────────────────────────────────────>│
  │                    │        evaluate: rules → outcomes/signals/claims/         │
  │                    │        contradictions/missing/explanations/confidence     │
  │                    │<──────────────────────────────────────────────────────────┤
  │                    │ persist AnalystAssessment (append-only)                   │
  │<───────────────────┤ assessment (fully attributed, reproducible)               │
```

## C. Proposed package structure (NOT created in this sprint)

```
ares/analysts/
  contract.py     # AnalystInput / AnalystAssessment / AnalystContract (typed)
  descriptor.py   # AnalystDescriptor, versioning metadata
  primitives/     # closed deterministic rule-primitive vocabulary
  loader.py       # Institutional Knowledge Package loading + validator
  registry.py     # append-only AnalystRegistry + discovery seam
  engine.py       # the single generic evaluation engine
  service.py      # AnalystService (DI: repos + registry)
  council.py      # Phase 9 only — orchestration over the same contract
tests/analysts/   # contract tests, golden assessments, PIT/no-lookahead
```

## D. Module responsibilities & dependency graph

| Module | Responsibility | May import |
|---|---|---|
| contract | types only | models |
| descriptor | identity/version metadata | models |
| primitives | deterministic rule vocabulary | models, contract |
| loader | package parsing + validation | contract, descriptor, primitives |
| registry | append-only registration/resolution | descriptor, loader |
| engine | execute package against input | contract, primitives |
| service | orchestration + persistence | all above + facts + reports |
| council | multi-analyst orchestration | service, contract |

Graph (edges = imports): `service → {engine, registry, facts, reports}`;
`engine → {contract, primitives}`; `registry → {loader, descriptor}`;
`loader → {contract, descriptor, primitives}`; everything → `models`.
No cycles; no upward imports; pipeline and analysts never import each other
(both are consumed by service).

## E. Plugin lifecycle

`authored (docs) → packaged → validated (structural+methodological) →
registered (append-only event) → resolvable → executable → deprecated
(event; still resolvable for reproduction) — never deleted`

## F. Execution flow summary

Single analyst: §B. Council (Phase 9): fan-out over the same snapshot,
gather assessments, aggregate with attribution, record disagreements as
contradictions. Agents (Phase 10): schedule Council executions — no new
contracts.

## G. Future migration strategy (distributed execution)

Because `evaluate` is pure over an immutable snapshot: in-process (Phase 6)
→ worker pool in one host (Council initial) → distributed workers consuming
(input_digest, package_ref) tasks with assessments appended to shared
storage. The contract never changes; only the dispatcher does. Preconditions
already met by design: PIT snapshots, content-addressed packages, append-only
outputs, full attribution.

## H. Risk assessment

| Risk | Severity | Mitigation |
|---|---|---|
| Primitive vocabulary too weak → pressure to add per-analyst code | High | Vocabulary grows append-only via CTO-reviewed additions; escape hatch is a NEW primitive, never inline code |
| Institutional Knowledge Packages drift from their docs source | Medium | `knowledge_base_ref` pins the docs commit; validator recomputes derivation hash |
| Contract churn during early analysts | Medium | Contract semver + compatibility ranges; additive-only within major |
| ARES-ANALYST-FRAMEWORK-001 spec published later and diverges | Medium | Re-validation checkpoint before implementation begins (recorded in §0) |
| Council groupthink / false consensus | Medium | Aggregation preserves attribution; disagreement = contradiction records, no averaging |
| Performance at 100+ analysts | Low | Pure parallel evaluation; snapshot built once per (entity, t) |

## I. Known architectural tradeoffs

- **Analysts-as-data vs analysts-as-code**: chosen data. Cost: expressive
  ceiling bounded by the primitive vocabulary. Benefit: OCP, bounded review
  surface, determinism, N+1 = configuration. The ceiling is raised by
  vocabulary additions, which are cheap and centrally reviewed.
- **Closed primitive vocabulary vs sandboxed user code**: sandboxing rejected
  — undecidable review burden, nondeterminism risk, security surface.
- **Declarative manifest discovery vs entry-point scanning (now)**: manifest
  chosen for auditability; scanning can arrive later behind the registry.
- **In-process execution first vs distributed-first**: in-process chosen;
  distribution is a dispatcher swap thanks to purity (§G) — building it now
  would violate the roadmap's anti-deviation directive.

## J. Alternatives considered and rejected

1. **Per-analyst Python classes implementing a base interface** — rejected:
   violates OCP at scale, unbounded per-analyst code review, invites logic
   duplication, makes 100 analysts 100 codebases.
2. **LLM-interpreted principles at evaluation time** — rejected outright:
   non-deterministic, violates non-negotiable principle #4 and the signal
   standards.
3. **Microservice per analyst** — rejected as premature: operational cost
   without benefit at current scale; purity already buys future distribution.
4. **Storing assessments inside ResearchReport** — rejected: different
   lifecycle and cardinality; assessments get their own append-only store
   patterned on the report store.

## K. Future implementation plan (post-approval)

1. Freeze contract types + primitive vocabulary v1 (smallest set needed by
   the first analyst's documented rules).
2. Loader + validator + registry with golden-package fixtures.
3. Engine + deterministic explanation rendering + assessment persistence
   (memory + PostgreSQL, migration 0003, same hardening pattern).
4. AnalystService + API read surface (no new mutation endpoints).
5. Quant-validation harness: PIT backcheck runner over historical snapshots.
Each step lands as its own reviewed PR; implementation starts ONLY after CTO
approval of this document.
