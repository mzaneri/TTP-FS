from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField
from wtforms.validators import DataRequired

class RegisterForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()], render_kw={"placeholder": "Name"})
    email = StringField('Email', validators=[DataRequired()], render_kw={"placeholder": "Email"})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={"placeholder": "Password"})
    submit = SubmitField('Register')

class SignInForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()], render_kw={"placeholder": "Email"})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={"placeholder": "Password"})
    submit = SubmitField('Sign In')

class StockForm(FlaskForm):
    ticker = StringField('Ticker Symbol', validators=[DataRequired()], render_kw={"placeholder": "Ticker Symbol"})
    quantity = IntegerField('Quantity', validators=[DataRequired()], render_kw={"placeholder": "Quantity"})
    submit = SubmitField('Submit Transaction')
