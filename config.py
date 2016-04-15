# coding: utf-8
import os  # 系统库
basedir = os.path.abspath(os.path.dirname(__file__))  # 当前文件的绝对路径


class Config:  # 定义一个Config类
    # 我去，这个SECRET_KEY亮瞎了我，小改一下
    SECRET_KEY = os.environ.get('SECRET_KEY') or '\x03y\xf4e\x95a\x15\xa4y\xfbe\xc0e\xd1\xafc\x18o\x16m'
    SSL_DISABLE = False  # 让程序拦截发往 http:// 的请求，重定向到https://, SSL 的支持只需在生产模式中启用
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True  # 每次请求结束后都会自动提交数据库中的变动,TEARDOWN(拆卸)
    SQLALCHEMY_RECORD_QUERIES = True  # 启用记录查询统计数字的功能
    BABEL_DEFAULT_LOCALE = 'zh'  # 国际化支持

    @staticmethod  # 对当前环境进行初始化
    def init_app(app):
        pass


class DevelopmentConfig(Config):  # 继承上面的Config类，对数据库进行配置
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')  # 数据库的路径，可默认是搜寻


class TestingConfig(Config):   # 测试环境运行配置
    TESTING = True
    SERVER_NAME = 'localhost:5000'  # 服务器的名称
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')  # 数据库的路径
    WTF_CSRF_ENABLED = False


class Production(Config):  # 生产环境配置
    DEBUG=True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
                              'postgresql://ray:?@localhost/blog-db'  # postgresql 也是很强大的Json存储，mongo配置不同


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': Production,
    'default': DevelopmentConfig
}
#  默认为开发环境，该源码是Ray的成品，所以也就是产品环境了，但是本地运行应该也是可以的，数据库可以自行搜索
