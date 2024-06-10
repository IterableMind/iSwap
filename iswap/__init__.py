from flask import Flask
from flask_wtf import FlaskForm
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate 
from wtforms import StringField, SearchField, PasswordField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Length, EqualTo, Email
from flask_login import LoginManager
from flask_moment import Moment


app = Flask(__name__)
# application configuration
app.config['SECRET_KEY'] = '017ea1eef80483c737ebbd954d7f8a8fb7240730aa613f959f95de26d2eb1f81'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///store.db'

db = SQLAlchemy(app)
migrate = Migrate(app, db) 
login = LoginManager(app)
moment = Moment(app)
login.login_view = 'auth_bp.login'
login.login_message = 'Please login to access this page!'
login.login_message_category = 'info'

from . import models