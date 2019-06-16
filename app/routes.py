from app import app
from app.forms import SignUp
from flask import render_template

@app.route('/')
def blank():
    return "Starting Page"

@app.route('/signup')
def signup():
    form = SignUp()
    return render_template('signup.html', form=form)
