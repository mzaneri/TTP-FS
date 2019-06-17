import sqlite3
from flask import render_template, url_for, redirect
from app import app
from app.forms import SignUp
from app.sql import preparedSignUp, preparedLogin

conn = sqlite3.connect("database.sqlite", check_same_thread=False)
cur = conn.cursor()

@app.route('/')
def blank():
    return "Starting Page"

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUp()
    if form.validate_on_submit():
        cur.execute(preparedLogin, (form.email.data,))
        result = cur.fetchone()
        if result is not None:
            return render_template('signup.html', form=form)
        newUserInfo = (form.name.data, form.email.data, form.password.data, 5000)
        cur.execute(preparedSignUp, newUserInfo)
        conn.commit()
        return redirect(url_for('blank'))
    return render_template('signup.html', form=form)
