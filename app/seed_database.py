from app import bcrypt, conn, cur
from app.sql import preparedRegister, preparedStock, preparedTransactionLog

cur.execute("DELETE FROM users")
conn.commit()
cur.execute("DELETE FROM stock_transactions")
conn.commit()

cur.execute(preparedRegister, ("mike", "m@youtube.com", bcrypt.generate_password_hash("hi"), 5000))
conn.commit()
cur.execute(preparedRegister, ("bill", "b@google.com", bcrypt.generate_password_hash("there"), 5000))
conn.commit()

cur.execute(preparedStock, ("m@youtube.com", "AAPL", 180.3, 2, "BUY"))
conn.commit()
cur.execute(preparedStock, ("m@youtube.com", "AAPL", 180.3, -2, "SELL"))
conn.commit()
cur.execute(preparedStock, ("m@youtube.com", "GOOG", 1111.111, 3, "BUY"))
conn.commit()

cur.execute(preparedStock, ("b@google.com", "GOOG", 1111.111, 3, "BUY"))
conn.commit()

# cur.execute(preparedTransactionLog, ("youtube.com", ))
# result = cur.fetchone()
# print(result)

# cur.execute(preparedTransactionLog, ("google.com", ))
# result = cur.fetchone()
# print(result)
