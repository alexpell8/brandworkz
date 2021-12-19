from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers

from src.config import Config
from src.orm_layer.map_db import metadata, map_models

engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
engine = metadata.create_all(engine)

class Transaction:
    def __init__(self) -> None:
        map_models()
        self.session_maker = sessionmaker(bind=engine)

    def __enter__(self):
        """
        Set-up for context manager.
        """
        self.session = self.session_maker()
    
    def __exit__(self, *args):
        """
        Tear down for context manager
        """
        self.session.rollback()
        self.session.close()
        clear_mappers()
    
    def commit(self):
        self.session.commit()
    
    def rollback(self):
        self.session.rollback()