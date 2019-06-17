import sqlite3

stockTable = """CREATE TABLE IF NOT EXISTS "stock_transactions" (
	"ID"	INTEGER NOT NULL,
	"email"	TEXT NOT NULL,
	"stock_ticker"	TEXT NOT NULL,
	"price"	REAL NOT NULL,
	"quantity"	INTEGER NOT NULL,
	PRIMARY KEY("ID")
);"""

userTable = """CREATE TABLE IF NOT EXISTS "users" (
	"ID"	INTEGER NOT NULL,
	"name"	TEXT NOT NULL,
	"email"	TEXT NOT NULL,
	"password"	TEXT NOT NULL,
	PRIMARY KEY("ID")
);"""

preparedSignUp = """INSERT into users (name, email, password)
VALUES (?, ?, ?)"""

preparedStock = """INSERT into stock_transactions (email, stock_ticker, price, quantity)
VALUES (?, ?, ?, ?)"""

preparedLogin = "SELECT password FROM users WHERE email=?"

preparedTransactionLog = """
SELECT stock_ticker, sum(quantity)
FROM stock_transactions
WHERE email=?
GROUP BY stock_ticker
HAVING sum(quantity)>0
ORDER BY stock_ticker;
"""

conn = sqlite3.connect("database.sqlite")
cursor = conn.cursor()
cursor.execute(stockTable)
cursor.execute(userTable)

conn.close()
