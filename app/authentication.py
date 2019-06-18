from flask import render_template, url_for, redirect
from flask_login import current_user, login_user, login_required, logout_user
from app import app, login_manager, bcrypt, conn, cur
from app.forms import RegisterForm, SignInForm
from app.sql import preparedRegister, preparedUserInfo
from app.models import User

@login_manager.user_loader
def user_loader(email):
    cur.execute(preparedUserInfo, (email,))
    result = cur.fetchone()
    if not result:
        return None
    user = User(result)
    return user

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        cur.execute(preparedUserInfo, (form.email.data,))
        result = cur.fetchone()
        if result is not None:
            return render_template('register.html', form=form)
        pw_hash = bcrypt.generate_password_hash(form.password.data)
        newUserInfo = (form.name.data, form.email.data, pw_hash, 5000)
        cur.execute(preparedRegister, newUserInfo)
        conn.commit()
        return redirect(url_for('index'))
    return render_template('register.html', form=form)

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    form = SignInForm()
    if form.validate_on_submit():
        cur.execute(preparedUserInfo, (form.email.data,))
        result = cur.fetchone()
        if not result:
            return redirect(url_for('index'))
        user = User(result)
        if bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('secure'))
        return redirect(url_for('index'))
    return render_template('signin.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/')
def index():
    return render_template('index.html')
