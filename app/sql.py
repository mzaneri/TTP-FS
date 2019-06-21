from app import conn, cur

# Creates the stock transactions table
stockTable = """CREATE TABLE IF NOT EXISTS "stock_transactions" (
	"ID"	INTEGER NOT NULL,
	"email"	TEXT NOT NULL,
	"stock_ticker"	TEXT NOT NULL,
	"price"	REAL NOT NULL,
	"quantity"	INTEGER NOT NULL,
    "type" TEXT NOT NULL,
	PRIMARY KEY("ID")
);"""

# Creates the user information table
userTable = """CREATE TABLE IF NOT EXISTS "users" (
	"ID"	INTEGER NOT NULL,
	"name"	TEXT NOT NULL,
	"email"	TEXT NOT NULL,
	"password"	TEXT NOT NULL,
    "balance" REAL,
	PRIMARY KEY("ID")
);"""

# All statements are prepared to prevent SQL injection

# Creates enries into the user table
preparedRegister = """INSERT into users (name, email, password, balance)
VALUES (?, ?, ?, ?)"""

# Creates new stock transactions, rounding price to 2nd decimal place
preparedStock = """INSERT into stock_transactions (email, stock_ticker, price, quantity, type)
VALUES (?, ?, round(?, 2), ?, ?)"""

# Iterates accross transactions log to show current state of stocks user owns
preparedCurrentPortfolio = """
SELECT stock_ticker, sum(quantity)
FROM stock_transactions
WHERE email=?
GROUP BY stock_ticker
HAVING sum(quantity)>0
ORDER BY stock_ticker;
"""

# Shows quantiy of a specified stok that a user owns
preparedCurrentStock = """
SELECT sum(quantity)
FROM stock_transactions
WHERE email=? AND stock_ticker=?;
"""

# All transactions made by a given user
preparedTransactionLog = "SELECT * from stock_transactions WHERE email=?"

# All user info for a given user
preparedUserInfo = "SELECT * FROM users WHERE email=?"

# Changes the balance of a user after a transaction
preparedChangeBalance = "UPDATE users SET balance=round(?, 2) WHERE email=?"

# This creates the tabes for transactions and users in the database
cur.execute(stockTable)
cur.execute(userTable)
