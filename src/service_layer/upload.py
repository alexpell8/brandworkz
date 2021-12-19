"""
Contains the service layer logic.
"""
from os.path import exists, realpath

from src.domain.models import FileMetaData
from src.orm_layer.transaction import Transaction

def file_uploader(path):
    """
    Upload a file based on the file path posted by the HTML form.

    Args:
        path (str):
            The file path submitted by the form to the server.
    
    Returns:
        status (int):
            The status code
                201 - Succesfully created the entry in the database.
                204 - Content not found, path does not exist.
    """
    with Transaction() as transaction:
        path = realpath(path) # mitigate against symlinks.
        if exists(path):
            f_data = FileMetaData(file_path=path)
            f_data.parse_meta()
            transaction.add(f_data)
            transaction.commit()
            return f_data.extr_id, 201

    return None, 204

# def batch_file_uploader(paths):
#     with Transaction() as transaction:
#         for path in paths:
#             if exists(path):
#                 f_data = MetaData(file_path=path)
#                 f_data.parse_meta()
#                 transaction.add(f_data)
#         transaction.commit()
    
#     return 201