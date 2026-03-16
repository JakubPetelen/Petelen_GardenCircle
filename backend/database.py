import os
import sqlite3
from flask import g


def _default_db_path() -> str:
    # Vercel's filesystem is read-only except for /tmp.
    if os.environ.get("VERCEL"):
        return os.path.join("/tmp", "gardencircle.db")
    return os.path.join(os.path.dirname(__file__), "gardencircle.db")


DB_PATH = os.environ.get("DB_PATH", _default_db_path())


def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
        db = g._database = sqlite3.connect(DB_PATH)
        db.row_factory = sqlite3.Row

        # Enable pragmatic performance tweaks for SQLite.
        # These are safe for a single-writer, low-concurrency app like this.
        try:
            db.execute("PRAGMA journal_mode=WAL;")
            db.execute("PRAGMA synchronous=NORMAL;")
            db.execute("PRAGMA foreign_keys=ON;")
            db.execute("PRAGMA cache_size=-8000;")  # ~8MB cache
        except Exception:
            # If any pragma fails (e.g. on older SQLite), just continue.
            pass
    return db


def close_db(e=None):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()
        g._database = None


