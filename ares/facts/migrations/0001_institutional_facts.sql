-- ARES-FACT-001 persistent store — migration 0001 (v0.3.0).
-- The InstitutionalFact contract lives in ares/models/ifact.py; this schema
-- stores the canonical JSON record verbatim plus indexed identity columns.
-- Nothing here alters the contract. Reversible via 0001_institutional_facts_down.sql.

CREATE TABLE IF NOT EXISTS institutional_facts (
    fact_id            TEXT PRIMARY KEY,
    fact_key           TEXT        NOT NULL,
    content_hash       TEXT        NOT NULL UNIQUE,
    supersedes_fact_id TEXT        REFERENCES institutional_facts (fact_id),
    retrieved_at       TIMESTAMPTZ NOT NULL,
    record             JSONB       NOT NULL,
    -- The JSONB record is canonical; the indexed columns are projections of
    -- it and the DATABASE guarantees they can never diverge (a direct SQL
    -- insert with mismatched columns is rejected).
    CONSTRAINT chk_fact_id_matches_record CHECK (fact_id = record ->> 'fact_id'),
    CONSTRAINT chk_fact_key_matches_record CHECK (fact_key = record ->> 'fact_key'),
    CONSTRAINT chk_content_hash_matches_record CHECK (content_hash = record ->> 'content_hash'),
    CONSTRAINT chk_supersedes_matches_record CHECK (
        supersedes_fact_id IS NOT DISTINCT FROM record ->> 'supersedes_fact_id'
    ),
    CONSTRAINT chk_retrieved_at_matches_record CHECK (
        retrieved_at = (record ->> 'retrieved_at')::timestamptz
    )
);

CREATE INDEX IF NOT EXISTS idx_facts_fact_key ON institutional_facts (fact_key);
CREATE INDEX IF NOT EXISTS idx_facts_retrieved_at ON institutional_facts (retrieved_at);
CREATE INDEX IF NOT EXISTS idx_facts_supersedes ON institutional_facts (supersedes_fact_id);

-- event_seq is a database-internal, monotonically increasing insertion-order
-- tie-breaker for equal occurred_at timestamps. It is NOT part of the public
-- ARES-FACT-001 event model; event_id remains the public identity.
CREATE TABLE IF NOT EXISTS fact_validation_events (
    event_seq   BIGINT GENERATED ALWAYS AS IDENTITY,
    event_id    TEXT PRIMARY KEY,
    fact_id     TEXT        NOT NULL REFERENCES institutional_facts (fact_id),
    status      TEXT        NOT NULL,
    reason      TEXT        NOT NULL DEFAULT '',
    occurred_at TIMESTAMPTZ NOT NULL,
    recorded_by TEXT        NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_validation_events_fact
    ON fact_validation_events (fact_id, occurred_at, event_seq);

CREATE TABLE IF NOT EXISTS fact_freshness_events (
    event_seq   BIGINT GENERATED ALWAYS AS IDENTITY,
    event_id    TEXT PRIMARY KEY,
    fact_id     TEXT        NOT NULL REFERENCES institutional_facts (fact_id),
    status      TEXT        NOT NULL,
    reason      TEXT        NOT NULL DEFAULT '',
    occurred_at TIMESTAMPTZ NOT NULL,
    recorded_by TEXT        NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_freshness_events_fact
    ON fact_freshness_events (fact_id, occurred_at, event_seq);

-- Append-only is enforced by the DATABASE, not just the repository code:
-- any UPDATE or DELETE on facts or status events raises.
CREATE OR REPLACE FUNCTION ares_reject_mutation() RETURNS trigger AS $$
BEGIN
    RAISE EXCEPTION 'ARES-FACT-001: % on % is forbidden (append-only)', TG_OP, TG_TABLE_NAME;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS facts_append_only ON institutional_facts;
CREATE TRIGGER facts_append_only
    BEFORE UPDATE OR DELETE ON institutional_facts
    FOR EACH ROW EXECUTE FUNCTION ares_reject_mutation();

DROP TRIGGER IF EXISTS validation_events_append_only ON fact_validation_events;
CREATE TRIGGER validation_events_append_only
    BEFORE UPDATE OR DELETE ON fact_validation_events
    FOR EACH ROW EXECUTE FUNCTION ares_reject_mutation();

DROP TRIGGER IF EXISTS freshness_events_append_only ON fact_freshness_events;
CREATE TRIGGER freshness_events_append_only
    BEFORE UPDATE OR DELETE ON fact_freshness_events
    FOR EACH ROW EXECUTE FUNCTION ares_reject_mutation();
