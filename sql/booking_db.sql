-- SQL DDL for booking_db (booking table)
CREATE TABLE IF NOT EXISTS booking (
    id_booking SERIAL PRIMARY KEY,
    id_user INTEGER NOT NULL,
    id_loker VARCHAR(100) NOT NULL,
    nama_tempat VARCHAR(255),
    durasi_sewa INTEGER NOT NULL,
    total_biaya NUMERIC(12,2) NOT NULL,
    status_booking VARCHAR(50) DEFAULT 'PENDING',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_booking_user ON booking(id_user);
CREATE INDEX IF NOT EXISTS idx_booking_status ON booking(status_booking);
