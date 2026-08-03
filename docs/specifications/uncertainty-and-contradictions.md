---
id: ARES-SPEC-UNCERTAINTY
title: Uncertainty and contradiction handling
status: Draft (pending CTO architecture review and CRO methodology review)
version: 0.1.0
owner: CKO
governance: change only via pull request; merge only with Luis's authorization
---

# Uncertainty and contradiction handling

## Unknowns

"Unknown" is a first-class, publishable answer. Templates include explicit
`unknowns` fields; leaving them empty when unknowns exist is a methodology
violation. Missing evidence is recorded, never papered over.

## Contradictions

- Every detected conflict (source vs source, claim vs claim, analyst vs
  data) gets a Contradiction record ([template](../templates/contradiction.md)).
- Contradictions are never silently resolved: a resolution names the
  prevailing evidence, its grade, and the reason; both sides remain on file.
- While unresolved, all affected claims are downgraded to at most
  Reasonable Inference and marked CONFLICTED.

## Downgrade rules

1. Weakest-link: derived statements inherit their weakest support's class.
2. Conflict: unresolved contradiction caps the class and flags the artifact.
3. Staleness: facts past their validity horizon degrade to High Confidence
   at best until re-verified.
