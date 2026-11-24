"""1-qadam: baza sozlamalari. Hammasi muhit o'zgaruvchisidan olinadi, bo'lmasa default."""
import getpass
import os

DB = dict(
    host=os.getenv("DB_HOST", "localhost"),
    port=os.getenv("DB_PORT", "5432"),
    dbname=os.getenv("DB_NAME", "talaba_db"),
    user=os.getenv("DB_USER", getpass.getuser()),  # Homebrew PostgreSQL: foydalanuvchi nomi = Mac login
    password=os.getenv("DB_PASSWORD") or None,
)
