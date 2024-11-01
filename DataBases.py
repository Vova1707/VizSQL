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
        if user:
            return user
        else:
            return False

    def close(self):
        self.connection.close()





class User_Database:
    def __init__(self, user_login, name_database):
        self.connection = sqlite3.connect(f'users/{user_login}/databases/{name_database}')
        self.cursor = self.connection.cursor()
        self.name = name_database

    def create_table(self, table_name, polses):
        pols = []
        foreign_key = []
        for pole in polses:
            pole_text = pole['название'] + ' ' + pole['тип']
            if pole['ключ'] == 'Первичный':
                pole_text += ' PRIMARY KEY'
            elif pole['ключ'] == 'Вторичный':
                pole_text += ' PRIMARY KEY'
                foreign_key.append(
                    f'FOREIGN KEY ({pole['название']}) REFERENCES {pole['Таблица первичного ключа']}({pole['Поле первичного ключа']})')
            else:
                if pole['Not Null']:
                    pole_text += ' NOT NULL'
                if pole['AutoIncrement']:
                    pole_text += ' AUTOINCREMENT'
                if pole['Binary']:
                    pole_text += ' BINARY'
                if pole['Unsignet']:
                    pole_text += ' UNSIGNET'
                if pole['Zero Fill']:
                    pole_text += ' ZERO FILL'
            pols.append(pole_text)
        create_table = f'CREATE TABLE IF NOT EXISTS {table_name} (' + ', '.join(pols + foreign_key) + ')'
        try:
            self.cursor.execute(create_table)
            self.connection.commit()
            return True
        except Exception as d:
            print(create_table)
            print(d.__class__.__name__)
            return False


    def delete_table(self, name):
        try:
            self.cursor.execute(f'''DROP TABLE {name}''')
            self.connection.commit()
            return True
        except Exception as d:
            print(d.__class__.__name__)
            return False

    def get_tables(self):
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = self.cursor.fetchall()
        return tables

    def get_primary_key_tables(self, table_name):
        self.cursor.execute(f"PRAGMA table_info({table_name})")
        info = self.cursor.fetchall()
        primary_keys = [pole[1] for pole in info if pole[5] and pole[2].upper() == 'INTEGER']
        return primary_keys

    def table_info(self, table_name):
        self.cursor.execute(f'PRAGMA table_info({table_name});').fetchall()

    def get_foreign_keys(self, table_name):
        self.cursor.execute(f"PRAGMA foreign_key_list({table_name})")
        a = self.cursor.fetchall()
        return a

    def close(self):
        self.connection.close()

    def get_name(self):
        return self.name