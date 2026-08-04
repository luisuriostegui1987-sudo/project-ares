---
id: ARES-SPEC-FACTS
title: Fact and evidence standards
status: Active (CTO and CRO reviews passed; merged to main with Luis's authorization)
version: 0.1.0
owner: CKO
governance: change only via pull request; merge only with Luis's authorization
---

# Fact and evidence standards

## Documentary facts

A documentary fact is a dated, sourced, independently checkable statement.
It must reference at least one Source record, carry the source's locator
(URL, filing accession, timestamp/segment for media), an as-of date, a RULE 17
class, and an evidence grade. Numbers additionally follow ARES-FACT-001
semantics (basis, period, unit) so they can be ingested as `InstitutionalFact`
records later without reinterpretation.

## Evidence grades

| Grade | Meaning | Examples |
|---|---|---|
| A | Primary, independently verifiable | Regulatory filings, official datasets |
| B | Primary statement by the subject | The analyst's own publication/interview, timestamped |
| C | Reputable secondary reporting | Established press citing identifiable sources |
| D | Aggregated/community secondary | Transcripts of unverified provenance, wikis |
| E | Unsourced or opinion | Social posts without provenance, hearsay |

Rules: Verified Fact requires grade A. High Confidence requires A or B.
Grades D/E can support at most Speculation/Opinion. Corroboration across
independent sources is recorded, never assumed.

## Restatements

A correction never edits the original record: a new record supersedes it and
both remain, mirroring the append-only Fact store.
