"""2-qadam: bazaga ulanish. Butun dastur faqat query() va execute() orqali SQL yuboradi."""
import psycopg2

from .config import DB

_conn = None


def _connection():
    global _conn
    if _conn is None or _conn.closed:
        _conn = psycopg2.connect(**DB)
    return _conn


def _run(sql, params, fetch):
    c = _connection()
    try:
        with c.cursor() as cur:
            cur.execute(sql, params)
            rows = cur.fetchall() if fetch else None
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
