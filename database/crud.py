"""
crud.py
~~~~~~~~
Database module for all CRUD operations
"""

from config import engine
import models
from sqlalchemy.orm import Session
from sqlalchemy import insert
from sqlalchemy.exc import SQLAlchemyError


def bulk_db_write(data):
    with Session(engine) as session, session.begin():
        session.execute(insert(models.Champion), data)
