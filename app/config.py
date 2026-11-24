"""1-qadam: baza sozlamalari. Hammasi muhit o'zgaruvchisidan olinadi, bo'lmasa default."""
import os

DB = dict(
    host=os.getenv("DB_HOST", "localhost"),
    port=int(os.getenv("DB_PORT", "3306")),
    user=os.getenv("DB_USER", "root"),
    password=os.getenv("DB_PASSWORD", ""),
)
DB_NAME = os.getenv("DB_NAME", "talaba_db")
