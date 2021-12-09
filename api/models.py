"""
Contains the schema for the database table.

SQL Alchemy is used as a database agnostic ORM to map the meta data to an SQLite database.
"""
from api import db
import datetime
import pathlib
import mimetypes

from sqlalchemy import inspect

class MetaData(db.Model):
    """
    A dataclass that holds the table schema for holding file meta data.
    """
    extr_id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime)
    date_modified = db.Column(db.DateTime)
    file_path = db.Column(db.String(256))
    file_name = db.Column(db.String(64))
    file_ext = db.Column(db.String(32))
    file_type = db.Column(db.String(32))

    def to_json(self) -> dict:
        """
        Output the relevant class attributes to a dict representing JSON format.

        Args:
            None
        
        Returns:
            (dict):
                The key, value pairs for all of the metadata table columns.
        """
        return {k: v for k, v in vars(self).items() if k in inspect(self).attrs.keys()}
    
    def parse_meta(self):
        """
        Parse the file path to extract the relevant meta data.

        NOTE: The values of the meta data may change dependent on Operating System.

        Args:
            None
        
        Returns:
            None
        """
        if self.file_path is not None:
            f_path = pathlib.Path(self.file_path)
            self.file_name = f_path.stem
            self.file_ext = f_path.suffix
            self.date_created = datetime.date.fromtimestamp(f_path.stat().st_ctime)
            self.date_modified = datetime.date.fromtimestamp(f_path.stat().st_mtime)
            self.file_type, enc = mimetypes.guess_type(f_path)
