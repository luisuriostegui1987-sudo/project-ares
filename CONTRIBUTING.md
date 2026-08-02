# Contributing to ARES

Professional workflow for a small team (1 human + 2 AI collaborators). Keep it
lightweight; every rule below earns its place.

## 1. Roles & ownership (RACI)

| Activity | Luis (CIO) | ChatGPT (CTO/Architect) | Claude (Principal Eng / Reviewer) |
|---|---|---|---|
| Architecture design | Approves | **Owns** | Reviews, challenges |
| ADRs (Drive) | Approves | Authors design ADRs | Authors/records, keeps consistent |
| Writing code | — | Authors (arch-heavy modules) | **Authors + implements** |
| Code review | Spot-checks | Reviews | **Owns review** |
| Approving merges to `main` | **Owns** (final human gate) | — | Recommends |
| Numbers / risk thresholds | **Owns** (sole approver) | Proposes | Flags implementability |
| Documentation / data dictionary | Approves | Contributes | **Owns** |
| Technical decisions | Final say | Proposes | Proposes, reviews |

Two AIs never edit the same file simultaneously. Coordination is **artifact-mediated**:
the repo, PRs, and ADRs are the shared memory — not chat.

## 2. Branch strategy (trunk-based)
- `main` is always releasable and **protected** (no direct pushes).
- Short-lived branches: `feat/<topic>`, `fix/<topic>`, `chore/<topic>`.
- Rebase/merge frequently; keep branches < a few days old.

## 3. Commits (Conventional Commits)
`type(scope): summary` — types: `feat, fix, refactor, test, docs, chore, ci`.
Small, atomic commits. Reference ADR ids when a commit embodies a decision.

## 4. Pull requests
- One logical change per PR; keep them small and reviewable.
- PR description: what changed, why, ADR refs, test evidence.
- **CI must be green** (pytest + ruff + mypy) before review.
- **≥1 human approval (Luis) required to merge.** AI approvals are advisory.
- Squash-merge to keep `main` history clean.

## 5. Code review checklist
- Consistency with Constitution + ARES-015 (Data Dictionary).
- Traceability: numbers sourced; decisions link to ADRs.
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
