---
id: ARES-DOCS-ROOT
title: ARES Knowledge Library
status: Draft (pending CTO architecture review and CRO methodology review)
version: 0.1.0
owner: CKO
governance: change only via pull request; merge only with Luis's authorization
---

# ARES Knowledge Library

The institutional memory layer of Project ARES: methodology specifications,
reusable research templates, per-analyst knowledge bases, and the authorized
product roadmap. Code enforces governance at runtime (see `ares/`); this
library records the METHODOLOGY that governs research itself.

> **RESEARCH STATUS: BLOCKED.** No investor research has been performed and none
> may begin until Luis explicitly authorizes it per analyst (ARES-ANALYST-001,
> Authorization Gate). This directory holds structure only.

## Map

| Area | Path | Contents |
|---|---|---|
| Specifications | [specifications/](specifications/README.md) | ARES-KNOWLEDGE-001, ARES-ANALYST-001, ARES-ANALYST-FRAMEWORK-001 and the methodology standards |
| Templates | [templates/](templates/README.md) | The 10 reusable research artifact templates |
| Analysts | [analysts/](analysts/README.md) | Empty, structured knowledge bases per analyst (research blocked) |
| Roadmap | [roadmap/](roadmap/README.md) | Authorized ARES OS product roadmap and the permanent continuous-improvement principle |
| Architecture | [architecture/](architecture/README.md) | Technical contracts translating specifications into software architecture |

## Conventions (normative)

- **Naming**: kebab-case file and directory names; one artifact per file.
- **Metadata**: every document begins with a YAML front-matter block
  (`id`, `title`, `status`, `version`, `owner`, `governance`).
- **Versioning**: per-document semver; status lifecycle
  `Draft -> Reviewed -> Active -> Superseded` (superseded documents are kept,
  never deleted — the library is append-only in spirit, like the Fact store).
- **Epistemics**: every substantive statement in future research artifacts
  must carry a RULE 17 knowledge class and an evidence grade
  (see [fact-and-evidence-standards](specifications/fact-and-evidence-standards.md)).
- **Scalability**: adding an analyst, strategy or source type never requires
  restructuring — copy the documented structure (ARES-KNOWLEDGE-001 §5).
