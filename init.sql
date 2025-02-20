CREATE TABLE IF NOT EXISTS sensor_metrics (
    id SERIAL PRIMARY KEY,
    device_id VARCHAR(255) NOT NULL,
    temperature_f FLOAT NOT NULL,
    pressure_psi FLOAT NOT NULL,
    timestamp TIMESTAMP NOT NULL
); 