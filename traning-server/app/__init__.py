from flask import Flask
# from flask_restful import Api
from flask_cors import *
from flask_caching import Cache
from config import config
from app.api_1_0 import *
from logging.config import dictConfig
from flask_sqlalchemy import SQLAlchemy

cache = Cache()
# 完成操作句柄
db = SQLAlchemy()
dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {
        'console': {'class': 'logging.StreamHandler',
                    # 'stream': 'ext: // sys.stdout',
                    'formatter': 'default'
                    },
        'file': {'class': 'logging.FileHandler',
                 'level': 'DEBUG',
                 'formatter': 'default',
                 'filename': 'log/systemlog.log'
                 }
    },
    # 'loggers': {
    #     'wsgi': {'level': 'DEBUG',
    #                 'handlers': '[wsgi]',
    #                 'propagate': 'no'
    #                 },
    #     'file': {'level': 'DEBUG',
    #              'handlers': '[file]',
    #              'propagate': 'no'
    #              }
    # },
    'root': {
        'level': 'INFO',
        'handlers': ['console', 'file']
    }
})


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    cache.init_app(app)
    db.init_app(app)
    # api = Api()
    # Api_1_0(api)
    # api.init_app(app)
    # 注册蓝图
    # url_prefix='/api/v1.0'是路径的前缀，相当于一级路径
    app.register_blueprint(api, url_prefix='/')
    CORS(app, supports_credentials=True)
    # print(app.url_map)
    return app




