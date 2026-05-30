-- SQL DDL for loker_db (loker table)
CREATE TABLE IF NOT EXISTS loker (
    id_loker VARCHAR(100) PRIMARY KEY,
    id_usaha INTEGER,
    tipe_loker VARCHAR(100),
    harga_per_jam NUMERIC(12,2),
    lokasi VARCHAR(255),
    latitude NUMERIC(10,7),
    longitude NUMERIC(10,7),
    status VARCHAR(50) DEFAULT 'READY',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_loker_lokasi ON loker(lokasi);
CREATE INDEX IF NOT EXISTS idx_loker_status ON loker(status);
CREATE INDEX IF NOT EXISTS idx_loker_coordinates ON loker(latitude, longitude);
