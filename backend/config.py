import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # ── Database ──────────────────────────────────────────────
    # Uses PostgreSQL if DATABASE_URL is set, otherwise SQLite fallback
    _db_url = os.getenv('DATABASE_URL')
    
    if not _db_url:
        # SQLite fallback for quick development (no PostgreSQL needed)
        _sqlite_path = os.path.join(os.path.dirname(__file__), 'student_predictor.db')
        SQLALCHEMY_DATABASE_URI = f'sqlite:///{_sqlite_path}'
        print("[INFO] Using SQLite database (no DATABASE_URL set).")
        print(f"[INFO] DB path: {_sqlite_path}")
    else:
        SQLALCHEMY_DATABASE_URI = _db_url

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # ── Flask ─────────────────────────────────────────────────
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = os.getenv('FLASK_DEBUG', 'True') == 'True'

    # ── ML model paths ────────────────────────────────────────
    MODELS_DIR = os.path.join(os.path.dirname(__file__), 'saved_models')
