-- Reversal of 0002_research_reports.sql. Destroys stored reports — run only
-- with explicit human authorization. (ares_reject_mutation() belongs to 0001
-- and is intentionally not dropped here.)

DROP TRIGGER IF EXISTS reports_append_only ON research_reports;
DROP TABLE IF EXISTS research_reports;
DELETE FROM schema_migrations WHERE version = '0002_research_reports.sql';
