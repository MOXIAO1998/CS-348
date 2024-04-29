import os


class Config(object):
    """
    configuration file
    """
    FLASK_DEBUG = True
    SECRET_KEY = os.environ.get('SECRET_KEY') or ''

    # database configuration
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(os.path.dirname(__file__), 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_POOL_SIZE = 10


    TEMPLATES_FOLDER = 'templates'
