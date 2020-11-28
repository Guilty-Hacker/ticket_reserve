import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def get_db_uri(dbinfo):
    engine = dbinfo.get("ENGINE") or "sqlite"
    driver = dbinfo.get("DRIVER") or "sqlite"
    user = dbinfo.get("USER") or ""
    password = dbinfo.get("PASSWORD") or ""
    host = dbinfo.get("HOST") or ""
    port = dbinfo.get("PORT") or ""
    name = dbinfo.get("NAME") or ""
    # mysql+pymysql://root:dandan@localhost:3306/flask_test
    return "{}+{}://{}:{}@{}:{}/{}".format(engine,driver,user,password,host,port,name)


class Config:
    DEBUG = False
    TFSTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # SECRET_KEY = "XiaoHao"
    SECRET_KEY = "小豪"
    SESSION_TYPE = 'redis'
    SESSION_COOKIE_SESSION = True

class DevelopConfig(Config):
    DEBUG = True
    dbinfo = {
        "ENGINE":"mysql",
        "DRIVER":"pymysql",
        "USER":"root",
        "PASSWORD":"dandan",
        "HOST":"localhost",
        "PORT":"3306",
        "NAME":"flask_tpp",
    }
    SQLALCHEMY_DATABASE_URI = get_db_uri(dbinfo)


class TestConfig(Config):
    TFSTING = True
    dbinfo = {
        "ENGINE":"mysql",
        "DRIVER":"pymysql",
        "USER":"root",
        "PASSWORD":"dandan",
        "HOST":"localhost",
        "PORT":"3306",
        "NAME":"flask_TPP",
    }
    SQLALCHEMY_DATABASE_URI = get_db_uri(dbinfo)


class StagingConfig(Config):
    dbinfo = {
        "ENGINE":"mysql",
        "DRIVER":"pymysql",
        "USER":"root",
        "PASSWORD":"dandan",
        "HOST":"localhost",
        "PORT":"3306",
        "NAME":"api_test",
    }
    SQLALCHEMY_DATABASE_URI = get_db_uri(dbinfo)


class ProductConfig(Config):
    dbinfo = {
        "ENGINE":"mysql",
        "DRIVER":"pymysql",
        "USER":"root",
        "PASSWORD":"dandan",
        "HOST":"localhost",
        "PORT":"3306",
        "NAME":"flask_TPP",
    }
    SQLALCHEMY_DATABASE_URI = get_db_uri(dbinfo)

envs = {
    "development":DevelopConfig,
    "testing":TestConfig,
    "staging":StagingConfig,
    "product":ProductConfig,
    "default":DevelopConfig,
}

ADMINS = ('admin',)

FILE_PATH_PREFIX = "/static/uploads/icons"

UPLOAD_DIR = os.path.join(BASE_DIR,'App/static/uploads/icons')