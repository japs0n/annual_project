import os

# domain = os.environ['SERVICE_DOMAIN']
db_url = os.environ['DB_URL']
db_user = os.environ['DB_USER']
db_password = os.environ['DB_PASSWORD']
db_dbname = os.environ['DB_DBNAME']


class CommonConfig(object):
    SECRET_KEY = '1N3UaUprdFHCKkTipVAv'


class ProdConfig(CommonConfig):
    """生产环境设置"""
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://' + db_user + ':' + db_password + '@' + db_url + '/' + db_dbname
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False


class DevConfig(CommonConfig):
    """开发环境设置"""
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@localhost:3306/em?charset=utf8'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    DEBUG = True


config = {'devconfig': DevConfig, 'prodconfig': ProdConfig, 'default': DevConfig}
