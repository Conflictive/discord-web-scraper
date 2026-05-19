"""
database.init_db.py
~~~~~~~~~~~
Script to generate database tables

Dependencies:
    - models: Defines SQLAlchemy ORM models.
    - config: Provides Base and engine used to create tables.
"""

import database.models
from database.config import Base, engine

if __name__ == "__main__":
    print("Creating database tables")
    Base.metadata.create_all(bind=engine)
    print("Done!")
