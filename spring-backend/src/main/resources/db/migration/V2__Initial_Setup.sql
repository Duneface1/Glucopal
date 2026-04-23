DROP VIEW IF EXISTS your_glucose_view_name;

ALTER TABLE glucose_records ALTER COLUMN id SET DATA TYPE bigint;

CREATE VIEW your_glucose_view_name AS
SELECT ... FROM glucose_records;