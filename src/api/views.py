"""
api/routes.py

Contains the definitions for all of the end-points available to request.

This module is to remain as clutter-free as possible, delegating to services or views modules
such that the end-point definitions are easily comprehendable and maintainable.
"""
from flask import render_template, request, jsonify, redirect, url_for
import markdown
from os.path import dirname, join

from src.api import flask_api
from src.service_layer.upload import file_uploader
from src.service_layer.view_builder import get_metadata, get_metadata_collection, query_metadata_by_tag

@flask_api.route('/')
def root_endpoint() -> str:
    ''' The API root page.
    
    Args:
        None
    
    Returns:
        md (str):
            The README markdown translated into HTML.
    '''
    with open(join(dirname(dirname(flask_api.root_path)), 'README.md'), 'r') as readme:
        md = markdown.markdown(readme.read())
    return md

@flask_api.route('/task')
def task_endpoint() -> str:
    ''' The API technical task information.
    
    Args:
        None
    
    Returns:
        md (str):
            The task information markdown translated into HTML.
    '''
    with open(join(dirname(dirname(flask_api.root_path)), 'Brandworkz - Python - CODE-TASK.md'), 'r') as readme:
        md = markdown.markdown(readme.read())
    return md

@flask_api.route('/file/<int:extr_id>', methods=['GET'])
def file_metadata_endpoint(extr_id) -> dict:
    ''' Retrieves the resource at the given unique key from the filedata collection.
    
    Args:
        extr_id (int):
            The unique key for a resource given to the resource at time of upload.
    
    Returns:
        payload (dict):
            The requested payload in JSON format.
    '''
    payload = get_metadata(extr_id)
    return jsonify(payload)

@flask_api.route('/files', methods=['GET'])
def metadata_query_endpoint():
    ''' Retrieves all resources in the filedata collection.
    
    Args:
        None
    
    Returns:
        payload (dict):
            The requested payload in JSON format.
    '''
    if 'tag' not in request.args and 'value' not in request.args:
        payload = get_metadata_collection()
    else:
        tag = request.args['tag']
        value = request.args['value']
        payload = query_metadata_by_tag(tag=tag, value=value)        

    return jsonify(payload)

@flask_api.route('/upload', methods=['GET', 'POST'])
def file_upload_endpoint():
    ''' Retrieves the file upload service wrapped in a POST-REDIRECT-GET pattern.

    It displays a web form to accept a local file path and returns the status of the POST request.
    
    Args:
        None
    
    Returns:
        (HTML):
            Upload page with the creation status.
    '''
    if request.method == 'POST':
        path = request.form['path']
        extr_id, status = file_uploader(path)
        if status == 201:
            return redirect(url_for('file_metadata_endpoint', extr_id=extr_id))
        else:
            return render_template('upload.html', uploaded='No content: Path does not exist. [204]')
    else:
        return render_template('upload.html')
