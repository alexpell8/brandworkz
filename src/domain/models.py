"""
The domain model that parses the uploaded file path into an object that is then mapped to
the database via SQLAlchemy.

This API is a CRUD wrapper which needs no further modelling outside of parsing the metadata of
a file.
"""
import datetime
import pathlib
import mimetypes

class FileMetaData():
    """
    A class that parses the file meta data.
    """
    def __init__(self, file_path):
        """
        Initialise the known meta data attributes.

        Args:
            file_path (str): The filepath to the uploaded file.
        """
        self.file_path = file_path
        self.file_name = None
        self.file_ext = None
        self.date_created = None
        self.date_modified = None
        self.file_type = None

    def parse_file_path(self):
        """
        Parse the file path into the known/required attributes.
        """
        file_path = pathlib.Path(self.file_path)
        self.file_path = str(file_path)
        self.file_name = file_path.stem
        self.file_ext = file_path.suffix
        self.date_created = datetime.date.fromtimestamp(file_path.stat().st_ctime) # may change dependent on Operating System.
        self.date_modified = datetime.date.fromtimestamp(file_path.stat().st_mtime)
        self.file_type, _ = mimetypes.guess_type(file_path)

    def to_json(self) -> dict:
        """
        Output the relevant class attributes to a dict representing JSON format.

        Args:
            None
        
        Returns:
            (dict):
                The key, value pairs for all of the metadata table columns.
        """
        return {k: v for k, v in self.__dict__.items() if not k.startswith('_')}
