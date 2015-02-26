from flask import Flask

from template_maker.settings import DevConfig, ProdConfig
from template_maker.assets import assets
from template_maker import builder
from template_maker.extensions import (
    db,
    migrate
)

def create_app(config_object=DevConfig):
    app = Flask(__name__)
    app.config.from_object(config_object)
    register_extensions(app)
    register_blueprints(app)
    return app

def register_blueprints(app):
    app.register_blueprint(builder.views.blueprint)
    return None

def register_extensions(app):
    assets.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    return None
