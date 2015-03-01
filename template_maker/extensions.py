from flask.ext.sqlalchemy import SQLAlchemy
db = SQLAlchemy()

from flask.ext.bcrypt import Bcrypt
bcrypt = Bcrypt()

from flask.ext.migrate import Migrate
migrate = Migrate()

from flask.ext.debugtoolbar import DebugToolbarExtension
debug_toolbar = DebugToolbarExtension()

