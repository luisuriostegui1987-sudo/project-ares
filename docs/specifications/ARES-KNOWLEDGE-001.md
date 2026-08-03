---
id: ARES-KNOWLEDGE-001
title: Knowledge Library specification
status: Draft (pending CTO architecture review and CRO methodology review)
version: 0.1.0
owner: CKO
governance: change only via pull request; merge only with Luis's authorization
---

# ARES-KNOWLEDGE-001 — Knowledge Library specification

## 1. Purpose

Define the structure, conventions and change rules of the ARES Knowledge
Library so that research knowledge accumulates in a durable, auditable,
machine-mappable form.

## 2. Structure contract

```
docs/
  specifications/   normative methodology (this spec and its siblings)
  templates/        the 10 reusable artifact templates
  analysts/<name>/  one knowledge base per analyst:
    sources/ claims/ facts/ signals/ principles/
    decision-rules/ contradictions/ reports/ validation/
  roadmap/          authorized product direction
```

Every directory MUST contain a `README.md` stating its purpose, the template
that governs its artifacts, and its research status.

## 3. Naming, metadata, versioning

- kebab-case names; one artifact per Markdown file.
- Mandatory YAML front matter: `id`, `title`, `status`, `version`, `owner`,
  `governance`.
- Per-document semver. Lifecycle: `Draft -> Reviewed -> Active -> Superseded`.
- Documents are never deleted; superseded versions remain with updated status
  and a pointer to their successor (append-only, mirroring the Fact store).

## 4. Epistemic alignment with the codebase

Documentary artifacts are designed to map 1:1 onto runtime objects so future
database ingestion is mechanical, not interpretive:

| Document artifact | Runtime object |
|---|---|
| Source record | `source_id` / `source_locator` provenance |
| Fact record | `InstitutionalFact` (ARES-FACT-001) |
| Claim record | `Claim` (knowledge class + supporting fact ids) |
| Signal record | `Signal` (deterministic rule + rule_version) |
| Validation record | `FactValidationEvent` |

## 5. Scalability rules

- **New analyst**: copy the analyst directory structure verbatim; no other
  change is required or permitted.
- **New artifact type**: requires a new template plus an update to this spec
  (version bump) — never ad-hoc files.
- **Future agents/APIs**: consumers must rely only on the structure and front
  matter defined here; nothing may depend on prose layout.

## 6. Change governance

Changes land only via pull request; the CKO owns methodology content; the CTO
reviews structure; the CRO reviews methodology; Luis authorizes every merge.
