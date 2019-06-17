import sqlite3
from flask import render_template, url_for, redirect
from flask_login import current_user, login_user, login_required, logout_user
from app import app, login_manager
from app.forms import SignUpForm, LoginForm
from app.sql import preparedSignUp, preparedLogin, preparedUserInfo
from app.models import User

conn = sqlite3.connect("database.sqlite", check_same_thread=False)
cur = conn.cursor()

@login_manager.user_loader
def user_loader(email):
    cur.execute(preparedUserInfo, (email,))
    result = cur.fetchone()
    if not result:
        return None
    user = User(result)
    return user

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
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

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        cur.execute(preparedUserInfo, (form.email.data,))
        result = cur.fetchone()
        if not result:
            return redirect(url_for('blank'))
        user = User(result)
        if form.password.data == user.password:
            login_user(user)
            return redirect(url_for('secure'))
        return redirect(url_for('blank'))
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('blank'))

@app.route('/secure')
@login_required
def secure():
    return "Hi and Welcome to secure place"

@app.route('/')
def blank():
    return "Starting Page"
