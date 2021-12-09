"""
Initialises the API and the local database.
"""
from os.path import dirname, join, exists
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

api = Flask(__name__)

db_uri = 'sqlite:///' + join(dirname(api.root_path), 'metadata.db')

api.config['SQLALCHEMY_DATABASE_URI'] = db_uri
api.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(api)

# import models to correctly initialise db table
from api import models
db.create_all()
