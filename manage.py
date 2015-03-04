from flask.ext.script import Manager, Server
from flask.ext.migrate import MigrateCommand

from template_maker.app import create_app
from template_maker.settings import DevConfig, ProdConfig

app = create_app(DevConfig)

manager = Manager(app)
manager.add_command('server', Server(port=9000))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
