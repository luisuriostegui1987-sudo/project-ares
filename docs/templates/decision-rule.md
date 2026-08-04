---
id: ARES-TPL-RULE
title: Template: Decision rule
status: Active (CTO and CRO reviews passed; merged to main with Luis's authorization)
version: 0.1.0
owner: CKO
governance: change only via pull request; merge only with Luis's authorization
---

# Template — Decision rule

> **TEMPLATE.** Copy into the relevant analyst directory when research is
> authorized. Never populate with invented data; every field must trace to a
> real source per the specifications.

## Fields

- **rule_id**
- **derived_from_principle_ids**
- **deterministic_formulation** — executable logic only — no judgment
- **inputs** — facts/signals with grades
- **output** — research flag only — NEVER a capital action; Luis decides
- **validation_record_ids**
- **version**

## Rules

- All applicable [fact and evidence standards](../specifications/fact-and-evidence-standards.md) apply.
- Knowledge class and evidence grade are mandatory wherever defined.
- Unknowns are recorded explicitly; an empty unknowns field asserts there are none.
