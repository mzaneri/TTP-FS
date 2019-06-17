from app import bcrypt, conn, cur
from app.sql import preparedRegister, preparedStock, preparedTransactionLog

cur.execute("DELETE FROM users")
conn.commit()
cur.execute("DELETE FROM stock_transactions")
conn.commit()

cur.execute(preparedRegister, ("mike", "youtube.com", bcrypt.generate_password_hash("hi"), 5000))
conn.commit()
cur.execute(preparedRegister, ("bill", "google.com", bcrypt.generate_password_hash("there"), 5000))
conn.commit()

cur.execute(preparedStock, ("youtube.com", "aapl", 20.3, 2))
conn.commit()
cur.execute(preparedStock, ("youtube.com", "aapl", 20.3, -2))
conn.commit()
cur.execute(preparedStock, ("youtube.com", "goog", 24.6, 5))
conn.commit()

cur.execute(preparedStock, ("google.com", "goog", 24.6, 5))
conn.commit()

# cur.execute(preparedTransactionLog, ("youtube.com", ))
# result = cur.fetchone()
# print(result)

# cur.execute(preparedTransactionLog, ("google.com", ))
# result = cur.fetchone()
# print(result)
