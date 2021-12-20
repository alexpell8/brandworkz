"""
Initialises the API and the local database.

This is an example of a bootstrapper script to launch the API.
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

flask_api = Flask(__name__)
flask_api.config.from_object('src.config.Config')

from src.api import views