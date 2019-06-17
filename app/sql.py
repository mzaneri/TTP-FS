import sqlite3

stockTable = """CREATE TABLE "stock_transactions" (
	"ID"	INTEGER NOT NULL,
	"email"	TEXT NOT NULL,
	"stock_ticker"	TEXT NOT NULL,
	"price"	REAL NOT NULL,
	"quantity"	INTEGER NOT NULL,
	PRIMARY KEY("ID")
);"""

userTable = """CREATE TABLE "users" (
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

conn = sqlite3.connect("database.sqlite")
cursor = conn.cursor()
cursor.execute(stockTable)
cursor.execute(userTable)
print("hi")
cursor.execute(preparedSignUp, ("mike", "youtube.com", "hi"))
conn.commit()
cursor.execute(preparedStock, ("youtube.com", "YOU", 20.3, 2))
conn.commit()
