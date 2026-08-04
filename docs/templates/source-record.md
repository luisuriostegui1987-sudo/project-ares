---
id: ARES-TPL-SOURCE
title: Template: Source record
status: Active (CTO and CRO reviews passed; merged to main with Luis's authorization)
version: 0.1.0
owner: CKO
governance: change only via pull request; merge only with Luis's authorization
---

# Template — Source record

> **TEMPLATE.** Copy into the relevant analyst directory when research is
> authorized. Never populate with invented data; every field must trace to a
> real source per the specifications.

## Fields

- **source_id** — kebab-case, unique within the analyst
- **tier** — T1–T5 per the source hierarchy
- **type** — filing / book / letter / video / interview / article / dataset / other
- **title**
- **author_or_publisher**
- **published_date**
- **locator** — URL / accession / ISBN / timestamp — enough to re-check independently
- **captured_date**
- **access** — open / paywalled / archived
- **notes** — provenance caveats only — no content summary here

## Rules

- All applicable [fact and evidence standards](../specifications/fact-and-evidence-standards.md) apply.
- Knowledge class and evidence grade are mandatory wherever defined.
- Unknowns are recorded explicitly; an empty unknowns field asserts there are none.
