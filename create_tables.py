import os
from pathlib import Path
import psycopg2

BASE_DIR = Path(__file__).resolve().parent
ENV_PATH = BASE_DIR / ".env"
EXAMPLE_ENV_PATH = BASE_DIR / ".env.example"

if ENV_PATH.exists():
    path = ENV_PATH
elif EXAMPLE_ENV_PATH.exists():
    path = EXAMPLE_ENV_PATH
else:
    raise FileNotFoundError("Neither .env nor .env.example was found in the project root.")

with path.open("r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip())

DBS = [
    ("AUTH_DB_NAME", "sql/auth_db.sql"),
    ("BOOKING_DB_NAME", "sql/booking_db.sql"),
    ("LOKER_DB_NAME", "sql/loker_db.sql"),
    ("USAHA_DB_NAME", "sql/usaha_db.sql"),
    ("PAYMENT_DB_NAME", "sql/payment_db.sql"),
]


def get_setting(key: str, default: str):
    return os.getenv(key, default)


def execute_sql(db_key: str, sql_path: Path):
    sql_text = sql_path.read_text(encoding="utf-8")
    prefix = db_key.replace("_NAME", "")
    conn = psycopg2.connect(
        host=get_setting(f"{prefix}_HOST", "localhost"),
        database=get_setting(db_key, None),
        user=get_setting(f"{prefix}_USER", "postgres"),
        password=get_setting(f"{prefix}_PASS", ""),
    )
    conn.autocommit = True
    with conn.cursor() as cur:
        cur.execute(sql_text)
    conn.close()


def main():
    print("Creating tables from SQL files...")
    for db_key, relative_sql in DBS:
        db_name = os.getenv(db_key)
        if not db_name:
            raise ValueError(f"Environment variable {db_key} is missing.")
        sql_path = BASE_DIR / relative_sql
        if not sql_path.exists():
            raise FileNotFoundError(f"SQL file not found: {sql_path}")

        print(f"- {db_key} -> {db_name}: {sql_path}")
        execute_sql(db_key, sql_path)
        print(f"  Created tables in {db_name}")

    print("All schema files executed successfully.")


if __name__ == "__main__":
    main()
