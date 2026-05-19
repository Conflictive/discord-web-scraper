"""
database.crud.py
~~~~~~~~
Database module for all CRUD operations
"""

from database.config import engine
import database.models as models
from sqlalchemy.orm import Session
from sqlalchemy import insert


def bulk_db_write(models_class, data):
    """
    Writes bulk data (lists) to the database

    Args:
        models_class(DeclarativeBase): Class to target the destination table
        data (List[dict]): A list of champion dictionaries containing the following keys:
            - name(str): The champion's name
    """
    with Session(engine) as session, session.begin():
        session.execute(insert(models_class), data)
