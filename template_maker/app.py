from flask import Flask

from template_maker.settings import DevConfig
from template_maker.assets import assets
from template_maker.builder import views as b_views
from template_maker.generator import views as g_views
from template_maker import frontmatter, users
from template_maker.extensions import (
    db, migrate, debug_toolbar, login_manager
)

def create_app(config_object=DevConfig):
    app = Flask(__name__)
    app.config.from_object(config_object)
    register_extensions(app)
    register_blueprints(app)
    return app

def register_blueprints(app):
    app.register_blueprint(b_views.blueprint)
    app.register_blueprint(g_views.blueprint)
    app.register_blueprint(frontmatter.views.blueprint)
    app.register_blueprint(users.views.blueprint)
    return None

def register_extensions(app):
    assets.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    debug_toolbar.init_app(app)
    login_manager.init_app(app)
    return None
