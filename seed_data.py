from pathlib import Path

import bcrypt

from database import (
    execute_query,
    fetch_one,
    get_auth_db_conn,
    get_booking_db_conn,
    get_loker_db_conn,
    get_payment_db_conn,
    get_usaha_db_conn,
)


BASE_DIR = Path(__file__).resolve().parent


def hashed(password):
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def seed_auth():
    query = """
        INSERT INTO users (nama_lengkap, email, no_telp, hashed_password, role)
        VALUES
            ('Andi Penyewa', 'andi@keepin.example.com', '0811111111', %s, 'Penyewa'),
            ('Maya Mitra', 'maya@keepin.example.com', '0822222222', %s, 'Mitra'),
            ('Admin KeepIn', 'admin@keepin.example.com', '0833333333', %s, 'Admin')
        ON CONFLICT (email) DO UPDATE SET
            nama_lengkap = EXCLUDED.nama_lengkap,
            no_telp = EXCLUDED.no_telp,
            hashed_password = EXCLUDED.hashed_password,
            role = EXCLUDED.role;
    """
    execute_query(get_auth_db_conn, query, (hashed("password123"), hashed("password123"), hashed("admin123")))
    penyewa = fetch_one(get_auth_db_conn, "SELECT id_user FROM users WHERE email = %s", ("andi@keepin.example.com",))
    mitra = fetch_one(get_auth_db_conn, "SELECT id_user FROM users WHERE email = %s", ("maya@keepin.example.com",))
    return penyewa["id_user"], mitra["id_user"]


def seed_loker():
    sql_text = (BASE_DIR / "sql" / "seed_loker.sql").read_text(encoding="utf-8")
    execute_query(get_loker_db_conn, sql_text)


def seed_usaha(mitra_id):
    query = """
        INSERT INTO usaha (id_usaha, id_owner, nama_usaha, alamat, phone, jumlah_slot, status_verifikasi)
        VALUES
            (1, %s, 'KeepIn Malioboro Hub', 'Malioboro Mall, Yogyakarta', '0274-111111', 24, 'TERVERIFIKASI'),
            (2, %s, 'KeepIn Ambarrukmo Hub', 'Ambarrukmo Plaza, Yogyakarta', '0274-222222', 18, 'TERVERIFIKASI'),
            (3, %s, 'KeepIn Jogja City Hub', 'Jogja City Mall, Yogyakarta', '0274-333333', 16, 'MENUNGGU')
        ON CONFLICT (id_usaha) DO UPDATE SET
            id_owner = EXCLUDED.id_owner,
            nama_usaha = EXCLUDED.nama_usaha,
            alamat = EXCLUDED.alamat,
            phone = EXCLUDED.phone,
            jumlah_slot = EXCLUDED.jumlah_slot,
            status_verifikasi = EXCLUDED.status_verifikasi;
        SELECT setval('usaha_id_usaha_seq', GREATEST((SELECT MAX(id_usaha) FROM usaha), 1));
    """
    execute_query(get_usaha_db_conn, query, (mitra_id, mitra_id, mitra_id))


def seed_booking(penyewa_id):
    query = """
        INSERT INTO booking (id_booking, id_user, id_loker, nama_tempat, durasi_sewa, satuan_durasi, total_biaya, status_booking, metode_bayar)
        VALUES
            (1, %s, 'MALIO-A01', 'Malioboro Mall, Yogyakarta', 3, 'JAM', 24000, 'PAID', 'QRIS'),
            (2, %s, 'AMPLAZ-B01', 'Ambarrukmo Plaza, Yogyakarta', 2, 'JAM', 18000, 'PENDING', 'QRIS')
        ON CONFLICT (id_booking) DO UPDATE SET
            id_user = EXCLUDED.id_user,
            id_loker = EXCLUDED.id_loker,
            nama_tempat = EXCLUDED.nama_tempat,
            durasi_sewa = EXCLUDED.durasi_sewa,
            satuan_durasi = EXCLUDED.satuan_durasi,
            total_biaya = EXCLUDED.total_biaya,
            status_booking = EXCLUDED.status_booking,
            metode_bayar = EXCLUDED.metode_bayar;
        SELECT setval('booking_id_booking_seq', GREATEST((SELECT MAX(id_booking) FROM booking), 1));
    """
    execute_query(get_booking_db_conn, query, (penyewa_id, penyewa_id))


def seed_payment():
    query = """
        INSERT INTO payments (id_payment, booking_id, amount, method, status, reference)
        VALUES
            (1, 1, 24000, 'QRIS', 'PAID', 'KEEPIN-PAY-00001'),
            (2, 2, 18000, 'QRIS', 'PENDING', 'KEEPIN-PAY-00002')
        ON CONFLICT (id_payment) DO UPDATE SET
            booking_id = EXCLUDED.booking_id,
            amount = EXCLUDED.amount,
            method = EXCLUDED.method,
            status = EXCLUDED.status,
            reference = EXCLUDED.reference;
        SELECT setval('payments_id_payment_seq', GREATEST((SELECT MAX(id_payment) FROM payments), 1));
    """
    execute_query(get_payment_db_conn, query)


def main():
    penyewa_id, mitra_id = seed_auth()
    seed_loker()
    seed_usaha(mitra_id)
    seed_booking(penyewa_id)
    seed_payment()
    print("Seed data inserted successfully.")
    print("Demo penyewa: andi@keepin.example.com / password123")
    print("Demo mitra: maya@keepin.example.com / password123")
    print("Demo admin: admin@keepin.example.com / admin123")


if __name__ == "__main__":
    main()
