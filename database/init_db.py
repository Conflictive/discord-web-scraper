"""
init_db.py
~~~~~~~~~~~
Script to generate database tables

Dependencies:
    - models: Defines SQLAlchemy ORM models.
    - config: Provides Base and engine used to create tables.
"""

import models
from config import Base, engine

print("Creating database tables")
Base.metadata.create_all(bind=engine)
print("Done!")
