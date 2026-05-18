import os
import psycopg2
from dotenv import load_dotenv
from psycopg2.extras import RealDictCursor

# Load variabel dari file .env
load_dotenv()

def get_auth_db_conn():
    return psycopg2.connect(
        host=os.getenv("AUTH_DB_HOST"),
        database=os.getenv("AUTH_DB_NAME"),
        user=os.getenv("AUTH_DB_USER"),
        password=os.getenv("AUTH_DB_PASS")
    )

def get_booking_db_conn():
    return psycopg2.connect(
        host=os.getenv("BOOKING_DB_HOST"),
        database=os.getenv("BOOKING_DB_NAME"),
        user=os.getenv("BOOKING_DB_USER"),
        password=os.getenv("BOOKING_DB_PASS")
    )

def get_inventory_db_conn():
    return psycopg2.connect(
        host=os.getenv("INVENTORY_DB_HOST"),
        database=os.getenv("INVENTORY_DB_NAME"),
        user=os.getenv("INVENTORY_DB_USER"),
        password=os.getenv("INVENTORY_DB_PASS")
    )

def get_payment_db_conn():
    return psycopg2.connect(
        host=os.getenv("PAYMENT_DB_HOST"),
        database=os.getenv("PAYMENT_DB_NAME"),
        user=os.getenv("PAYMENT_DB_USER"),
        password=os.getenv("PAYMENT_DB_PASS")
    )

# --- FUNGSI HELPER AGAR UTILITY DI ATAS BISA LANGSUNG PAKAI ---
# Tambahkan ini di bagian paling bawah file database.py kamu

def fetch_one(db_conn_func, query, params=None):
    """Helper untuk mengambil satu data dari fungsi koneksi tertentu"""
    conn = db_conn_func()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute(query, params)
    data = cur.fetchone()
    cur.close()
    conn.close()
    return data

def fetch_all(db_conn_func, query, params=None):
    """Helper untuk mengambil banyak data dari fungsi koneksi tertentu"""
    conn = db_conn_func()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute(query, params)
    data = cur.fetchall()
    cur.close()
    conn.close()
    return data

def execute_query(get_conn_func, query, params=()):
    """Fungsi helper untuk mengeksekusi INSERT, UPDATE, atau DELETE ke database"""
    conn = get_conn_func()
    try:
        cur = conn.cursor()
        cur.execute(query, params)
        conn.commit()
        cur.close()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()