# -*- coding: utf-8 -*-

from app import app, db
from app.models import User
from flask_script import Manager, Shell, Server
from flask_migrate import Migrate, MigrateCommand


migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command("runserver", Server(host='0.0.0.0', port=8000, use_debugger=True))
manager.add_command("db", MigrateCommand)


def make_shell_context():
    return dict(app=app, db=db, User=User)

manager.add_command("shell", Shell(make_context=make_shell_context))

#测试数据库初始化
@manager.command
def datainit():
    from app.models import User
    user_list = [(u'猜猜我是谁', '18814115785'), (u'科比脑残粉', '1881411578')]
    for tu in user_list:
        user = User.query.filter_by(username=tu[0]).first()
        if not user:
            print ("make wen in admin")
            user=User(username=tu[0],phonenum=tu[1], password='123')
            db.session.add(user)
            db.session.commit()        
        else :
            print "User already in data"    
    print "all_data readly now"

if __name__ == '__main__':
    manager.run()