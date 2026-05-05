-- ============================================================
--  Student Performance Predictor — PostgreSQL Schema
-- ============================================================

-- Create database (run separately if needed)
-- CREATE DATABASE student_db;

-- Drop tables if they exist (for clean re-run)
DROP TABLE IF EXISTS predictions CASCADE;
DROP TABLE IF EXISTS students CASCADE;

-- ─────────────────────────────────────────
--  Students Table
-- ─────────────────────────────────────────
CREATE TABLE students (
    id          SERIAL PRIMARY KEY,
    name        VARCHAR(100)        NOT NULL,
    email       VARCHAR(150)        UNIQUE,
    created_at  TIMESTAMP           DEFAULT CURRENT_TIMESTAMP
);

-- ─────────────────────────────────────────
--  Predictions Table
-- ─────────────────────────────────────────
CREATE TABLE predictions (
    id                  SERIAL PRIMARY KEY,
    student_id          INT             REFERENCES students(id) ON DELETE SET NULL,
    student_name        VARCHAR(100),
    study_hours         FLOAT           NOT NULL CHECK (study_hours >= 0 AND study_hours <= 24),
    attendance          FLOAT           NOT NULL CHECK (attendance >= 0 AND attendance <= 100),
    sleep_hours         FLOAT           NOT NULL CHECK (sleep_hours >= 0 AND sleep_hours <= 24),
    previous_score      FLOAT           NOT NULL CHECK (previous_score >= 0 AND previous_score <= 100),
    extra_curricular    BOOLEAN         DEFAULT FALSE,
    model_used          VARCHAR(30)     NOT NULL DEFAULT 'random_forest',
    predicted_score     FLOAT           NOT NULL,
    performance_grade   VARCHAR(2),
    created_at          TIMESTAMP       DEFAULT CURRENT_TIMESTAMP
);

-- ─────────────────────────────────────────
--  Indexes
-- ─────────────────────────────────────────
CREATE INDEX idx_predictions_created_at ON predictions(created_at DESC);
CREATE INDEX idx_predictions_model      ON predictions(model_used);
CREATE INDEX idx_predictions_student    ON predictions(student_id);

-- ─────────────────────────────────────────
--  Sample seed data (optional)
-- ─────────────────────────────────────────
INSERT INTO students (name, email) VALUES
    ('Alice Johnson',  'alice@example.com'),
    ('Bob Smith',      'bob@example.com'),
    ('Carol White',    'carol@example.com');
