"""
Database configuration.

Default: a local SQLite file (recruitment.db) — zero setup required.
If you want PostgreSQL (as listed in the tech stack), set DATABASE_URL
in your .env file, e.g.:

    DATABASE_URL=postgresql+psycopg2://postgres:postgres@localhost:5432/recruitment

and make sure a Postgres server is running with a database called
"recruitment". The code itself does not change either way.
"""

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./recruitment.db")

connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    # Import models so they register on Base before creating tables
    import models  # noqa: F401
    Base.metadata.create_all(bind=engine)
