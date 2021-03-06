#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from app import model
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Shell
from flask_cors import CORS
from app import create_app, db
import os


config_name = os.environ.get('FLASK_DEV_CONFIG_NAME', 'devconfig')
app = create_app(config_name)
manager = Manager(app)
migrate = Migrate(app, db)
CORS(app, supports_credentials=True)


def make_shell_context():
    return {'app': app, 'User': model.User, 'College': model.College, 'db': db}


manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
