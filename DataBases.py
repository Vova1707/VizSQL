import sqlite3
from PyQt6.QtWidgets import QApplication, QMainWindow, QDialog, QFileDialog, QMessageBox, QTableWidgetItem, QGraphicsView, QGraphicsScene, QGraphicsRectItem, QGraphicsTextItem
from PyQt6.QtGui import QBrush, QColor


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
    def __init__(self, user_login, name_database):
        self.connection = sqlite3.connect(f'users/{user_login}/databases/{name_database}')
        self.cursor = self.connection.cursor()
        self.name = name_database
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

    def create_custom_table(self, table_name, fields_with_properties):
        pols = []
        for field_name, properties in fields_with_properties.items():
            column_definition = field_name + ' ' + properties['type']
            if properties['primary_key']:
                column_definition += ' PRIMARY KEY'
            if properties['not_null']:
                column_definition += ' NOT NULL'
            if properties['unique']:
                column_definition += ' UNIQUE'
            if properties['binary']:
                column_definition += ' BLOB'
            if properties['unsigned']:
                column_definition += ' UNSIGNED'
            if properties['zero_fill']:
                column_definition += ' ZEROFILL'

            pols.append(column_definition)

        create_table_query = f'CREATE TABLE IF NOT EXISTS {table_name} (' + ', '.join(pols) + ')'
        try:
            self.cursor.execute(create_table_query)
            self.connection.commit()
        except Exception as d:
            print(d.__class__.__name__)


    def load_tables_from_db(self, scene):
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = self.cursor.fetchall()

        for table in tables:
            table_name = table[0]
            self.cursor.execute(f'PRAGMA table_info({table_name});')
            fields_info = self.cursor.fetchall()
            fields = [f"{field[1]}: {field[2]}" for field in fields_info]
            table_item = TableModelItem(table_name, fields)
            scene.addItem(table_item)
            table_item.setPos(20, 20 + len(scene.items()) * 120)

    def delete_table(self):
        pass

    def close(self):
        self.connection.close()

    def get_name(self):
        return self.name


class TableModelItem(QGraphicsRectItem):
    def __init__(self, table_name, fields):
        super().__init__(0, 0, 150, 300)
        self.setBrush(QBrush(QColor(200, 200, 255)))
        self.setFlag(QGraphicsRectItem.GraphicsItemFlag.ItemIsMovable)
        self.table_title = QGraphicsTextItem(table_name, self)
        self.table_title.setPos(10, 10)

        for i, field in enumerate(fields):
            field_item = QGraphicsTextItem(field, self)
            field_item.setPos(10, 30 + i * 20)