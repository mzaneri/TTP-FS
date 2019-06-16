from app import app
from app.forms import SignUp
from flask import render_template, url_for, redirect

@app.route('/')
def blank():
    return "Starting Page"

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUp()
    if form.validate_on_submit():
        print(form.name.data, form.email.data, form.password.data)
        return redirect(url_for('blank'))
    return render_template('signup.html', form=form)
