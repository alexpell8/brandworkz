from flask import render_template, request, jsonify
import markdown
from os.path import dirname, join

from api import api, db
from api.services import upload_file, get_metadata, query_metadata

@api.route('/')
def index():
    with open(join(dirname(api.root_path), 'README.md'), 'r') as readme:
        md = markdown.markdown(readme.read())
    return md

@api.route('/filedata/<int:extr_id>', methods=['GET'])
def get_file_metadata(extr_id):
    return get_metadata(extr_id)

@api.route('/filedata', methods=['GET'])
def get_metadata_query():
    return query_metadata(request.args)

@api.route('/upload', methods=['GET'])
def get_file_upload():
    response = upload_file(request.args)
    if response['status'] == 204:
        return render_template('upload.html', msg='Content not found. ({})'.format(request.args['path']))
    elif response['status'] == 200:
        return render_template('upload.html')
    else:
        return response
