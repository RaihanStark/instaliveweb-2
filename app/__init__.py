from flask import Flask
import flask_assets
from config import config as Config
import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import click


db = SQLAlchemy()
migrate = Migrate()

def create_app(config):
    app = Flask(__name__)
    config_name = config
    
    if not isinstance(config, str):
        config_name = os.getenv('FLASK_ENV', 'development')

    app.config.from_object(Config[config_name])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    Config[config_name].init_app(app)

    # Flask-Assets Bundler
    from .assets import bundles
    assets = flask_assets.Environment()
    assets.init_app(app)
    assets.register(bundles)


    # Routes
    from app.base.views import base
    from app.api.views import api
    from app import models

    # Blueprint
    app.register_blueprint(base)
    app.register_blueprint(api,url_prefix='/v1')
    

    # Databases
    db.init_app(app)
    migrate.init_app(app, db)

    return app

