from flask import render_template, url_for, redirect
from flask_login import current_user, login_user, login_required, logout_user
from app import app, login_manager, bcrypt, conn, cur
from app.sql import preparedTransactionLog
from app.models import User

@app.route('/secure')
@login_required
def secure():
    return "Hi and Welcome to secure place"

@app.route('/transactions')
@login_required
def transactions():
    cur.execute(preparedTransactionLog, (current_user.email,))
    result = cur.fetchall()
    moves = ""
    for res in result:
        moves += (str(res) + '\n')
    return moves

@app.route('/portfolio')
@login_required
def portfolio():
    pass
