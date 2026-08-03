---
id: ARES-TPL-CLAIM
title: Template: Claim
status: Draft (pending CTO architecture review and CRO methodology review)
version: 0.1.0
owner: CKO
governance: change only via pull request; merge only with Luis's authorization
---

# Template — Claim

> **TEMPLATE.** Copy into the relevant analyst directory when research is
> authorized. Never populate with invented data; every field must trace to a
> real source per the specifications.

## Fields

- **claim_id**
- **statement** — verbatim-grounded; quote + citation for anything attributed
- **attributed_to**
- **source_ids** — >= 1
- **as_of_date**
- **knowledge_class** — RULE 17
- **evidence_grade** — A–E, bounded by best source tier
- **supporting_fact_ids / contradicting_fact_ids**
- **unknowns**
- **unresolved_questions**

## Rules

- All applicable [fact and evidence standards](../specifications/fact-and-evidence-standards.md) apply.
- Knowledge class and evidence grade are mandatory wherever defined.
- Unknowns are recorded explicitly; an empty unknowns field asserts there are none.
