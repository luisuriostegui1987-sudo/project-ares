---
id: ARES-SPEC-GOVERNANCE
title: Research governance
status: Active (CTO and CRO reviews passed; merged to main with Luis's authorization)
version: 0.1.0
owner: CKO
governance: change only via pull request; merge only with Luis's authorization
---

# Research governance

## Roles

| Role | Responsibility |
|---|---|
| CKO | Defines and owns methodology; designs the Knowledge Library |
| Implementation/publishing engineer | Materializes structure, validates, publishes branches and PRs |
| CTO | Reviews architecture and structure |
| CRO | Reviews methodology and epistemics |
| Luis | Authorizes every merge and every research start; makes every capital decision |

## Flow

CKO defines methodology → engineer materializes and publishes → CTO reviews
architecture → CRO reviews methodology → **Luis authorizes merge**.

## Gates

1. **Research gate**: per-analyst research begins only on Luis's explicit,
   named authorization (ARES-ANALYST-001 §1).
2. **Merge gate**: nothing merges to `main` without Luis's authorization.
3. **Capital gate**: no artifact in this library is investment advice; ARES
   never decides or allocates capital.

## Change control

All changes via pull request with green CI. Documents follow the
Draft → Reviewed → Active → Superseded lifecycle; nothing is deleted.
