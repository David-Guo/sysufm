# -*- coding: utf-8 -*-

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_moment import Moment
from config import config
import os


basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

# 使用默认的配置（开发环境）
app.config.from_object(config['default'])

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'login'
login_manager.init_app(app)

moment = Moment(app)

from . import views