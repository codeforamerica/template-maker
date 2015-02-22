from flask.ext.script import Manager, Server

from template_maker.app import create_app
from template_maker.settings import DevConfig, ProdConfig

app = create_app(DevConfig)

manager = Manager(app)
manager.add_command('server', Server())

if __name__ == '__main__':
    manager.run()