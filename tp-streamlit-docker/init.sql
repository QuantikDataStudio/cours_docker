CREATE TABLE IF NOT EXISTS analyses (
    id SERIAL PRIMARY KEY,
    filename TEXT NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    report_path TEXT NOT NULL
)