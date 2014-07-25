from flask import Flask
from flask.ext.login import LoginManager
from flask.ext.bcrypt import Bcrypt
from flask.ext.restful import Api
import os
import logging

module_logger = logging.getLogger('wcsc_app')

app = Flask(__name__)
api = Api(app)
app.config.from_object('config')

login_manager = LoginManager(app)

bcrypt = Bcrypt(app)

from database import db_session as db
from app.views import *