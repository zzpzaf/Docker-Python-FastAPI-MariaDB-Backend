# app/core/database.py 
# (connection + FastAPI dependency)
#
# Creates a PyMySQL connection per request
# Exposes dependency get_db() that yields conn

from contextlib import contextmanager
import pymysql
from pymysql.cursors import DictCursor
from .config import settings


def _connect():
    return pymysql.connect(
        host=settings.db_host,
        port=settings.db_port,
        user=settings.db_user,
        password=settings.db_password,
        database=settings.db_name,
        charset="utf8mb4",
        cursorclass=DictCursor,   # rows as dicts
        autocommit=True,          # for GET-only it's fine; later we can manage transactions
    )


@contextmanager
def get_conn():
    conn = _connect()
    try:
        yield conn
    finally:
        conn.close()


def get_db():
    """
    FastAPI dependency that yields a live DB connection per request.
    """
    with get_conn() as conn:
        yield conn
