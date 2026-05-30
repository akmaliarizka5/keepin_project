-- SQL DDL for usaha_db (usaha table)
CREATE TABLE IF NOT EXISTS usaha (
    id_usaha SERIAL PRIMARY KEY,
    id_owner INTEGER,
    nama_usaha VARCHAR(255) NOT NULL,
    alamat TEXT,
    phone VARCHAR(50),
    jumlah_slot INTEGER DEFAULT 1,
    status_verifikasi VARCHAR(50) DEFAULT 'MENUNGGU',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);

ALTER TABLE usaha ADD COLUMN IF NOT EXISTS jumlah_slot INTEGER DEFAULT 1;
ALTER TABLE usaha ADD COLUMN IF NOT EXISTS status_verifikasi VARCHAR(50) DEFAULT 'MENUNGGU';

CREATE INDEX IF NOT EXISTS idx_usaha_owner ON usaha(id_owner);
CREATE INDEX IF NOT EXISTS idx_usaha_status ON usaha(status_verifikasi);
