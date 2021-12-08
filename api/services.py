from logging import error
from os.path import exists

from api.models import MetaData
from api import db

def upload_file(request_args):
    if 'path' in request_args:
        path_arg = request_args['path']
        if exists(path_arg):
            f_data = MetaData(file_path=path_arg)
            f_data.parse_meta()
            db.session.add(f_data)
            db.session.commit()
            meta = f_data.to_json()
            status = 201
        else:
            meta = None
            status = 204
    else:
        meta = None
        status = 200
    return {
        'metadata': meta,
        'status': status,
    }

def get_metadata(extr_id):
    if extr_id is not None:
        return {
            'metadata': MetaData.query.get(extr_id).to_json(),
            'status': 200
        }

def query_metadata(request_args):
    if 'tag' in request_args.keys() and 'value' in request_args.keys():
        tag = request_args['tag']
        value = request_args['value']
        return {
            'metadata': [meta.to_json() for meta in MetaData.query.filter(getattr(MetaData, tag) == value)],
            'query': {
                'tag': request_args['tag'],
                'value': request_args['value']
                },
            'status': 200
        }
    elif len(request_args) == 0:
        return {
            'metadata': [meta.to_json() for meta in MetaData.query.all()],
            'status': 200
        }
    else:
        return {
            'metadata': None,
            'status': 204,
            'error': 'did not supply tag and value in query'
        }
