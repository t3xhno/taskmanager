from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os # if you wanna have db credenitalas in os.environ

app = Flask(__name__)

# SQLAlchemy setup
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///taskmanager.db'

#MySql setup
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://user:pass@localhost/dbname'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from taskmanager import routes
