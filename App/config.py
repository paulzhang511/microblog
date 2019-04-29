import os

basedir = os.path.abspath(os.path.dirname(__file__))


def get_data_uri(dbinfo):
    ENGING = dbinfo.get('ENGING') or 'sqlite'
    DRIVER = dbinfo.get('DRIVER') or 'pymysql'
    USER = dbinfo.get('USER') or 'root'
    PASSWORD = dbinfo.get('PASSWORD') or 'root'
    HOST = dbinfo.get('HOST') or 'localhost'
    PORT = dbinfo.get('PORT') or '3306'
    NAME = dbinfo.get('NAME') or 'mysqldb'

    return '{}+{}://{}:{}@{}:{}/{}'.format(ENGING, DRIVER, USER, PASSWORD, HOST, PORT, NAME)


class Config:
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'you-will-never-guess-xdkeksfjdkjvwikjvskjfidfkjwkjds'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    OPENID_PROVIDERS = [
        {'name': 'Google', 'url': 'https://www.google.com/accounts/o8/id'},
        {'name': 'Yahoo', 'url': 'https://me.yahoo.com'},
        {'name': 'AOL', 'url': 'http://openid.aol.com/<username>'},
        {'name': 'Flickr', 'url': 'http://www.flickr.com/<username>'},
        {'name': 'MyOpenID', 'url': 'https://www.myopenid.com'}]


class DevelopConfig(Config):
    DEBUG = True

    DATABASE ={
        'ENGING': 'mysql',
        'DRIVER': 'pymysql',
        'USER': 'root',
        'PASSWORD': '123456',
        'HOST': 'localhost',
        'PORT': '3306',
        'NAME': 'PythonFlaskmysqldb'
    }

    SQLALCHEMY_DATABASE_URI = get_data_uri(DATABASE)


class TestingConfig(Config):
    DEBUG = True

    DATABASE ={
        'ENGING': 'mysql',
        'DRIVER': 'pymysql',
        'USER': 'root',
        'PASSWORD': '123456',
        'HOST': 'localhost',
        'PORT': '3306',
        'NAME': 'PythonFlaskmysqldb'
    }

    SQLALCHEMY_DATABASE_URI = get_data_uri(DATABASE)


class StagingConfig(Config):
    DEBUG = False

    DATABASE ={
        'ENGING': 'mysql',
        'DRIVER': 'pymysql',
        'USER': 'root',
        'PASSWORD': '123456',
        'HOST': 'localhost',
        'PORT': '3306',
        'NAME': 'PythonFlaskmysqldb'
    }

    SQLALCHEMY_DATABASE_URI = get_data_uri(DATABASE)


class ProductConfig(Config):
    DEBUG = False

    DATABASE ={
        'ENGING': 'mysql',
        'DRIVER': 'pymysql',
        'USER': 'root',
        'PASSWORD': '123456',
        'HOST': 'localhost',
        'PORT': '3306',
        'NAME': 'PythonFlaskmysqldb'
    }

    SQLALCHEMY_DATABASE_URI = get_data_uri(DATABASE)


envs = {
        'develop': DevelopConfig,
        'testing': TestingConfig,
        'staging': StagingConfig,
        'product': ProductConfig,
        'default': DevelopConfig
}

