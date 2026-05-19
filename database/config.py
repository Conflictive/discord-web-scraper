"""
database.config.py
~~~~~~~~~~~~~~~~
This module is for setting up and configuring the connection to the PostgreSQL database

Dependencies:
    - urllib: For parsing unsupported characters in the db password
    - os, dotenv: For loading environment variables from .env files
    - psycopg2: PostgreSQL adapter for Python
    - sqlalchemy: ORM and SQL toolkit
"""

import os
import urllib.parse
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

load_dotenv()

db_url = os.environ.get("DB_URL")
db_user = os.environ.get("DB_USER")
db_pass = os.environ.get("DB_PASS")
db_pass = urllib.parse.quote_plus(db_pass)

DATABASE_URL = f"postgresql+psycopg2://{db_user}:{db_pass}@{db_url}"

engine = create_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


if __name__ == "__main__":
    try:
        with engine.connect() as connection:
            print("Successfully connected to the database!")
    except Exception as e:
        print(f"Connection failed: {e}")
