---
id: ARES-SPEC-SOURCES
title: Source hierarchy
status: Active (CTO and CRO reviews passed; merged to main with Luis's authorization)
version: 0.1.0
owner: CKO
governance: change only via pull request; merge only with Luis's authorization
---

# Source hierarchy

| Tier | Description | Max evidence grade |
|---|---|---|
| T1 | Regulatory / official primary (filings, official statistics) | A |
| T2 | Subject's own primary output (books, letters, videos, interviews) | B |
| T3 | Reputable secondary (established financial press, with attribution) | C |
| T4 | Aggregated or community secondary (summaries, wikis, transcripts of unclear provenance) | D |
| T5 | Unverified (unattributed posts, screenshots, hearsay) | E |

Usage rules:

- Every Source record declares its tier at capture time.
- A claim's maximum evidence grade is bounded by its best source's tier.
- Tier is about provenance, not agreement: a T1 source can still be wrong —
  contradictions are handled per
  [uncertainty-and-contradictions](uncertainty-and-contradictions.md).
- Paywalled or ephemeral sources must be captured with enough locator detail
  (date, edition, timestamp) to be independently re-checkable.
