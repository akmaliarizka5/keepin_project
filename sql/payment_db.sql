-- SQL DDL for payment_db (payments table)
CREATE TABLE IF NOT EXISTS payments (
    id_payment SERIAL PRIMARY KEY,
    booking_id INTEGER,
    amount NUMERIC(12,2) NOT NULL,
    method VARCHAR(100),
    status VARCHAR(50) DEFAULT 'PENDING',
    reference VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_payments_booking ON payments(booking_id);
