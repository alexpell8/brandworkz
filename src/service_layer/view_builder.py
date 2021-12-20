"""
The read-only views of the data base content.

This module is responsible for providing the endpoints with responses.
"""
import sqlalchemy
from src.domain.models import FileMetaData

def get_metadata(extr_id, transaction):
    """
    Retrieve the meta data related to the resource stored at a given key.

    Args:
        extr_id (int):
            Unique resource identifier
        transaction (Transaction):
            An instance of a transaction to the configured database
    
    Returns:
        (dict):
            An enveloped JSON representation of the meta data payload and the response status_code.
    """
    with transaction:
        try:
            file = transaction.session.query(FileMetaData).filter_by(extr_id=extr_id).one()
            return {
                'metadata': file.to_json(),
                'status_code': 200
            }
        except sqlalchemy.exc.NoResultFound:
            return {
                'metadata': {},
                'status_code': 204
            }


def get_metadata_collection(transaction):
    """
    Retrieve the meta data stored in the filedata collection

    Args:
        transaction (Transaction):
            An instance of a transaction to the configured database
    
    Returns:
        (dict):
            An enveloped JSON representation of the meta data payload for the full collection and the response status_code.
    """
    with transaction:
        files = transaction.session.query(FileMetaData).all()
        filedata_content = [
            {'metadata': meta.to_json()} for meta in files
            ]
        return {
            'filedata': filedata_content,
            'status_code': 200
            }


def query_metadata_by_tag(tag, value, transaction):
    """
    Retrieve the meta data related to any resource where key=value is True and the values
    of key and value are taken from the query string in the form:

    ?key=<key>&value=<value>

    Args:
        extr_id (int):
            Unique resource identifier
        transaction (Transaction):
            An instance of a transaction to the configured database
    
    Returns:
        (dict):
            An enveloped JSON representation of the meta data payload, the response status_code and any error message.
    """
    with transaction:
        try:
            filtered_files = transaction.session.query(FileMetaData).filter(getattr(FileMetaData, tag) == value)
            filedata_content = [
                {'metadata': meta.to_json()} for meta in filtered_files
                ]
            status_code = 200
            error_msg = None
        except AttributeError:
            filedata_content = {}
            status_code = 404
            error_msg = "invalid query params, column '{}' does not exist".format(tag)

        # build payload
        payload = {
            'filedata': filedata_content,
            'status_code': status_code,
            'query': {
                'tag': tag,
                'value': value
            }
        }
        if error_msg:
            payload['error'] = error_msg

        return payload