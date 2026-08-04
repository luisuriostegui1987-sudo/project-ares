---
id: ARES-TPL-VALIDATION
title: Template: Validation record
status: Active (CTO and CRO reviews passed; merged to main with Luis's authorization)
version: 0.1.0
owner: CKO
governance: change only via pull request; merge only with Luis's authorization
---

# Template — Validation record

> **TEMPLATE.** Copy into the relevant analyst directory when research is
> authorized. Never populate with invented data; every field must trace to a
> real source per the specifications.

## Fields

- **validation_id**
- **target_ids** — facts/claims/rules validated
- **method** — re-verification, backcheck against later data, source audit
- **outcome** — VALID / INVALID / CONFLICTED
- **occurred_date**
- **recorded_by**
- **follow_ups**

## Rules

- All applicable [fact and evidence standards](../specifications/fact-and-evidence-standards.md) apply.
- Knowledge class and evidence grade are mandatory wherever defined.
- Unknowns are recorded explicitly; an empty unknowns field asserts there are none.
