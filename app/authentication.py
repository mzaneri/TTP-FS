from flask import render_template, url_for, redirect, flash
from flask_login import current_user, login_user, login_required, logout_user
from app import app, login_manager, bcrypt, conn, cur
from app.forms import RegisterForm, SignInForm
from app.sql import preparedRegister, preparedUserInfo
from app.models import User

# Callback that runs on every view endpoint call to ensure user is logged in
@login_manager.user_loader
def user_loader(email):
    cur.execute(preparedUserInfo, (email,))
    result = cur.fetchone()
    if not result:
        return None
    user = User(result)
    return user

# Callback to redirect user when trying to access unauthorized views
@login_manager.unauthorized_handler
def unauthorized():
    flash("You must signin to access the last page you attempted to access")
    return redirect(url_for("signin"))

# View for registering
@app.route('/register', methods=['GET', 'POST'])
def register():
    # If user is signed in already, redirects to portfolio view
    if current_user.is_authenticated:
        flash("Can't register if you're already signed in")
        return redirect(url_for("portfolio"))
    form = RegisterForm()
    # If this function returns true, it's a valid post request
    if form.validate_on_submit():
        # Checks to see if user info for register exists in db already
        cur.execute(preparedUserInfo, (form.email.data,))
        result = cur.fetchone()
        if result is not None:
            flash("Email is already in use")
            return redirect(url_for('register'))
        # Salts and hashes password
        pw_hash = bcrypt.generate_password_hash(form.password.data)
        # Creates new user with a balance of 5000
        newUserInfo = (form.name.data, form.email.data, pw_hash, 5000)
        # Add new user to db
        cur.execute(preparedRegister, newUserInfo)
        conn.commit()
        # Redirects to signin page
        return redirect(url_for('signin'))
    # If get request, take html page and form object to be rendered and sent to client
    return render_template('register.html', form=form)

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    # Redirects user if currently signed in
    if current_user.is_authenticated:
        flash("Can't signin if you're already signed in")
        return redirect(url_for("portfolio"))
    form = SignInForm()
    # If this function returns true, it's a valid post request
    if form.validate_on_submit():
        # Checks to see if user exists
        cur.execute(preparedUserInfo, (form.email.data,))
        result = cur.fetchone()
        if not result:
            flash("This user does not exist")
            return redirect(url_for('register'))
        # Instantiates instance of User object
        user = User(result)
        # Authenticates password securely using Bcrypt
        if bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('portfolio'))
        flash("Incorrect password")
        return redirect(url_for('signin'))
    # If get request, take html page and form object to be rendered and sent to client
    return render_template('signin.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('signin'))

@app.route('/')
def index():
    return redirect(url_for('register'))
