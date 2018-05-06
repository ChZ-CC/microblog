#-*- encoding: utf-8 -*-
import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config(object):
    # 激活 跨站点请求伪造 保护
    #CSRF_ENABLED = True 
    # 当 CSRF 激活时，需要配置 SECRET_KEY，用于验证表单的一个加密令牌。
    SECRET_KEY = os.environ.get('SECRET_KEY')
    # SQLALCHEMY_DATABASE_URI 是 Flask-SQLAlchemy 扩展需要的，是数据库文件路径
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USE_SSL = os.environ.get('MAIL_USE_SSL') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['testforflask@163.com', 'system@chzcc.live']
    #ADMINS = ['system@chzcc.live']
    LANGUAGES = ['en', 'zh']
    MS_TRANSLATOR_KEY = os.environ.get('MS_TRANSLATOR_KEY')
    BD_TRANSLATOR_KEY = os.environ.get('BD_TRANSLATOR_KEY')
    BD_TRANSLATOR_ID = os.environ.get('BD_TRANSLATOR_ID')
    ELASTICSEARCH_URL = os.environ.get('ELASTICSEARCH_URL')
    POSTS_PER_PAGE = 25
    REDIS_URL = os.environ.get('REDIS_URL') or 'redis://'

