import sqlite3
import time


class Database:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY, mute_time INTEGER)")

    def examination(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,)).fetchall()
            return bool(len(result))

    def add(self, user_id):
        with self.connection:
            return self.cursor.execute("INSERT INTO users (user_id, mute_time) VALUES (?, ?)", (user_id, 0))

    def mute(self, user_id):
        with self.connection:
            user = self.cursor.execute("SELECT mute_time FROM users WHERE user_id = ?", (user_id,)).fetchone()
            return int(user[0]) >= int(time.time())

    def add_mute(self, user_id, mute_time):
        with self.connection:
            return self.cursor.execute("UPDATE users SET mute_time = ? WHERE user_id = ?", (int(time.time() + mute_time), user_id))

    def clear_mute(self, user_id):
        with self.connection:
            return self.cursor.execute("UPDATE users SET mute_time = ? WHERE user_id = ?", (0, user_id))

    def close(self):
        self.connection.close()