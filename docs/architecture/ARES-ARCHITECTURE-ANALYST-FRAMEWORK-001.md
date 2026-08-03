---
id: ARES-ARCHITECTURE-ANALYST-FRAMEWORK-001
title: Analyst Framework — implementation architecture
status: Research Draft — Pending CTO Review
version: 1.1
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
  authorization), ARES-KNOWLEDGE-001 (knowledge package layout), the
  methodology standards (signals, sources, uncertainty), MASTER-ROADMAP §§6–9
  (sequencing: Framework = Phase 6; Council = Phase 9; 24/7 agents = Phase 10).
- **Institutional dependency (per CTO direction)**: ARES-ANALYST-FRAMEWORK-001
  has been drafted and reviewed in conversation by the CKO but is NOT yet
  preserved in the repository. It must be added — from the CKO-provided
  exact source, never reconstructed from this document — to the Knowledge
  Library branch (Draft PR #6) at
  `docs/specifications/ARES-ANALYST-FRAMEWORK-001.md` with status
  "Research Draft — Pending CRO Review and Luis Approval". Once preserved,
  this architecture must reference it by that path and its version, and be
  re-validated against it before any implementation. Until then, the interim
  institutional basis is MASTER-ROADMAP §7 plus ARES-ANALYST-001 v0.2.0.
- **Branch dependency**: the specifications this document cites live on the
  unmerged Draft PR #6 branch; this document therefore stacks on that branch
  and cannot merge before it.
- **Operational state (for accuracy; out of Sprint-6 scope)**: ARES v0.4.0
  is LIVE on Render; PostgreSQL is connected and healthy; the production
  health check passes. Deployment is complete and is not part of this
  sprint.

## 1. What is an Analyst inside the software?

**Institutional rule (normative, CTO-refined):**

> Analyst methodology is declarative by default. Analyst packages may not
> ship arbitrary executable business logic. New executable primitives,
> adapters or calculation operators require separate framework-level
> architecture review, versioning, tests and governance approval.

An Analyst is therefore a versioned, immutable **Knowledge Package** —
declarative data derived from the analyst's `docs/analysts/<name>/`
knowledge base — executed by ONE shared, generic engine:

```
Analyst = AnalystDescriptor            (identity, version, provenance)
        + PrincipleSet                 (documented principles, with doc refs)
        + RuleSet                      (deterministic rules as DATA:
                                        primitive-id + parameters + citations)
        + ConfidenceRubric             (deterministic scoring table)
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

**How analyst packages are prevented from executing arbitrary code** —
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
every assessment records the analyst package version, the contract version,
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
- **KnowledgePackageValidator**: structural + methodological validation at
  registration time (every rule cites principle ids; every principle cites
  claim/fact document ids; rubric is total and deterministic).

## 3. Analyst lifecycle

`CANDIDATE → AUTHORIZED (gate 8) → RESEARCHED (knowledge base complete) →
PACKAGED (knowledge package built + validated) → CTO-IMPLEMENTATION-REVIEWED
→ CRO-VALIDATED → QUANT-VALIDATED (point-in-time backcheck, no lookahead) →
PRODUCTION → DEPRECATED`

Deprecation retires an analyst version from execution; **nothing is ever
deleted** (append-only philosophy). Every state transition is a recorded
event with actor and date.

## 4. Input contract

`AnalystInput` (immutable snapshot):

- `entity` (canonical Entity)
- `evaluation_time` (decision time — ALL reads are as-of this instant)
- `facts`: graded `InstitutionalFact`s obtained via
  `FactRepository.current_facts_as_of(evaluation_time)` — the framework
  never receives facts newer than evaluation_time (no lookahead, mirroring
  the Quant-validation requirement)
- `prior_reports`: relevant `ResearchReport`s via `ReportRepository`
  (read-only, as-of filtered)
- `framework_context`: contract version, comparability predicate version

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
deterministic, versioned per analyst package
(`<analyst_id>/<rule_id>@<semver>` as `rule_version`), fail closed on
missing or non-comparable inputs, and always cite `source_fact_ids`.
The framework owns execution; the package owns parameters. No new signal
model is introduced.

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
score exists only if the analyst package defines a deterministic
ConfidenceRubric, the class obeys weakest-link inheritance, and the rubric
reference makes the number auditable. No rubric ⇒ class only. Never LLM
judgment.

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
2. **Analyst package version** (semver per analyst): knowledge content.
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
  loader.py       # knowledge-package loading + KnowledgePackageValidator
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
| Knowledge packages drift from their docs source | Medium | `knowledge_base_ref` pins the docs commit; validator recomputes derivation hash |
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
