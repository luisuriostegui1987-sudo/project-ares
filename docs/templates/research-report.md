---
id: ARES-TPL-REPORT
title: Template: Research report
status: Active (CTO and CRO reviews passed; merged to main with Luis's authorization)
version: 0.1.0
owner: CKO
governance: change only via pull request; merge only with Luis's authorization
---

# Template — Research report

> **TEMPLATE.** Copy into the relevant analyst directory when research is
> authorized. Never populate with invented data; every field must trace to a
> real source per the specifications.

## Fields

- **report_id**
- **question** — what this report answers
- **evidence_summary** — claim/fact ids with classes and grades
- **missing_evidence** — explicit
- **assumptions** — explicit
- **analysis** — base rates first
- **confidence** — RULE 17 class + 0-100
- **what_would_invalidate**
- **next_research**

## Rules

- All applicable [fact and evidence standards](../specifications/fact-and-evidence-standards.md) apply.
- Knowledge class and evidence grade are mandatory wherever defined.
- Unknowns are recorded explicitly; an empty unknowns field asserts there are none.
