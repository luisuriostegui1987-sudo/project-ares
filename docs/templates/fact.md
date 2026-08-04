---
id: ARES-TPL-FACT
title: Template: Fact
status: Draft (pending CTO architecture review and CRO methodology review)
version: 0.1.0
owner: CKO
governance: change only via pull request; merge only with Luis's authorization
---

# Template — Fact

> **TEMPLATE.** Copy into the relevant analyst directory when research is
> authorized. Never populate with invented data; every field must trace to a
> real source per the specifications.

## Fields

- **fact_id**
- **statement or metric** — numbers follow ARES-FACT-001: basis, period, unit
- **source_ids** — grade A/B required
- **as_of_date**
- **knowledge_class**
- **evidence_grade**
- **verification_method** — how it was independently checked
- **supersedes_fact_id** — restatements create NEW records
- **valid_until** — staleness horizon

## Rules

- All applicable [fact and evidence standards](../specifications/fact-and-evidence-standards.md) apply.
- Knowledge class and evidence grade are mandatory wherever defined.
- Unknowns are recorded explicitly; an empty unknowns field asserts there are none.
