-- Reversal of 0001_institutional_facts.sql. Destroys stored records —
-- run only with explicit human authorization (Constitution: append-only data
-- is never dropped casually).

DROP TRIGGER IF EXISTS freshness_events_append_only ON fact_freshness_events;
DROP TRIGGER IF EXISTS validation_events_append_only ON fact_validation_events;
DROP TRIGGER IF EXISTS facts_append_only ON institutional_facts;
DROP FUNCTION IF EXISTS ares_reject_mutation();
DROP TABLE IF EXISTS fact_freshness_events;
DROP TABLE IF EXISTS fact_validation_events;
DROP TABLE IF EXISTS institutional_facts;
DROP TABLE IF EXISTS schema_migrations;
