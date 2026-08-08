# DF-1 — Sprint 7 Authorization Review Record (Preservation Index)

**Purpose.** This directory closes dependency **DF-1** of the Sprint 7
authorization cycle: the permanent, in-repository preservation of the
institutional review record, so that every CTO/CRO verdict cited by any event,
gate or future order resolves to a preserved artifact with a verifiable
identity (per CR-4, GitHub is the provisional institutional registry; per
CLAUDE.md, "if it isn't preserved in the repository, it doesn't officially
exist").

**Contents.** Eight deposits — four CTO verdicts and four CRO verdicts —
covering the four review stages of the Sprint 7 Authorization Package cycle
(plan review of package `0.4.0`; closure verification of `0.4.1-draft`;
re-verification of the first limited remediation; re-verification of the
second limited remediation, r2). Each file contains a clearly separated
`DEPOSIT METADATA` block (added at deposit time) followed by the original
verdict text between `BEGIN/END ORIGINAL DICTAMEN TEXT` markers. The deposit
metadata is not part of the historical verdicts. **The original texts are the
authoritative record; this index does not reinterpret or replace them.**

**Provenance and verification chain.**

1. **Step 4A/4B** — each authority deposited exclusively its own verdicts
   (CTO from its original session record; CRO from its original session
   record). No authority created, reconstructed or certified the other's
   reports.
2. **Step 5B** — the CTO deposits were authenticated against the CTO's
   original session record (`PASS`).
3. **Step 5C** — an independent CTO check detected that the CRO deposits were
   **not verbatim** against the CRO's primary session record (systematic
   abridgements introduced by manual re-transcription at deposit time):
   `FAIL — DISCREPANCIES DETECTED`.
4. **Step 6A** — the CRO remediated its four deposits by **programmatic
   extraction from the primary source** (its original session JSONL record),
   replacing manual transcription entirely.
5. **Step 6B** — independent CTO verification against the primary source:
   original messages identified unambiguously (exactly one candidate each);
   historical blocks byte-verbatim against the originals; the four
   post-remediation SHA-256 identities reproduced independently. In-place
   confirmation was temporarily blocked by an environmental read denial
   (EB-1).
6. **Step 6C** — after access restoration, direct on-disk `shasum`
   verification: all 8 hashes exact
   (`PASS — EB-1 RESOLVED; ALL 8 DEPOSITS VERIFIED IN PLACE`).
7. **Step 7** — final reconciliation:
   `DF-1 CLOSURE RECOMMENDED — EVIDENCE COMPLETE AND RECONCILED`.

**Final deposit identities.**

| Deposit | Final SHA-256 | Verification status |
|---|---|---|
| CTO-1-PLAN-CONDITIONAL-PASS.md | `40859133285525265f778670713633c441f0fd2a8f0b6b63d2a403d7b72fc848` | Authenticated vs original CTO record (5B); verified in place (6C) |
| CTO-2-CLOSURE-CONDITIONAL-PASS.md | `1d5395b8218e385e81691631b4c092089098894a44eb736d2236fadc81bb6e45` | Authenticated vs original CTO record (5B); verified in place (6C) |
| CTO-3-REMEDIATION-REVERIFICATION-CONDITIONAL-PASS.md | `7e9cf3cab5a125b826b60142557e8d70343d7390bcaa1a158659c16c9b4a2bd3` | Authenticated vs original CTO record (5B); verified in place (6C) |
| CTO-4-SECOND-REMEDIATION-REVERIFICATION-PASS.md | `17a6387f6b62be6660bf3deb3992ead2c23ff7bd6fb89c21bf73bb81c1c8c21d` | Authenticated vs original CTO record (5B); verified in place (6C) |
| CRO-1-PLAN-CONDITIONAL-PASS.md | `68f9b20d1d5f6a663ce13615bb693471d21fadff811c1a42e79b80626dc6faaf` | Byte-verbatim vs primary CRO record (6A/6B); verified in place (6C) |
| CRO-2-CLOSURE-CONDITIONAL-PASS.md | `7b2284a38e4149d7626abe75021d31b7842f0d75bf22ff7005866a8bdc706f42` | Byte-verbatim vs primary CRO record (6A/6B); verified in place (6C) |
| CRO-3-REMEDIATION-REQUIRES-REVISION.md | `1af889a8a5d01562f110e85a322fc132ba373253384dae6bf1157b2018fff90f` | Byte-verbatim vs primary CRO record (6A/6B); verified in place (6C) |
| CRO-4-SECOND-REMEDIATION-REVERIFICATION-PASS.md | `3779a5df1de58c98641fffecc34177597f0d9c47caec4cc791ee818b3b57026e` | Byte-verbatim vs primary CRO record (6A/6B); verified in place (6C) |

**Artifact chain referenced by these verdicts** (identities recorded inside
the deposits): package `0.4.0` = `e19245a4…5c4147a1` · `0.4.1-draft` =
`d6e11b7f…c5b3ee91` · remediated r1 = `ee1759c5…f995f943` · remediated r2 =
`82bb6c52…11715d32` · preserved framework
(`docs/specifications/ARES-ANALYST-FRAMEWORK-001.md`) =
`cac6ad75becd98e3702411c8cdefce64558a9bfeac95251a4217808498711df9`.

**Governance barriers — unchanged by this deposit.** This record preserves
review evidence only. **Phase 5 remains `pending`. Sprint 7 remains
`not started`. The Analyst Framework remains a Preserved Verbatim
Institutional Document ("Research Draft — Pending Institutional Review"),
not activated. The canonical version remains `0.4.0`; no `v0.5.0` tag
exists.** Nothing in this directory authorizes implementation, analyst
research, signals, operations, activation, or any capital action; all
decisions L-1…L-10 remain exclusively with Luis.
