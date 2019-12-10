from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
import os


class Config:
    SQLALCHEMY_DATABASE_URI = 'postgres://eurczfydmrjive:dca46aadb46ebcf2bbc06bf37432f9a04f0a06dc68f8c0d2255ae96b59c38eaa@ec2-184-72-223-163.compute-1.amazonaws.com:5432/d6julun39c92p1'
    # SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    SQLALCHEMY_POOL_SIZE = 100
    SQLALCHEMY_MAX_OVERFLOW = -1
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CACHE_TYPE = 'filesystem'
    CACHE_DIR = 'cache_root'
    ADMIN_ROLE_ID = 1
    MODERATOR_ROLE_ID = 2


class DevelopConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@localhost:3306/db_bbs?charset=utf8'


class ReleaseConfig(Config):
    pass


config = {
    'development': DevelopConfig,
    'release': ReleaseConfig,
    'default': DevelopConfig
}
