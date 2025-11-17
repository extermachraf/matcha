from sqlalchemy import create_engine, text
from flask import current_app


def get_db_engine():
    """Create and return a SQLAlchemy engine using the DATABASE_URL from config."""
    db_uri = current_app.config.get('DATABASE_URL')
    if not db_uri:
        raise ValueError("DATABASE_URL is not set in the application configuration.")
    engine = create_engine(db_uri)
    return engine