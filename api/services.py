"""
Contains the services or business logic for the API.
"""
from os.path import exists, realpath

from api.models import MetaData
from api import db

def upload_file(path):
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
    path = realpath(path) # mitigate against symlinks.
    if exists(path):
        f_data = MetaData(file_path=path)
        f_data.parse_meta()
        db.session.add(f_data)
        db.session.commit()
        return 201

    return 204

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
    payload = MetaData.query.get(extr_id)
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
    filedata_content = [{'metadata': meta.to_json()} for meta in MetaData.query.all()]
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
    try:
        filedata_content = [
            {'metadata': meta.to_json()} for meta in MetaData.query.filter(getattr(MetaData, tag) == value)
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