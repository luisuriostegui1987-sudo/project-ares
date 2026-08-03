---
id: ARES-TPL-PRINCIPLE
title: Template: Investment principle
status: Draft (pending CTO architecture review and CRO methodology review)
version: 0.1.0
owner: CKO
governance: change only via pull request; merge only with Luis's authorization
---

# Template — Investment principle

> **TEMPLATE.** Copy into the relevant analyst directory when research is
> authorized. Never populate with invented data; every field must trace to a
> real source per the specifications.

## Fields

- **principle_id**
- **statement** — the analyst's recurring position, in their terms
- **attributed_to**
- **supporting_claim_ids** — >= 2 independent occurrences
- **conditions_and_context** — when the analyst applies it
- **counter_examples** — where the analyst deviated
- **knowledge_class / evidence_grade**
- **contradiction_ids** — if any

## Rules

- All applicable [fact and evidence standards](../specifications/fact-and-evidence-standards.md) apply.
- Knowledge class and evidence grade are mandatory wherever defined.
- Unknowns are recorded explicitly; an empty unknowns field asserts there are none.
