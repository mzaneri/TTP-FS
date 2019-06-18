from flask import render_template, url_for, redirect, flash
from flask_login import current_user, login_user, login_required, logout_user
from app import app, login_manager, bcrypt, conn, cur
from app.sql import preparedTransactionLog, preparedCurrentPortfolio, preparedStock, preparedChangeBalance, preparedCurrentStock
from app.models import User
from app.forms import StockForm
import requests


@app.route('/secure')
@login_required
def secure():
    return render_template("secure.html")

@app.route('/transactions', methods=["GET"])
@login_required
def transactions():
    cur.execute(preparedTransactionLog, (current_user.email,))
    completed = cur.fetchall()
    return render_template("transactions.html", completed=completed)

@app.route('/portfolio', methods=['GET', 'POST'])
@login_required
def portfolio():
    form = StockForm()
    cur.execute(preparedCurrentPortfolio, (current_user.email,))
    all_transactions = cur.fetchall()
    balance = current_user.balance
    if form.validate_on_submit():
        ticker = form.ticker.data.lower()
        request_url = f"https://api.iextrading.com/1.0/stock/{ticker}/book"
        r = requests.get(request_url)
        if r.status_code != 200:
            flash("That ticker does not exist")
            return redirect(url_for("portfolio"))
        price = r.json()['quote']['latestPrice']
        quantity = int(form.quantity.data)
        transaction_cost = quantity * price
        new_balance = current_user.balance - transaction_cost
        if quantity < 0:
            cur.execute(preparedCurrentStock, (current_user.email, ticker))
            result = cur.fetchone()
            if result[0] is None or result[0] < (-1 * quantity):
                flash("You can't sell more than you have")
                return redirect(url_for("portfolio"))
            cur.execute(preparedStock, (current_user.email, ticker, price, quantity))
            conn.commit()
            cur.execute(preparedChangeBalance, (new_balance, current_user.email))
            conn.commit()
        elif transaction_cost > current_user.balance:
            flash("You don't have enough money to buy this")
        else:
            cur.execute(preparedStock, (current_user.email, ticker, price, quantity))
            conn.commit()
            cur.execute(preparedChangeBalance, (new_balance, current_user.email))
            conn.commit()
        return redirect(url_for("portfolio"))
    value, annotated = getPrices(all_transactions)
    return render_template("portfolio.html", form=form, annotated=annotated, balance=balance, value=value)

def getPrices(all_transactions):
    annotated = []
    value = 0
    for transaction in all_transactions:
        stock = requests.get(f"https://api.iextrading.com/1.0/stock/{transaction[0]}/book").json()
        opening = float(stock['quote']['open'])
        current = float(stock['quote']['latestPrice'])
        stock_value = current * transaction[1]
        direction = "Green" if current > opening else "Red"
        annotated.append((transaction[0], transaction[1], stock_value, direction))
        value += stock_value
    return value, annotated
