from flask import render_template, url_for, redirect
from flask_login import current_user, login_user, login_required, logout_user
from app import app, login_manager, bcrypt, conn, cur
from app.sql import preparedTransactionLog, preparedStock, preparedChangeBalance, preparedCurrentStock
from app.models import User
from app.forms import StockForm
import requests


@app.route('/secure')
@login_required
def secure():
    return "Hi and Welcome to secure place"

@app.route('/transactions', methods=["GET"])
@login_required
def transactions():
    cur.execute(preparedTransactionLog, (current_user.email,))
    result = cur.fetchall()
    moves = ""
    for res in result:
        moves += (str(res) + '\n')
    return moves

@app.route('/portfolio', methods=['GET', 'POST'])
@login_required
def portfolio():
    form = StockForm()
    if form.validate_on_submit():
        ticker = form.ticker.data.lower()
        request_url = f"https://api.iextrading.com/1.0/stock/{ticker}/book"
        r = requests.get(request_url)
        print(r.status_code)
        if r.status_code != 200:
            print("bad ticker")
            return redirect(url_for("blank"))
        price = r.json()['quote']['latestPrice']
        print(form.quantity.data)
        quantity = int(form.quantity.data)
        print(quantity)
        if quantity == 0:
            print("no transaction")
            return redirect(url_for("blank"))
        transaction_cost = quantity * price
        if quantity < 0:
            cur.execute(preparedCurrentStock, (current_user.email, ticker))
            result = cur.fetchone()
            if result[0] is None or result[0] < (-1 * quantity):
                print("cant sell more than you have")
                return redirect(url_for("blank"))
            cur.execute(preparedStock, (current_user.email, ticker, price, quantity))
            conn.commit()
            new_balance = current_user.balance - transaction_cost
            cur.execute(preparedChangeBalance, (new_balance, current_user.email))
            conn.commit()
            print("sold stuff")
        elif transaction_cost > current_user.balance:
            print("not enough dough")
            return redirect(url_for("blank"))
        else:
            cur.execute(preparedStock, (current_user.email, ticker, price, quantity))
            conn.commit()
            new_balance = current_user.balance - transaction_cost
            cur.execute(preparedChangeBalance, (new_balance, current_user.email))
            conn.commit()
            print("bought stuff")
            return redirect(url_for("blank"))
    return render_template('portfolio.html', form=form)
