"""2-qadam: bazaga ulanish. Butun dastur faqat query() va execute() orqali SQL yuboradi."""
import mysql.connector

from .config import DB, DB_NAME

_conn = None


def _connection():
    global _conn
    if _conn is None or not _conn.is_connected():
        _conn = mysql.connector.connect(**DB, database=DB_NAME)
    return _conn


def _run(sql, params, fetch):
    c = _connection()
    try:
        cur = c.cursor()
        try:
            cur.execute(sql, params)
            rows = cur.fetchall() if fetch else None
        finally:
            cur.close()
        c.commit()  # INSERT/UPDATE/DELETE shu yerda saqlanadi
        return rows
    except Exception:
        c.rollback()  # xato bo'lsa, o'zgarish bekor qilinadi
        raise


def query(sql, params=()):
    """SELECT: qatorlar ro'yxatini qaytaradi."""
    return _run(sql, params, True)


def execute(sql, params=()):
    """INSERT / UPDATE / DELETE."""
    _run(sql, params, False)
