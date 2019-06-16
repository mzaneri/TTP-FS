from flask import Flask

app = Flask(__name__)

app.config['SECRET_KEY'] = "gbbsb54k6rzta5i75yAEt"

from app import routes
