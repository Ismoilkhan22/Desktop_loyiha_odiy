"""3-qadam: bazani yaratish + jadvallar + namuna ma'lumot.
Ishga tushirish:  python -m app.init_db
Qayta ishga tushirsa ham ma'lumotni o'chirmaydi."""
from pathlib import Path

import psycopg2

from . import db
from .config import DB

SQL = Path(__file__).resolve().parent.parent / "sql"


def main():
    # Bazaning o'zi hali yo'q bo'lishi mumkin, shuning uchun avval 'postgres' bazasiga ulanamiz.
    admin = psycopg2.connect(**{**DB, "dbname": "postgres"})
    admin.autocommit = True  # CREATE DATABASE tranzaksiya ichida ishlamaydi
    with admin.cursor() as cur:
        cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (DB["dbname"],))
        if not cur.fetchone():
            cur.execute(f'CREATE DATABASE "{DB["dbname"]}"')
            print("Baza yaratildi:", DB["dbname"])
    admin.close()

    db.execute((SQL / "schema.sql").read_text())
    if db.query("SELECT COUNT(*) FROM faculties")[0][0] == 0:  # namuna faqat bo'sh bazaga
        db.execute((SQL / "seed.sql").read_text())
        print("Namuna ma'lumot qo'shildi")
    print("Tayyor")


if __name__ == "__main__":
    main()
