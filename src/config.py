"""
Contains configuration settings for use in the api.
"""
class Config:
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///../../metadata.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False