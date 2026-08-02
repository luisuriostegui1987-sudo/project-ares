-- Research report persistence — migration 0002 (Sprint 4).
-- Same hardening pattern as 0001: canonical JSONB record, indexed projections
-- guaranteed by CHECK constraints, append-only enforced by trigger.
-- Reversible via 0002_research_reports_down.sql.

CREATE TABLE IF NOT EXISTS research_reports (
    report_id        TEXT PRIMARY KEY,
    entity_id        TEXT        NOT NULL,
    data_mode        TEXT        NOT NULL,
    pipeline_version TEXT        NOT NULL,
    generated_at     TIMESTAMPTZ NOT NULL,
    record           JSONB       NOT NULL,
    CONSTRAINT chk_report_id_matches_record CHECK (report_id = record ->> 'report_id'),
    CONSTRAINT chk_report_entity_matches_record CHECK (
        entity_id = record -> 'entity' ->> 'entity_id'
    ),
    CONSTRAINT chk_report_data_mode_matches_record CHECK (data_mode = record ->> 'data_mode'),
    CONSTRAINT chk_report_version_matches_record CHECK (
        pipeline_version = record ->> 'pipeline_version'
    ),
    CONSTRAINT chk_report_generated_matches_record CHECK (
        generated_at = (record ->> 'generated_at')::timestamptz
    )
);

CREATE INDEX IF NOT EXISTS idx_reports_entity ON research_reports (entity_id);
CREATE INDEX IF NOT EXISTS idx_reports_generated_at ON research_reports (generated_at);

DROP TRIGGER IF EXISTS reports_append_only ON research_reports;
CREATE TRIGGER reports_append_only
    BEFORE UPDATE OR DELETE ON research_reports
    FOR EACH ROW EXECUTE FUNCTION ares_reject_mutation();
