"""Configures the URL for the PostgreSQL database.

Recreates the db url using .env variables.
"""

import os
import urllib.parse

from dotenv import load_dotenv

load_dotenv()

db_url = os.environ.get("DB_URL")
db_user = os.environ.get("DB_USER")
db_pass = os.environ.get("DB_PASS")
db_pass = urllib.parse.quote_plus(db_pass)

DATABASE_URL = f"postgresql+asyncpg://{db_user}:{db_pass}@{db_url}"
