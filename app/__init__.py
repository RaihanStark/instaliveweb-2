from flask import Flask
import flask_assets
from config import config as Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config['development'])

    # Flask-Assets Bundler
    from .assets import bundles
    assets = flask_assets.Environment()
    assets.init_app(app)
    
    assets.register(bundles)

    # Routes
    from app.base.views import base
    from app.api.views import api
    # Blueprint
    app.register_blueprint(base)
    app.register_blueprint(api,url_prefix='/v1')
    
    return app