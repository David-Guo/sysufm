# -*- coding: utf-8 -*-

from app import app, db
from app.models import User
from flask_script import Manager, Shell, Server
from flask_migrate import Migrate, MigrateCommand


migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command("runserver", Server(host='0.0.0.0', port=5000, use_debugger=True))
manager.add_command("db", MigrateCommand)


def make_shell_context():
    return dict(app=app, db=db, User=User)

manager.add_command("shell", Shell(make_context=make_shell_context))


if __name__ == '__main__':
    manager.run()