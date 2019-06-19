from app import conn, cur

stockTable = """CREATE TABLE IF NOT EXISTS "stock_transactions" (
	"ID"	INTEGER NOT NULL,
	"email"	TEXT NOT NULL,
	"stock_ticker"	TEXT NOT NULL,
	"price"	REAL NOT NULL,
	"quantity"	INTEGER NOT NULL,
    "type" TEXT NOT NULL,
	PRIMARY KEY("ID")
);"""

userTable = """CREATE TABLE IF NOT EXISTS "users" (
	"ID"	INTEGER NOT NULL,
	"name"	TEXT NOT NULL,
	"email"	TEXT NOT NULL,
	"password"	TEXT NOT NULL,
    "balance" REAL,
	PRIMARY KEY("ID")
);"""

preparedRegister = """INSERT into users (name, email, password, balance)
VALUES (?, ?, ?, ?)"""

preparedStock = """INSERT into stock_transactions (email, stock_ticker, price, quantity, type)
VALUES (?, ?, ?, ?, ?)"""

preparedCurrentPortfolio = """
SELECT stock_ticker, sum(quantity)
FROM stock_transactions
WHERE email=?
GROUP BY stock_ticker
HAVING sum(quantity)>0
ORDER BY stock_ticker;
"""

preparedCurrentStock = """
SELECT sum(quantity)
FROM stock_transactions
WHERE email=? AND stock_ticker=?;
"""

preparedTransactionLog = "SELECT * from stock_transactions WHERE email=?"

preparedUserInfo = "SELECT * FROM users WHERE email=?"

preparedChangeBalance = "UPDATE users SET balance=? WHERE email=?"

cur.execute(stockTable)
cur.execute(userTable)
