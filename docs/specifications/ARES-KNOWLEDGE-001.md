---
id: ARES-KNOWLEDGE-001
title: Knowledge Library specification
status: Active (CTO and CRO reviews passed; merged to main with Luis's authorization)
version: 0.2.0
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

### 3.1 Preserved Verbatim Institutional Documents

An officially recognized document class for institutional documents that are
preserved verbatim from an authoritative external source (e.g., a
CKO-authored governance contract) and therefore cannot carry YAML front
matter. The class exists so that this exception is a governed rule, never an
ad-hoc file. Requirements:

- **Explicit authorization only**: a document may enter this class only when
  the exception is explicitly authorized through the standard governance flow
  (recorded in the pull request that preserves it); it is never a default.
- **Field-equivalent metadata table**: the document MUST begin with an
  institutional metadata table field-equivalent to the mandatory front
  matter (`id`, `title`, `status`, `version`, `owner`, governance/approval
  authority).
- **Byte-identical content**: the preserved content is never edited in
  place. Any change to the source contract arrives ONLY as a new preserved
  version with a new hash (append-only); the prior version is retained.
- **Mandatory SHA-256**: the document's SHA-256 is computed at preservation
  time and is part of its institutional identity.
- **Hash-recording references**: every repository document that references a
  Preserved Verbatim Institutional Document as a dependency MUST record the
  preserved SHA-256 it relied upon, so consumers can detect divergence.

Sole authorized instance at this version:
[ARES-ANALYST-FRAMEWORK-001](ARES-ANALYST-FRAMEWORK-001.md) v1.0
(sha256 `cac6ad75becd98e3702411c8cdefce64558a9bfeac95251a4217808498711df9`).

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
