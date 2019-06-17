import sqlite3
from flask import Flask
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

app = Flask(__name__)

app.config['SECRET_KEY'] = "gbbsb54k6rzta5i75yAEt"

bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "unauthorized"

conn = sqlite3.connect("database.sqlite", check_same_thread=False)
cur = conn.cursor()

from app import sql
from app import seed_database
from app import authentication
from app import protected_routes
