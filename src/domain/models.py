"""
The domain model that simply contains the schema for the database table.

SQL Alchemy is used as a database agnostic ORM as an abstraction of an SQLite database.
This API is a CRUD wrapper which needs no further modelling outside of parsing the metadata of
a file.
"""
import datetime
import pathlib
import mimetypes
import inspect

class FileMetaData():
    """
    A class that parses the file meta data.
    """
    def __init__(self, file_path):
        self.file_path = None
        self.file_name = None
        self.file_ext = None
        self.date_created = None
        self.date_modified = None
        self.file_type = None
        self.parse_file_path(file_path)

    def parse_file_path(self, file_path):
        self.file_path = pathlib.Path(file_path)
        self.file_name = self.file_path.stem
        self.file_ext = self.file_path.suffix
        self.date_created = datetime.date.fromtimestamp(self.file_path.stat().st_ctime) # may change dependent on Operating System.
        self.date_modified = datetime.date.fromtimestamp(self.file_path.stat().st_mtime)
        self.file_type, _ = mimetypes.guess_type(self.file_path)

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
