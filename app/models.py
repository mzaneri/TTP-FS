import sqlite3
from flask_login import UserMixin

# Custom created class for user_loader callback
class User(UserMixin):
    def __init__(self, result):
        self.name = result[1]
        self.email = result[2]
        self.password = result[3]
        self.balance = result[4]

    def get_id(self):
        return self.email
