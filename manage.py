import os
from flask.ext.script import Manager, Shell, Server
from flask.ext.migrate import MigrateCommand
from flask.ext.assets import ManageAssets

from template_maker.app import create_app, db
from template_maker.settings import DevConfig, ProdConfig

if os.environ.get('TEMPLATE_MAKER_ENV') == 'prod':
    app = create_app(ProdConfig)    
else:
    app = create_app(DevConfig)

def _make_context():
    """Return context dict for a shell session so you can access
    app and db by default.
    """
    return {'app': app, 'db': db}

manager = Manager(app)
manager.add_command('server', Server(port=9000))
manager.add_command('shell', Shell(make_context=_make_context))
manager.add_command('db', MigrateCommand)
manager.add_command('assets', ManageAssets)

if __name__ == '__main__':
    manager.run()
