-- Enable TimescaleDB
CREATE EXTENSION IF NOT EXISTS timescaledb;

-- USERS TABLE
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- REALTIME DATA TABLE
CREATE TABLE realtime_data (
    timestamp TIMESTAMPTZ NOT NULL,
    plant_id INTEGER NOT NULL,
    frequency DOUBLE PRECISION,
    generation DOUBLE PRECISION,
    schedule DOUBLE PRECISION,
    deviation DOUBLE PRECISION
);

-- Convert realtime_data into Timescale hypertable
SELECT create_hypertable('realtime_data', 'timestamp');

-- DSM RECORDS TABLE
CREATE TABLE DSM_records (
    timestamp TIMESTAMPTZ NOT NULL,
    plant_id INTEGER NOT NULL,
    schedule DOUBLE PRECISION,
    actual DOUBLE PRECISION,
    deviation DOUBLE PRECISION,
    penalty DOUBLE PRECISION
);
