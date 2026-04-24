-- 1. CLEANUP: Drop everything existing to start fresh
DROP VIEW IF EXISTS v_glucose_audit CASCADE;
DROP VIEW IF EXISTS v_glucose_daily_avg CASCADE;
DROP VIEW IF EXISTS v_today_glucose_records CASCADE;
DROP VIEW IF EXISTS v_active_glucose_records CASCADE;
DROP TABLE IF EXISTS glucose_audit_logs CASCADE;
DROP TABLE IF EXISTS glucose_records CASCADE;
DROP TABLE IF EXISTS users CASCADE;

-- 2. USERS TABLE
CREATE TABLE users (
  id              BIGSERIAL     PRIMARY KEY, -- Changed to BIGINT
  email           VARCHAR(255)  NOT NULL UNIQUE,
  display_name    VARCHAR(100),
  three_word_tag  VARCHAR(60)   CHECK (
                    three_word_tag IS NULL OR 
                    three_word_tag ~ '^[a-zA-Z]+-[a-zA-Z]+-[a-zA-Z]+$'
                  ),
  created_at      TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
  updated_at      TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
  is_deleted      BOOLEAN       NOT NULL DEFAULT FALSE
);

-- 3. GLUCOSE RECORDS TABLE
CREATE TABLE glucose_records (
  id              BIGSERIAL     PRIMARY KEY, -- Changed to BIGINT
  user_id         BIGINT        NOT NULL REFERENCES users(id), -- Matches BIGINT
  value           DECIMAL(5,2)  NOT NULL,
  meal_context    VARCHAR(20)   CHECK (meal_context IN ('fasting', 'before', 'after')),
  note            TEXT,
  status_label    VARCHAR(20),  -- e.g., 'In Range', 'High'
  three_word_tag  VARCHAR(60),
  recorded_at     TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
  created_at      TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
  updated_at      TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
  is_deleted      BOOLEAN       NOT NULL DEFAULT FALSE
);

-- 4. AUDIT LOGS TABLE
CREATE TABLE glucose_audit_logs (
  id              BIGSERIAL     PRIMARY KEY, -- Changed to BIGINT
  record_id       BIGINT        NOT NULL REFERENCES glucose_records(id), -- Matches BIGINT
  user_id         BIGINT        NOT NULL REFERENCES users(id), -- Matches BIGINT
  changed_field   VARCHAR(50)   NOT NULL,
  old_value       TEXT,
  new_value       TEXT,
  changed_at      TIMESTAMPTZ   NOT NULL DEFAULT NOW()
);

-- 5. VIEWS (Rebuilt with new types)

-- Active records with User Names
CREATE OR REPLACE VIEW v_active_glucose_records AS
  SELECT 
    gr.id, gr.user_id, gr.value, gr.meal_context, gr.note, 
    gr.status_label, gr.three_word_tag, gr.recorded_at, 
    u.display_name AS user_display_name
  FROM glucose_records gr
  JOIN users u ON u.id = gr.user_id
  WHERE gr.is_deleted = FALSE AND u.is_deleted = FALSE;

-- Today's readings
CREATE OR REPLACE VIEW v_today_glucose_records AS
  SELECT * FROM v_active_glucose_records
  WHERE recorded_at >= CURRENT_DATE;

-- Daily averages
CREATE OR REPLACE VIEW v_glucose_daily_avg AS
  SELECT 
    user_id, 
    DATE(recorded_at) AS reading_date, 
    ROUND(AVG(value), 1) AS avg_value,
    COUNT(*) AS reading_count
  FROM glucose_records
  WHERE is_deleted = FALSE
  GROUP BY user_id, reading_date;