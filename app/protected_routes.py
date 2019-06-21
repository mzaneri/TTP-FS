from flask import render_template, url_for, redirect, flash
from flask_login import current_user, login_user, login_required, logout_user
from app import app, login_manager, bcrypt, conn, cur
from app.sql import preparedTransactionLog, preparedCurrentPortfolio, preparedStock, preparedChangeBalance, preparedCurrentStock
from app.models import User
from app.forms import StockForm
import requests

# Function to test user authentication
@app.route('/secure')
@login_required
def secure():
    return render_template("secure.html")

# View that lists all transactions,
@app.route('/transactions', methods=["GET"])
@login_required
def transactions():
    # Query to retrieve all users transactions
    cur.execute(preparedTransactionLog, (current_user.email,))
    completed = cur.fetchall()
    completed = displayWrapper(completed)
    return render_template("transactions.html", completed=completed)

# This function changes the quantity to make sure its postive
def displayWrapper(completed):
    wrapped = []
    for line in completed:
        if line[4] < 0:
            new = (line[0], line[1], line[2], line[3], -line[4], line[5])
        else:
            new = line
        wrapped.append(new)
    return wrapped

@app.route('/portfolio', methods=['GET', 'POST'])
@login_required
def portfolio():
    form = StockForm()
    # Fetches and lists stock user current owns
    cur.execute(preparedCurrentPortfolio, (current_user.email,))
    all_transactions = cur.fetchall()
    balance = current_user.balance
    # If this function returns true, its a valid post request
    if form.validate_on_submit():
        ticker = form.ticker.data.upper()
        # Format string for request
        request_url = f"https://api.iextrading.com/1.0/stock/{ticker.lower()}/book"
        r = requests.get(request_url)
        # If the returned status code is not 200, assumes the ticker was invalid
        if r.status_code != 200:
            flash("That ticker does not exist")
            return redirect(url_for("portfolio"))
        # Parses json to get current price
        price = r.json()['quote']['latestPrice']
        quantity = int(form.quantity.data)
        if quantity < 1:
            flash("You can't have a negative quantity")
            return redirect(url_for("portfolio"))
        # If the user clicks the 'sell' button
        if form.sell.data:
            # Queries the db to get the quantity the user owns of the stock
            cur.execute(preparedCurrentStock, (current_user.email, ticker))
            result = cur.fetchone()
            # If the user doesn't have any of the stock or is trying to sell more than they own
            if result[0] is None or result[0] < quantity:
                flash("You can't sell more than you have")
                return redirect(url_for("portfolio"))
            # Records the sale in transaction log
            cur.execute(preparedStock, (current_user.email, ticker, price, -quantity, "SELL"))
            conn.commit()
            # Adjust the user balance to reflect the sale
            new_balance = current_user.balance + (price * quantity)
            cur.execute(preparedChangeBalance, (new_balance, current_user.email))
            conn.commit()
        # If the user is trying to buy with a transaction size higher than their balance
        elif price * quantity > current_user.balance:
            flash("You don't have enough money to buy this")
        # If the user has enough money to make a purchase
        else:
            # Records the sale in transaction log
            cur.execute(preparedStock, (current_user.email, ticker, price, quantity, "BUY"))
            conn.commit()
            # Adjust the user balance to reflect the buy
            new_balance = current_user.balance - (price * quantity)
            cur.execute(preparedChangeBalance, (new_balance, current_user.email))
            conn.commit()
        return redirect(url_for("portfolio"))
    # If get request annotate the users portfolio for pricing information and send all information and portfolio to be rendered and sent to client
    value, annotated = getPrices(all_transactions)
    return render_template("portfolio.html", form=form, annotated=annotated, balance=balance, value=value)

# Takes each stock, find the current price in realtion to opening price, annotated transaction
def getPrices(all_transactions):
    annotated = []
    value = 0
    for transaction in all_transactions:
        # Makes request to IEX API for current pricing infor for each stock
        stock = requests.get(f"https://api.iextrading.com/1.0/stock/{transaction[0]}/book").json()
        opening = float(stock['quote']['open'])
        current = float(stock['quote']['latestPrice'])
        stock_value = current * transaction[1]
        if current == opening:
            direction = "Gray"
        else:
            direction = "Green" if current > opening else "Red"
        annotated.append((transaction[0], transaction[1], truncateFloat(stock_value), direction))
        value += stock_value
    return truncateFloat(value), annotated

# Truncates the length of the float in python to 2 digits for displaying to user
def truncateFloat(number):
    precision = 2
    string = str(number)
    decimal = string.find('.')
    position = decimal + precision + 1
    rounded = string[:position]
    return rounded
