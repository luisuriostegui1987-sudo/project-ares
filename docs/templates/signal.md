---
id: ARES-TPL-SIGNAL
title: Template: Signal
status: Active (CTO and CRO reviews passed; merged to main with Luis's authorization)
version: 0.1.0
owner: CKO
governance: change only via pull request; merge only with Luis's authorization
---

# Template — Signal

> **TEMPLATE.** Copy into the relevant analyst directory when research is
> authorized. Never populate with invented data; every field must trace to a
> real source per the specifications.

## Fields

- **signal_id**
- **rule_version** — SIGNAL-x.y
- **deterministic_definition** — formula/pseudocode — no judgment terms
- **inputs** — fact requirements incl. comparability constraints
- **output** — value, baseline, direction
- **fail_closed_conditions** — when NO signal is emitted
- **provenance** — cited fact_ids

## Rules

- All applicable [fact and evidence standards](../specifications/fact-and-evidence-standards.md) apply.
- Knowledge class and evidence grade are mandatory wherever defined.
- Unknowns are recorded explicitly; an empty unknowns field asserts there are none.
