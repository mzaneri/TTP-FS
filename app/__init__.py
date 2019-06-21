import sqlite3
from flask import Flask
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

app = Flask(__name__)

#TODO: change to read from os environmental variable
app.config['SECRET_KEY'] = "gbbsb54k6rzta5i75yAEt"

# Flask exension to handle salting and hashing passwords securely
bcrypt = Bcrypt(app)

# Flask extension to handle user login sessions
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "unauthorized"

# Abstraction for objects that handle db IO
conn = sqlite3.connect("database.sqlite", check_same_thread=False)
cur = conn.cursor()

# Imports prepared SQL queries for use in app
from app import sql
# Adds some test data to db and removes old data
from app import seed_database
# Imports views handling registration and authentication
from app import authentication
# Imports views for portfolio and transactions
from app import protected_routes
