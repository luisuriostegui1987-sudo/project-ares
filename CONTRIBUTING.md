# Contributing to ARES

Professional workflow for a small team (1 human + AI collaborators). Keep it
lightweight; every rule below earns its place.

## 1. Roles & ownership

| Role | Responsibility |
|---|---|
| **CKO** | Constructs and preserves institutional knowledge (specifications, templates, analyst knowledge bases) |
| **Publishing engineer** | Verifies, commits and publishes changes through pull requests |
| **CTO** | Reviews architecture and implementation |
| **CRO** | Reviews methodology, epistemics and institutional risk |
| **Quant Research** | Validates testable rules when applicable |
| **Luis** | Final authorization to merge; the **only capital decision-maker** |

Governance sequence for every change: publish via PR → CTO review → CRO
review → **Luis authorizes merge**. Coordination is **artifact-mediated**: the
repository, PRs and `docs/` are the shared memory — not chat.

## 2. Branch strategy (trunk-based)
- `main` is always releasable and **protected** (no direct pushes).
- Short-lived branches: `feat/<topic>`, `fix/<topic>`, `chore/<topic>`.
- Rebase/merge frequently; keep branches < a few days old.

## 3. Commits (Conventional Commits)
`type(scope): summary` — types: `feat, fix, refactor, test, docs, chore, ci`.
Small, atomic commits. Reference the governing repository document when a
commit embodies a decision.

## 4. Pull requests
- One logical change per PR; keep them small and reviewable.
- PR description: what changed, why, governing-doc refs, test evidence.
- **CI must be green** (pytest + ruff + mypy) before review.
- **≥1 human approval (Luis) required to merge.** AI approvals are advisory.
- Squash-merge to keep `main` history clean.

## 5. Code review checklist
- Consistency with the golden governance rules (CLAUDE.md) and the
  specifications in `docs/specifications/`.
- Traceability: numbers sourced; decisions link to governing repository docs.
- Tests cover happy path + invalid input; governance validators intact.
- No secrets, no scope creep, no undocumented decisions.

## 6. Testing gate (Definition of Done)
```bash
pytest -q && ruff check . && mypy ares
```
All three must pass. New models require tests (construction, governance
rejection, invalid input, serialization round-trip).

## 7. Local setup
```bash
git clone <repo> && cd ares-core
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
pytest -q
```
Recommended: pre-commit hook running ruff + mypy; VS Code or JetBrains with the
Claude Code extension.

## 8. Security
- Branch protection on `main`: require PR, require green CI, require 1 approval.
- No secrets in the repo. Use GitHub Actions **secrets** / a secrets manager.
- Least privilege: the Claude GitHub App / CI token gets only the scopes it needs
  (contents, pull-requests, issues). Review jobs get **read-only**.
- AI agents **create PRs; they never push to protected branches**.
- Prefer **signed commits** for an audit trail of AI-generated changes.
- Whitelist allowed shell commands for any CI agent (no `rm -rf`, `curl`, Docker).
