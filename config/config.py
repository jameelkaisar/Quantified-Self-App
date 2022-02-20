import os


BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config():
    DEBUG = False
    SQLITE_DB_DIR = None
    SQLALCHEMY_DATABASE_URI = None
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "SECRET_KEY"


class DevConfig(Config):
    DEBUG = True
    SQLITE_DB_DIR = os.path.join(BASE_DIR, "../database")
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(SQLITE_DB_DIR, "dev_db.sqlite3")
