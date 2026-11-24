"""3-qadam: bazani yaratish + jadvallar + namuna ma'lumot.
Ishga tushirish:  python -m app.init_db
Qayta ishga tushirsa ham ma'lumotni o'chirmaydi."""
from pathlib import Path

import mysql.connector

from . import db
from .config import DB, DB_NAME

SQL = Path(__file__).resolve().parent.parent / "sql"


def run_script(path):
    # Fayl ichidagi har bir buyruq ';' bilan ajratiladi (fayllarda ';' faqat buyruq oxirida)
    for stmt in (SQL / path).read_text().split(";"):
        if stmt.strip():
            db.execute(stmt)


def main():
    # Bazaning o'zi hali yo'q bo'lishi mumkin, shuning uchun avval bazasiz ulanamiz.
    admin = mysql.connector.connect(**DB)
    cur = admin.cursor()
    cur.execute(f"CREATE DATABASE IF NOT EXISTS `{DB_NAME}` CHARACTER SET utf8mb4")
    cur.close()
    admin.close()

    run_script("schema.sql")
    if db.query("SELECT COUNT(*) FROM faculties")[0][0] == 0:  # namuna faqat bo'sh bazaga
        run_script("seed.sql")
        print("Namuna ma'lumot qo'shildi")
    print("Tayyor:", DB_NAME)


if __name__ == "__main__":
    main()
