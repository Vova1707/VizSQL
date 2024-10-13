import sqlite3


class Database_With_Users:
    def __init__(self, name='users.db'):
        self.connection = sqlite3.connect(name)
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute(
            '''CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                login TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL)
            '''
        )
        self.connection.commit()

    def update_name_users(self, new_name, id):
        self.cursor.execute("UPDATE users SET username = ? WHERE id = ?", (new_name, id))
        self.connection.commit()

    def add_user(self, username, login, password):
        try:
            self.cursor.execute("INSERT INTO users (username, login, password) VALUES (?, ?, ?)",
                                (username, login, password))
            self.connection.commit()
            return True
        except sqlite3.IntegrityError:
           return False

    def find_user(self, login, password):
        query = "SELECT * FROM users WHERE login = ? AND password = ?"
        self.cursor.execute(query, (login, password))
        user = self.cursor.fetchone()
        return user

    def close(self):
        self.connection.close()


class User_Database:
    def __init__(self, user_name, db_name):
        self.connection = sqlite3.connect(f'users/{user_name}/databases/{db_name}.db')
        self.cursor = self.connection.cursor()

    def create_table(self):
        pass

    def delete_table(self):
        pass