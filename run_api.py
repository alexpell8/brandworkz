from src.api import flask_api

import sys

if __name__ == '__main__':
    debug = True if sys.argv[-1] == 'debug' else False
    flask_api.run(debug=debug)