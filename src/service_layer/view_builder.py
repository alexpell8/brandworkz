"""
The read-only views of the data base content.

This module is responsible for providing the endpoints with responses.
"""
from src.domain.models import FileMetaData
from src.orm_layer.transaction import Transaction

def get_metadata(extr_id):
    """
    Retrieve the meta data related to the resource stored at a given key.

    Args:
        extr_id (int):
            Unique resource identifier
    
    Returns:
        (dict):
            An enveloped JSON representation of the meta data payload and the response status.
    """
    transaction = Transaction()
    with transaction:
        print(transaction.session)
        payload = transaction.session.query(FileMetaData).filter_by(extr_id=extr_id).one()
        if payload:
            return {
                'metadata': payload.to_json(),
                'status': 200
            }

        return {
            'metadata': {},
            'status': 204
        }

def get_metadata_collection():
    """
    Retrieve the meta data stored in the filedata collection

    Args:
        None
    
    Returns:
        (dict):
            An enveloped JSON representation of the meta data payload for the full collection and the response status.
    """
    transaction = Transaction()
    with transaction:
        filedata_content = [{'metadata': meta.to_json()} for meta in transaction.session.query(FileMetaData).all()]
        return {
            'filedata': filedata_content,
            'status': 200
            }

def query_metadata_by_tag(tag, value):
    """
    Retrieve the meta data related to any resource where key=value is True and the values
    of key and value are taken from the query string in the form:

    ?key=<key>&value=<value>

    Args:
        extr_id (int):
            Unique resource identifier
    
    Returns:
        (dict):
            An enveloped JSON representation of the meta data payload, the response status and any error message.
    """
    transaction = Transaction()
    with transaction:
        try:
            filedata_content = [
                {'metadata': meta.to_json()} for meta in transaction.session.query(FileMetaData).filter_by(getattr(FileMetaData, tag) == value)
                ]
            status = 200
            error_msg = None
        except AttributeError:
            filedata_content = {}
            status = 404
            error_msg = "invalid query params, column '{}' does not exist".format(tag)

        # build payload
        payload = {
            'filedata': filedata_content,
            'status': status,
            'query': {
                'tag': tag,
                'value': value
            }
        }
        if error_msg:
            payload['error'] = error_msg

        return payload