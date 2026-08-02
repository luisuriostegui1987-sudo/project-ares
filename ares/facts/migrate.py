"""Official ARES migration runner — deployment entry point.

Used by Render's preDeployCommand (`python -m ares.facts.migrate`) so
migrations 0001+ apply BEFORE a new application version receives traffic.

Properties:
- idempotent and concurrency-safe (the shared advisory-locked runner);
- exits non-zero on ANY failure, aborting the deployment;
- NEVER runs down migrations;
- output names migrations only — the DSN and connection details are never
  printed, even on failure.
"""

from __future__ import annotations

import os
import sys


def main() -> int:
    dsn = os.environ.get("ARES_PG_DSN")
    if not dsn:
        print("error: ARES_PG_DSN is not set; refusing to guess a database.", file=sys.stderr)
        return 1
    try:
        import psycopg

        from ares.facts.postgres import apply_migrations

        with psycopg.connect(dsn) as conn:
            applied = apply_migrations(conn)
    except Exception as exc:  # noqa: BLE001 - deploy must abort on ANY failure
        # Exception text may embed hostnames/usernames; never print it.
        print(
            f"error: migration failed ({type(exc).__name__}); deployment must abort. "
            "Inspect the database dashboard for details.",
            file=sys.stderr,
        )
        return 1
    print(f"migrations applied: {applied}" if applied else "migrations: up to date")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
