from flask.ext.sqlalchemy import SQLAlchemy
db = SQLAlchemy()

from flask.ext.bcrypt import Bcrypt
bcrypt = Bcrypt()

from flask.ext.migrate import Migrate
migrate = Migrate()
