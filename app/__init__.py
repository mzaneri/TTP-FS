from flask import Flask
from flask_login import LoginManager

app = Flask(__name__)

app.config['SECRET_KEY'] = "gbbsb54k6rzta5i75yAEt"

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "unauthorized"

from app import sql
from app import seed_database
from app import routes
