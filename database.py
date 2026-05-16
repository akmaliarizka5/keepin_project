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