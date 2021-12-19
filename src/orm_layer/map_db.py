"""
Contains the file meta data mapping to the database schema using the SQLAlchemy mapper.
"""
from sqlalchemy.orm import mapper
from sqlalchemy import Column, String, Integer, Date, Table, MetaData

from src.domain.models import FileMetaData

metadata = MetaData()

meta_data = Table(
    'meta_data', metadata,
    Column('extr_id', Integer, primary_key=True, autoincrement=True),
    Column('date_created', Date),
    Column('date_modified', Date),
    Column('file_path', String(256)),
    Column('file_name', String(64)),
    Column('file_ext', String(32)),
    Column('file_type', String(32))
)

def map_models():
    mapped_models = mapper(FileMetaData, meta_data)