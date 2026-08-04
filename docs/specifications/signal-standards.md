---
id: ARES-SPEC-SIGNALS
title: Signal standards
status: Draft (pending CTO architecture review and CRO methodology review)
version: 0.1.0
owner: CKO
governance: change only via pull request; merge only with Luis's authorization
---

# Signal standards

A documented signal is a DETERMINISTIC, versioned computation over graded
facts — never an impression, never LLM judgment.

Requirements:

1. **Rule identity**: name + semver (`SIGNAL-x.y`); any behavior change bumps
   the version. Matches the runtime convention in `ares/pipeline/signals.py`.
2. **Inputs**: only facts meeting the calculation gate (RULE 17 usable
   classes; comparable per the comparability predicate: same subject, scope,
   metric, basis, period type, unit, currency, scale or explicit
   normalization, comparable periods).
3. **Fail closed**: missing or non-comparable inputs produce NO signal —
   a missing signal is a valid outcome; a guessed one is not.
4. **Outputs**: measured value, baseline, direction, cited fact ids.
5. **Documentation**: every signal rule gets a Signal record
   ([template](../templates/signal.md)) before implementation.
