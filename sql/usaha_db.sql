-- SQL DDL for usaha_db (usaha table)
CREATE TABLE IF NOT EXISTS usaha (
    id_usaha SERIAL PRIMARY KEY,
    id_owner INTEGER,
    nama_usaha VARCHAR(255) NOT NULL,
    alamat TEXT,
    phone VARCHAR(50),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_usaha_owner ON usaha(id_owner);
