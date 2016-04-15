# coding: utf-8
# manage.py程序启动脚本，定义shell方法等等，遇到不懂的地方就跳过
from flask.ext.script import Manager, Shell  # 如上，实现这两个功能必须引用这两个库
from app import create_app, db  # 路径在app/__init__中，db = SQLAlchemy() 只是一个实例化的对象
from app.models import User, Role, Post, Comment  # app.model和数据库相关的表单，角色，发帖，评论相关操作
from flask_migrate import Migrate, MigrateCommand, upgrade # 数据库迁移

app = create_app('production')  # 创建一个'production'app，和wsigi对应
manager = Manager(app)   # 初始化开始
migrate = Migrate(app, db)  # 初始化


def make_shell_context():  # manage的shell中添加一个上下文函数，在shell中可以直接导入
    return dict(app=app, db=db, User=User, Role=Role)


manager.add_command("shell", Shell(make_context=make_shell_context))  # 在shell中直接运行app\db\user\role
# 在shell 中增加db命令，(venv)  python manage.py db init，直接运行MigrateCommand的初始化命令创建迁移库
#  (venv) python manage.py db migrate -m "initial migration" 创建迁移脚本
#  (venv) python manage.py  db upgrade 把迁移应用到数据库中
manager.add_command('db', MigrateCommand)


@manager.command  # 建立一个shell命令，用来运行livereload函数，作用在调试中和修改同步显示：(venv) python manage.py dev
def dev():
    from livereload import Server
    live_server = Server(app.wsgi_app)
    live_server.watch('**/*.*')  # 对项目全文见进行实施监控
    live_server.serve(open_url=False) # 是否用DEV进行监控，True时才有作用


@manager.command  # 单元你测试模式，本文头已经定义为production模式，在纸质教程中的config还有一个开发环境
def test():  # 关于测试，暂时pass，等用的时候在学习
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


@manager.command
def deploy():
    upgrade()  # 把数据库迁移到最新修订版本
    Role.seed() # app\models.py中定义了一个seed()的方法，添加所有用户，并提交，session为sqlalchemy中的事务


@manager.command  # 教程木有的命令，生成虚拟的用户数据，http://tomekwojcik.github.io/ForgeryPy/
def forged():
    from forgery_py import basic, lorem_ipsum, name, internet, date
    from random import randint

    db.drop_all()
    db.create_all()  # 删除数据库中的数据

    Role.seed()

    guests = Role.query.first()

    def generate_comment(func_author, func_post):  # 生成虚拟的评论
        return Comment(body=lorem_ipsum.paragraphs(),
                       created=date.date(past=True),
                       author=func_author(),
                       post=func_post())

    def generate_post(func_author):  # 生成虚拟的文章
        return Post(title=lorem_ipsum.title(),
                    body=lorem_ipsum.paragraphs(),
                    created=date.date(),
                    author=func_author())

    def generate_user():  # 生成虚拟的用户
        return User(name=internet.user_name(),
                    email=internet.email_address(),
                    password=basic.text(6, at_least=6, spaces=False),
                    role=guests)

    users = [generate_user() for i in range(0, 5)]
    db.session.add_all(users) # 增加2个用户

    random_user = lambda: users[randint(0, 4)]

    posts = [generate_post(random_user) for i in range(0, randint(50, 200))]  # 用随机的用户发布50-200条随机的文章
    db.session.add_all(posts)

    random_post = lambda: posts[randint(0, len(posts) - 1)]
    comments = [generate_comment(random_user, random_post) for i in range(0, randint(2, 100))]  # 再整点随机的评论，擦
    db.session.add_all(comments)  # 提交评论

    db.session.commit()  # 提交所有的数据


if __name__ == '__main__':  # 好吧，可以运行了！
    manager.run()
