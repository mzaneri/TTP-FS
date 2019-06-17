import sqlite3

from app.sql import preparedSignUp, preparedStock, preparedTransactionLog

conn = sqlite3.connect("database.sqlite", check_same_thread=False)
cur = conn.cursor()

cur.execute("DELETE FROM users")
conn.commit()
cur.execute("DELETE FROM stock_transactions")
conn.commit()

cur.execute(preparedSignUp, ("mike", "youtube.com", "hi", 5000))
conn.commit()
cur.execute(preparedSignUp, ("bill", "google.com", "there", 5000))
conn.commit()

cur.execute(preparedStock, ("youtube.com", "YOU", 20.3, 2))
conn.commit()
cur.execute(preparedStock, ("youtube.com", "YOU", 20.3, -2))
conn.commit()

cur.execute(preparedStock, ("google.com", "GOOG", 24.6, 5))
conn.commit()

# cur.execute(preparedTransactionLog, ("youtube.com", ))
# result = cur.fetchone()
# print(result)

# cur.execute(preparedTransactionLog, ("google.com", ))
# result = cur.fetchone()
# print(result)

conn.close()
