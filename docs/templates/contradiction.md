---
id: ARES-TPL-CONTRADICTION
title: Template: Contradiction
status: Draft (pending CTO architecture review and CRO methodology review)
version: 0.1.0
owner: CKO
governance: change only via pull request; merge only with Luis's authorization
---

# Template — Contradiction

> **TEMPLATE.** Copy into the relevant analyst directory when research is
> authorized. Never populate with invented data; every field must trace to a
> real source per the specifications.

## Fields

- **contradiction_id**
- **side_a** — claim/fact id + statement
- **side_b** — claim/fact id + statement
- **detected_date**
- **status** — OPEN / RESOLVED
- **resolution** — prevailing evidence, grade, reason — both sides remain on file
- **downgrades_applied**

## Rules

- All applicable [fact and evidence standards](../specifications/fact-and-evidence-standards.md) apply.
- Knowledge class and evidence grade are mandatory wherever defined.
- Unknowns are recorded explicitly; an empty unknowns field asserts there are none.
