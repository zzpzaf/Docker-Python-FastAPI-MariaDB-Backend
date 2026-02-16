# app/core/database.py 
# (connection + FastAPI dependency)
#
# Creates a PyMySQL connection per request
# Exposes dependency get_db() that yields conn

# 260215: 
#   - Switched to autocommit=False for better transaction management in POST/PUT/PATCH/DELETE routes.
# 260216:
#   - Added automatic commit/rollback logic to ensure INSERT persistence

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
        # autocommit=True,          # for GET-only it's fine; later we can manage transactions
        autocommit=False,  # IMPORTANT for POST/PUT/PATCH/DELETE
    )


@contextmanager
def get_conn():
    """
    Context manager for DB connection with automatic
    commit / rollback handling.
    """
    conn = _connect()
    try:
        yield conn
        conn.commit()          # IMPORTANT: commit after successful use
    except Exception:
        conn.rollback()        # rollback if anything fails
        raise
    finally:
        conn.close()


def get_db():
    """
    FastAPI dependency: yields connection per request.
    Auto commit/rollback handled by get_conn().
    """
    with get_conn() as conn:
        yield conn