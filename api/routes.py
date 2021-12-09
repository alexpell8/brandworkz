"""
api/routes.py

Contains the definitions for all of the end-points available to request.

The intention of this module is to remain as simplistic and clutter-free as possible
such that the end-point definitions are easily comprehendable and maintainable.
"""
from flask import render_template, request, jsonify, redirect
import markdown
from os.path import dirname, join

from api import api
from api.services import upload_file, get_metadata, get_metadata_collection, query_metadata_by_tag

@api.route('/')
def index() -> str:
    ''' The API root page.
    
    Args:
        None
    
    Returns:
        md (str):
            The README markdown translated into HTML.
    '''
    with open(join(dirname(api.root_path), 'README.md'), 'r') as readme:
        md = markdown.markdown(readme.read())
    return md

@api.route('/task')
def task_index() -> str:
    ''' The API technical task information.
    
    Args:
        None
    
    Returns:
        md (str):
            The task information markdown translated into HTML.
    '''
    with open(join(dirname(api.root_path), 'Brandworkz - Python - CODE-TASK.md'), 'r') as readme:
        md = markdown.markdown(readme.read())
    return md

@api.route('/filedata/<int:extr_id>', methods=['GET'])
def get_file_metadata(extr_id) -> dict:
    ''' Retrieves the resource at the given unique key from the filedata collection.
    
    Args:
        extr_id (int):
            The unique key for a resource.
    
    Returns:
        payload (dict):
            The requested payload in JSON format.
    '''
    payload = get_metadata(extr_id)
    return jsonify(payload)

@api.route('/filedata', methods=['GET'])
def get_metadata_query():
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

@api.route('/upload', methods=['GET', 'POST'])
def get_file_upload():
    ''' Retrieves the file upload service.
    
    This end-point displays a web form to accept a local file path and returns the status of the POST request.
    
    Args:
        None
    
    Returns:
        (HTML):
            Upload page with the creation status.
    '''
    print(request.form)
    if request.method == 'POST':
        path = request.form['path']
        status = upload_file(path)
        return render_template('upload.html', uploaded='Success! [201]' if status == 201 else 'No content: Path does not exist. [204]')

    return render_template('upload.html')
