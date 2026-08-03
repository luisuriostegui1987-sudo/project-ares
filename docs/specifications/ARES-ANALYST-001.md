---
id: ARES-ANALYST-001
title: Analyst research methodology
status: Draft (pending CTO architecture review and CRO methodology review)
version: 0.1.0
owner: CKO
governance: change only via pull request; merge only with Luis's authorization
---

# ARES-ANALYST-001 — Analyst research methodology

## 1. Authorization Gate (normative, first)

No research on any analyst may begin until Luis explicitly authorizes that
analyst by name. Until then, analyst directories contain ONLY structural
README files. Populating a template with real or invented content before
authorization is a governance violation.

## 2. Research phases (once authorized)

1. **Source inventory** — every source captured as a Source record
   (template: [source-record](../templates/source-record.md)) with tier per
   the [source hierarchy](source-hierarchy.md).
2. **Claim extraction** — verbatim-grounded claims with citations
   ([claim](../templates/claim.md)); no paraphrase without a locator.
3. **Fact verification** — claims promoted to facts only with grade A/B
   evidence ([fact](../templates/fact.md)).
4. **Principle synthesis** — recurring, cross-sourced positions become
   investment principles ([investment-principle](../templates/investment-principle.md)).
5. **Decision-rule formalization** — only principles expressible as
   deterministic rules become decision rules
   ([decision-rule](../templates/decision-rule.md)).
6. **Contradiction ledger** — every conflict recorded, never silently
   resolved ([contradiction](../templates/contradiction.md)).
7. **Reporting & validation** — research reports and validation records
   close the loop ([research-report](../templates/research-report.md),
   [validation-record](../templates/validation-record.md)).

## 3. Epistemic requirements

- Every statement carries a RULE 17 knowledge class
  (Verified Fact / High Confidence / Reasonable Inference / Speculation /
  Opinion / Unknown) and an evidence grade (A–E).
- A derived statement never carries a stronger class than its weakest support.
- "Unknown" is a valid, publishable state.
- Analyst positions are recorded as THEIR claims, never as ARES's view.

## 4. Prohibitions

- No signal or decision rule based on LLM judgment — deterministic logic only.
- No capital recommendations of any kind: ARES researches; Luis decides.
