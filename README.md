# ares-core

Core domain models for **Project ARES** — the AI-native investment *research*
platform. This is the first code commit: the objects the whole pipeline moves
around, implemented faithfully from **ARES-015** (Canonical Glossary & Data
Dictionary) and **ARES-003** (System Architecture).

## What's here

```
ares/models/
  enums.py      # RULE 17 classes, process states, horizons, verdicts, decision types
  base.py       # id generation, AresValidationError, helpers
  fact.py       # Fact        — verified, sourced, timestamped datum
  event.py      # Event       — + catalyst flag
  evidence.py   # Claim, Evidence
  thesis.py     # Thesis (+ Scores) — Constitution Sec 8 schema
  decision.py   # Decision    — Paper Decision Ledger record
tests/
  test_models.py  # rebuilds the CRWV run; proves the validators fire
```

## The models enforce the Constitution — in code

These aren't just schemas. The validators make governance non-optional:

- **A `Thesis` without a bear case or an invalidation condition cannot be
  constructed** (Constitution Sec 8).
- **A `Decision` to `APPROVE` requires `human_approved=True`** and a non-failing
  risk result — *no AI moves capital* (Constitution Sec 4 & 6).
- **Only `Verified Fact` / `High Confidence` facts are `usable_for_calculation`**,
  and a Verified Fact must carry a real source (Constitution Sec 5).
- **A `Verified Fact` / `High Confidence` claim needs supporting facts**
  (ARES-004 Sec 6).

## Run it (no dependencies)

```bash
python3 tests/test_models.py     # -> "7 tests passed."
```

## A note on the stack (ADR-023)

The target stack (ADR-023, *Proposed*) is **Pydantic v2**. Pydantic could not be
installed in the build sandbox (no network), so this first commit uses the
**standard library** (`dataclasses` + `Enum`) with equivalent `__post_init__`
validation, so the commit **runs and is verified now** rather than shipping
untested code. Migration is field-for-field: each `@dataclass` becomes a
`BaseModel`; each `require(...)` check becomes a `@field_validator` /
`@model_validator`. `requirements.txt` lists the target deps.

## Traceability

| Model | Source of truth |
|---|---|
| Fact | ARES-003 Sec 5.3 / ARES-015 |
| Event / Catalyst | ARES-015 |
| Claim / Evidence | ARES-004 Sec 6 / ARES-015 |
| Thesis / Scores | Constitution Sec 8 / ARES-003 Sec 5.6, 5.8 |
| Decision | ARES-003 Sec 5.11 / ARES-015 |

Next: wire these into the MVP vertical slice (ARES-003 Sec 14) — the CoreWeave
run, in code.
