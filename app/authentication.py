from flask import render_template, url_for, redirect, flash
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

@login_manager.unauthorized_handler
def unauthorized():
    flash("You must signin to access the last page you attempted to access")
    return redirect(url_for("signin"))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        flash("Can't register if you're already signed in")
        return redirect(url_for("portfolio"))
    form = RegisterForm()
    if form.validate_on_submit():
        cur.execute(preparedUserInfo, (form.email.data,))
        result = cur.fetchone()
        if result is not None:
            flash("Email is already in use")
            return redirect(url_for('register'))
        pw_hash = bcrypt.generate_password_hash(form.password.data)
        newUserInfo = (form.name.data, form.email.data, pw_hash, 5000)
        cur.execute(preparedRegister, newUserInfo)
        conn.commit()
        return redirect(url_for('signin'))
    return render_template('register.html', form=form)

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if current_user.is_authenticated:
        flash("Can't signin if you're already signed in")
        return redirect(url_for("portfolio"))
    form = SignInForm()
    if form.validate_on_submit():
        cur.execute(preparedUserInfo, (form.email.data,))
        result = cur.fetchone()
        if not result:
            flash("This user does not exist")
            return redirect(url_for('register'))
        user = User(result)
        if bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('portfolio'))
        flash("Incorrect password")
        return redirect(url_for('signin'))
    return render_template('signin.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('signin'))

@app.route('/')
def index():
    return redirect(url_for('register'))
