from flask import Flask, blueprints
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from config import Config
from flask_login import LoginManager

db = SQLAlchemy()
ma = Marshmallow()
login_manager = LoginManager()


def create_app(config_file=Config):
    app = Flask(__name__)
    app.config.from_object(config_file)

    login_manager.login_view = 'main.auth.login'

    login_manager.init_app(app)
    db.init_app(app)
    ma.init_app(app)

    from app.routers import bp
    app.register_blueprint(bp)
    return app
