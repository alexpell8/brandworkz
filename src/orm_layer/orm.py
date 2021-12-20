"""
Contains the file meta data mapping to the database schema using the SQLAlchemy mapper.

Also provides a get_session helper function to provide a scoped session to the orm_layer.Transaction.

SQL Alchemy is used as a database agnostic ORM as an abstraction of an SQLite database.
"""
from sqlalchemy import create_engine, Column, String, Integer, Date, Table, MetaData
from sqlalchemy.orm import registry, scoped_session, sessionmaker, clear_mappers

from src.domain.models import FileMetaData
from src.config import Config

mapper_registry = registry()
metadata_obj = MetaData()

meta_data = Table(
    'meta_data', metadata_obj,
    Column('extr_id', Integer, primary_key=True, autoincrement=True),
    Column('date_created', Date),
    Column('date_modified', Date),
    Column('file_path', String(256)),
    Column('file_name', String(64)),
    Column('file_ext', String(32)),
    Column('file_type', String(32)),
)

def start_mappers():
    """
    A helper function to map interatively the domain model class to the DB Table.
    """
    mapper_registry.map_imperatively(FileMetaData, meta_data)

def get_session():
    """
    A helper function to provide a new DB session to a Transaction.

    Returns:
        scoped_session
    """
    clear_mappers()
    start_mappers()
    engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
    return scoped_session(sessionmaker(bind=engine))

class Transaction:
    def __init__(self, session=get_session) -> None:
        self.session_maker = session

    def __enter__(self):
        """
        Set-up for context manager.
        """
        self.session = self.session_maker()
    
    def __exit__(self, *args):
        """
        Tear down for context manager.

        The call to rollback will not have any effect if a commit has taken place.
        This implementation is fail-safe.
        """
        self.session.rollback()
        self.session.close()
    
    def commit(self):
        """
        Commit/persist the changes to the Database.
        """
        self.session.commit()
    
    def rollback(self):
        """
        Rollback the changes on error to maintain database integrity.
        """
        self.session.rollback()