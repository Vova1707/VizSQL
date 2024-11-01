import sys
import os
from PyQt6.QtWidgets import QApplication, QPushButton, QLineEdit, QMainWindow, QDialog, QFileDialog, QMessageBox, QTableWidgetItem, QGraphicsView, QGraphicsScene, QGraphicsRectItem, QGraphicsTextItem, QTableWidgetItem, QGraphicsItem
from PyQt6.QtGui import QPixmap
from Main_Window import Ui_Main
from DataBases import User_Database, Database_With_Users
from Profile import Ui_Profile
from PIL import Image
from Create_table import Ui_Create_table
from Data import Ui_Dialog
import sqlite3
from PyQt6.QtGui import QBrush, QColor, QPen
from PyQt6.QtCore import Qt


class Visual_PO_for_DB(QMainWindow, Ui_Main):
    def __init__(self):
        super().__init__()
        super().setupUi(self)
        self.open_page_login()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('VizSQL')
        self.newuser_button_2.clicked.connect(self.open_page_registration)
        self.newuser_button_3.clicked.connect(self.log_in_new_user)
        self.log_in_button.clicked.connect(self.log_in)
        self.return_log_in_button.clicked.connect(self.open_page_login)
        self.users = Database_With_Users()
        self.create_table_window = False



    '''Главная страница'''
    def open_page_main(self):# Открытие главной страницы
        self.VizSQL.setCurrentIndex(2)
        self.createdatabase_button.clicked.connect(lambda _: self.down_menu.setCurrentIndex(3))
        self.deletedatabase_button.clicked.connect(lambda _: self.down_menu.setCurrentIndex(1))
        self.deletedatabase_button.clicked.connect(lambda _: self.down_menu.setCurrentIndex(2))
        self.deletedatabase_button_2.clicked.connect(lambda _: self.down_menu.setCurrentIndex(4))
        self.down_menu.setCurrentIndex(0)
        self.directory = f'users/{self.user[2]}'
        if os.listdir(f'{self.directory}/databases'):
            self.user_db = User_Database(self.user[2], os.listdir(f'{self.directory}/databases')[0])
        else:
            self.user_db = User_Database(self.user[2], f'{self.user[2]}.db')
        print(self.user)
        """Сигналы кнопок"""
        self.download_button.clicked.connect(self.load_database)
        self.createtable_button.clicked.connect(self.open_create_table_windows)
        self.profile_button.clicked.connect(self.open_profile_dialog_window)
        self.save_new_database_button.clicked.connect(self.create_user_databases)
        self.deletedatabase_button_2.clicked.connect(self.open_delete_table_window)
        """Создание представления таблиц"""
        self.scene = QGraphicsScene(self)
        self.lines = []
        self.graphicsView.setScene(self.scene)
        self.load_tables_from_db()

    def load_tables_from_db(self):
        self.tables = self.user_db.get_tables()
        print(self.tables)
        self.models_table = {}
        for table in self.tables:
            table_name = table[0]
            fields_info = self.user_db.cursor.execute(f'PRAGMA table_info({table_name});').fetchall()
            fields = [f"{info[1]}: {info[2]}" for info in fields_info]
            table_item = TableModelItem(table_name, fields, self)
            self.models_table[table_name] = table_item
            self.scene.addItem(table_item)
            table_item.setPos(20, 20 + 120 * len(self.models_table))
        self.create_connections()

    def create_connections(self):
        for table in self.tables:
            table_name = table[0]
            foreign_keys = self.user_db.get_foreign_keys(table_name)
            for key in foreign_keys:
                if key[2] in self.models_table.keys():
                    self.draw_connection(self.models_table[table_name], self.models_table[key[2]])

    def draw_connection(self, model1, model2):
        line = self.scene.addLine(model1.x() + model1.rect().width() / 2,
                                  model1.y() + model1.rect().height(),
                                  model2.x() + model2.rect().width() / 2,
                                  model2.y(),
                                  QPen(QColor(200, 100, 0), 2))
        self.lines.append(line)

    def update_lines(self):
        for line in self.lines:
            self.scene.removeItem(line)
        self.lines.clear()
        for model1_name, model1 in self.models_table.items():
            foreign_keys = self.user_db.get_foreign_keys(model1_name)
            for key in foreign_keys:
                if key[2] in self.models_table.keys():
                    model2 = self.models_table[key[2]]
                    line = self.scene.addLine(
                        model1.x() + model1.rect().width() / 2,
                        model1.y() + model1.rect().height(),
                        model2.x() + model2.rect().width() / 2,
                        model2.y(),
                        QPen(QColor(200, 100, 0), 2)
                    )
                    self.lines.append(line)

    '''окно с данными таблиц'''
    def open_data_table_window(self):# открытие окна
        self.data_table_windows = QDialog()
        self.data_table = Ui_Dialog()
        self.data_table.setupUi(self.data_table_windows)
        table = [i[0] for i in self.user_db.get_tables()]
        self.data_table.table.addItems(table if table else ['нет таблиц'])
        self.data_table.change_table_button.clicked.connect(self.data_for_table)
        self.data_table_windows.exec()

    def data_for_table(self):
        try:
            table_name = self.data_table.table.currentText()
            data = self.user_db.cursor.execute(f'PRAGMA table_info({table_name});').fetchall()
            self.data_table.table_data.setColumnCount(len(list(data[0])))
        except Exception as d:
            print(len(list(data[0])))
            print(d.__class__.__name__)


    '''Удаление Базы данных'''
    def open_delete_database_window(self):
        pass

    '''Удаление таблицы'''
    def open_delete_table_window(self):
        tables = [i[0] for i in self.user_db.get_tables()]
        self.table_delete.clear()
        print(tables)
        if tables:
            self.table_delete.addItems(tables)
        else:
            self.table_delete.addItems(['Нет доступных таблиц'])
        self.delete_and_save_table.clicked.connect(self.delete_and_save_button)


    def delete_and_save_button(self):
        name = self.table_delete.currentText()
        if self.user_db.delete_table(name):
            self.open_page_main()

    '''Открытие новой базы данных'''
    def load_database(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Выберите файл", "",
                                                       "Database Files (*.db);;All Files (*)")
        if file_path:
           file_name = os.path.splitext(os.path.basename(file_path))[0]
           self.load_database_2(file_name, file_path)

    def load_database_2(self, file_name, file_path):
        try:
            if os.path.exists(os.path.join(self.directory + '/databases', file_name + '.db')):
                score = 0
                while os.path.exists(os.path.join(self.directory + '/databases', file_name + f'_{score}.db')):
                    score += 1
                os.rename(file_path, os.path.join(self.directory + '/databases', file_name + f'_{score}.db'))
                file_name = file_name + f'_{score}'
            else:
                os.rename(file_path, os.path.join(self.directory + '/databases', file_name + f'.db'))
            self.user_db.close()
            self.user_db = User_Database(self.user[2], file_name + '.db')
            self.open_page_main()
        except:
            QMessageBox.warning(self, 'Ошибка', 'Что-то пошло не так')

    '''Создание новой базы данных'''

    def create_user_databases(self):
        self.error_create_database_text.setVisible(False)
        log_in_except = {lambda: self.check_new_database.isChecked(): 'Нажатие на квадратик обязательное условие',
                         lambda: self.name_new_database.text(): 'Название должно быть больше 4 символов и содержать буквы и цифры',
                         lambda: not os.path.exists(f'{self.directory}/databases/{self.name_new_database.text()}.db'): 'База данных с таким названием уже существует',
                         }
        text_except = self.return_text_exception(log_in_except)
        if text_except:
            self.error_create_database_text.setVisible(True)
            self.error_create_database_text.setText(text_except)
        else:
            self.user_db.close()
            self.user_db = User_Database(self.user[2], self.name_new_database.text() + '.db')
            QMessageBox.information(self, "Создание завершено", f"База данных {self.name_new_database.text()} создана")
            self.name_new_database.setText('')
            self.check_new_database.setChecked(False)
            # self.create_table.error_create_table.setVisible(True)
            self.down_menu.setCurrentIndex(0)
            self.open_page_main()

    '''Окно для создания таблицы'''

    def open_create_table_windows(self):# Открытие окна
        if not self.create_table_window:
            self.create_table_window = QDialog()
            self.create_table = Ui_Create_table()
            self.create_table.setupUi(self.create_table_window)
            self.create_table.PrimaryKey_Button.toggled.connect(self.choose_primary_key)
            self.create_table.ForeignKey_Button_2.toggled.connect(self.choose_foreign_key)
            self.create_table.save_create_pole_button.clicked.connect(self.create_pole_in_tables)
            self.create_table.save_create_table_button.clicked.connect(self.save_and_close_create_table_windows)
            self.create_table.save_create_pole_button.clicked.connect(self.create_pole)
            self.create_table.Not_Key.toggled.connect(self.choose_not_key)
            self.create_table.table_with_pole.clear()
            self.create_table.table_with_pole.setRowCount(0)
            self.create_table.name_table.setText('')
            self.create_table.name_pole.setText('')
            self.create_table.name_used_database.setText(f'{self.user_db.get_name()}')
            self.create_table.table_with_pole.setColumnCount(13)
            self.create_table.table_with_pole.setHorizontalHeaderLabels(
                ['название', 'тип', 'ключ', 'AutoIncrement', 'Binary', 'Not Null', 'Unsignet', 'Uniqure', 'Zero Fill',
                 'Defaut', 'Таблица 1 ключа', 'поле 1 ключа', 'Удалить'])
            self.create_table.type_pole.addItems(["INTEGER", "TEXT", "REAL", "BLOB"])
            self.create_table.type_pole.clear()
            self.create_table.Not_Key.setChecked(True)
            self.create_table.error_create_table.setVisible(False)
            self.pols = []
            self.key = False
        self.create_table_window.exec()

    def save_and_close_create_table_windows(self):
        if self.create_table_window:
            self.create_table_window.exec()
            if (self.user_db.create_table(self.create_table.name_table.text(),
                                          self.pols) and self.create_table.name_table.text() and
                    self.create_table.table_with_pole.rowCount):
                self.create_table_window.close()
                self.create_table_window = None
                self.create_table = None
                self.open_page_main()
            else:
                self.create_table.error_create_table.setVisible(True)
                self.create_table.error_create_table.setText('Возникла ошибка в добавлении таблицы')

    def create_pole_in_tables(self):# Создание нового поля у таблицы


        def check_true(signal):# Быстрая обработка False и True
            return 'да' if signal else 'нет'


        if self.create_table.name_pole.text():
            self.create_table.table_with_pole.setRowCount(self.create_table.table_with_pole.rowCount() + 1)
            dict_pole = {'название': self.create_table.name_pole.text(),
                         'тип': self.create_table.type_pole.currentText(),
                         'ключ': self.key,
                         'AutoIncrement': self.create_table.AutoIncrement.isChecked(),
                         'Binary': self.create_table.Binary.isChecked(),
                         'Not Null': self.create_table.NotNull.isChecked(),
                         'Unsignet': self.create_table.Unsignet.isChecked(),
                         'Uniqure': self.create_table.Uniqure.isChecked(),
                         'Zero Fill': self.create_table.Zerofill.isChecked(),
                         'Defaut': self.create_table.Defaut.text(),
                         'Таблица первичного ключа': self.create_table.table_ForeignKey.currentText() if self.key == 'Вторичный' else False,
                         'Поле первичного ключа': self.create_table.pole_ForeignKey.currentText() if self.key == 'Вторичный' else False,
                         }
            keys = list(dict_pole.keys())
            self.pols.append(dict_pole)
            for i in range(12):
                a = check_true(dict_pole[keys[i]]) if dict_pole[keys[i]] in [True, False] else dict_pole[keys[i]]
                try:
                    item = QLineEdit()
                    item.setText(a)
                    item.setEnabled(False)
                    self.create_table.table_with_pole.setCellWidget(self.create_table.table_with_pole.rowCount() - 1, i,
                                                                    item)
                except Exception as d:
                    print(d.__class__.__name__)
            try:
                button = QPushButton()
                button.setText('Удалить')
                num = self.create_table.table_with_pole.rowCount() - 1
                button.clicked.connect(lambda _: self.delete_pole(num))
                self.create_table.table_with_pole.setCellWidget(self.create_table.table_with_pole.rowCount() - 1, 12,
                                                                button)
            except Exception as s:
                print(s.__class__.__name__)
        else:
            self.create_table.error_create_table.setVisible(True)
            self.create_table.error_create_table.setText('Некорректное имя поля')

    def delete_pole(self, num):# Удаление поля у новой таблицы
        self.create_table.table_with_pole.removeRow(num)
        del self.pols[num]



    def choose_not_key(self):# Выбор(Поле это не ключ)
        try:
            self.key = False
            self.create_table.type_pole.clear()
            self.create_table.pole_ForeignKey.clear()
            self.create_table.table_ForeignKey.clear()
            self.create_table.type_pole.addItems(["INTEGER", "TEXT", "REAL", "BLOB"])
            self.create_table.NotNull.setChecked(False)
            self.create_table.Uniqure.setChecked(False)
            self.create_table.NotNull.setEnabled(True)
            self.create_table.Uniqure.setEnabled(True)
            self.create_table.Binary.setEnabled(True)
            self.create_table.Zerofill.setEnabled(True)
            self.create_table.Unsignet.setEnabled(True)
            self.create_table.table_ForeignKey.setEnabled(False)
            self.create_table.pole_ForeignKey.setEnabled(False)
        except Exception as f:
            print(f.__class__.__name__)

    def choose_primary_key(self):# Выбор(Поле это первичный ключ)
        try:
            self.key = 'Первичный'
            self.create_table.pole_ForeignKey.clear()
            self.create_table.type_pole.clear()
            self.create_table.table_ForeignKey.clear()
            self.create_table.type_pole.addItems(["INTEGER"])
            self.create_table.table_ForeignKey.setEnabled(False)
            self.create_table.pole_ForeignKey.setEnabled(False)
            self.create_table.NotNull.setChecked(True)
            self.create_table.Uniqure.setChecked(True)
            self.create_table.NotNull.setEnabled(False)
            self.create_table.Uniqure.setEnabled(False)
            self.create_table.Binary.setEnabled(False)
            self.create_table.Zerofill.setEnabled(False)
            self.create_table.Unsignet.setEnabled(False)
        except Exception as f:
            print(f.__class__.__name__)

    def choose_foreign_key(self):# Выбор(Поле это вторичный ключ)
        try:
            self.key = 'Вторичный'
            self.create_table.table_ForeignKey.setEnabled(True)
            self.create_table.pole_ForeignKey.setEnabled(True)
            self.create_table.type_pole.clear()
            self.create_table.type_pole.addItems(["INTEGER"])
            self.create_table.table_ForeignKey.clear()
            table = [i[0] for i in self.user_db.get_tables()]
            self.create_table.table_ForeignKey.addItems(table if table else ['нет таблиц'])
            self.create_table.table_ForeignKey.currentIndexChanged.connect(self.choose_table_PK)
            self.create_table.NotNull.setChecked(True)
            self.create_table.Uniqure.setChecked(True)
            self.create_table.NotNull.setEnabled(False)
            self.create_table.Uniqure.setEnabled(False)
            self.create_table.Binary.setEnabled(False)
            self.create_table.Zerofill.setEnabled(False)
            self.create_table.Unsignet.setEnabled(False)
        except Exception as f:
            print(f.__class__.__name__)

    def choose_table_PK(self):# Добавление выбора зависимого поля для вторичного ключа при выборе зависимой таблицы
        try:
            self.create_table.pole_ForeignKey.clear()
            primary_keys = self.user_db.get_primary_key_tables(
                self.create_table.table_ForeignKey.currentText())
            self.create_table.pole_ForeignKey.addItems(
                primary_keys if primary_keys else ['нет первичных ключей'])
        except Exception as f:
            pass


    def create_pole(self):#
        name_table = self.create_table.name_pole.text()

    '''def save_and_close_create_table_windows(self):# Закрыть окно создания таблицы

        if (self.user_db.create_table(self.create_table.name_table.text(), self.pols) and self.create_table.name_table.text() and
                self.create_table.table_with_pole.rowCount):
            self.create_table_window.close()
            self.create_table_window = None
            self.create_table = None
            self.open_page_main()
        else:
            self.create_table.error_create_table.setVisible(True)
            self.create_table.error_create_table.setText('Возникла ошибка в добавлении таблицы')'''

    '''Окно Профиля'''

    def open_profile_dialog_window(self):
        if not hasattr(self, 'profile_window'):
            self.profile_window = QDialog()
            self.profile = Ui_Profile()
            self.profile.setupUi(self.profile_window)
            self.profile.change_image_button.clicked.connect(self.change_and_save_image_profile)
            self.profile.save_create_pole.clicked.connect(self.save_and_close_profile_windows)
        if not os.listdir(f'{self.directory}/image_profile/'):
            self.profile.profile_image.setText('Нет изображения')
        else:
            image = QPixmap(f'{self.directory}/image_profile/image_profile.png')
            self.profile.profile_image.setPixmap(image)
        self.profile.name_profile_text.setText(f'{self.user[1]}!')
        self.profile.name_login_text.setText(f'{self.user[2]}')
        self.profile_window.exec()

    def change_and_save_image_profile(self):# Выбрать картинку у профиля
        image = QFileDialog.getOpenFileName(self, 'Выбрать картинку', '')[0]
        if image:
            try:
                img = Image.open(image).resize((250, 250))
                save_path = os.path.join(f'{self.directory}/image_profile', 'image_profile.png')
                img.save(save_path)
                image = QPixmap(save_path)
                self.profile.profile_image.setPixmap(image)
            except IOError:
                QMessageBox.warning(self, "Ошибка", "Выбранный файл не является изображением.")
        else:
            QMessageBox.warning(self, "Ошибка", "Файл не выбран.")


    def save_and_close_profile_windows(self):# Закрыть окно профиля
        self.users.update_name_users(self.profile.user_name_profile.text(), self.user[0])
        self.user = self.users.find_user(self.user[2], self.user[3])
        self.profile_window.close()

    '''Функции авторизозации пользователя'''

    def open_page_login(self):
        self.VizSQL.setCurrentIndex(0)
        self.login.setText('')
        self.password.setText('')
        self.error_Log_in_text.setVisible(False)
        self.user = None

    def open_page_registration(self):
        self.newuser_name.setText('')
        self.newuser_login.setText('')
        self.newuser_password_2.setText('')
        self.VizSQL.setCurrentIndex(1)
        self.newuser_error_text.setVisible(False)

    def log_in(self):# Вход в существующий аккаунт
        log_in_except = {lambda: len(self.login.text()) > 7 and not self.login.text().isdigit()
                                 and not self.login.text().isalpha(): 'Логин должен быть не чем из менее 8 символов \n и состоять из букв и цифр',
                       lambda: len(self.password.text()) > 5 and not self.password.text().isdigit()
                                 and not self.password.text().isalpha(): 'Пароль должен быть не менее чем 6 символов \n и состоять из букв и цифр',
                       lambda: self.users.find_user(self.login.text(), self.password.text()): 'Пользователь не найден',
                       }
        text_except = self.return_text_exception(log_in_except)
        if text_except:
            self.error_Log_in_text.setVisible(True)
            self.error_Log_in_text.setText(text_except)
        else:
            self.user = self.users.find_user(self.login.text(), self.password.text())
            self.open_page_main()


    def log_in_new_user(self):# Функция для регистрации нового пользователя
        log_in_except = {lambda: len(self.newuser_name.text()) > 4: 'Имя должно быть не чем из менее 5 символов',
                         lambda: len(self.newuser_login.text()) > 7 and not self.newuser_login.text().isdigit()
                                 and not self.newuser_login.text().isalpha(): 'Логин должен быть не чем из менее 8 символов \n и состоять из букв и цифр',
                         lambda: len(self.newuser_password_2.text()) > 5 and not self.newuser_password_2.text().isdigit() and not self.newuser_password_2.text().isalpha(): 'Пароль должен быть не менее чем 6 символов \n и состоять из букв и цифр',
                         lambda: self.CHECK.isChecked(): 'Нажатие на квадратик обязательное условие',
                         lambda: self.users.add_user(self.newuser_name.text(), self.newuser_login.text(), self.newuser_password_2.text()): 'Пользователь с таким логином уже существует',
                         }

        text_except = self.return_text_exception(log_in_except)
        if text_except:
            self.newuser_error_text.setText(text_except)
            self.newuser_error_text.setVisible(True)
        else:
            self.user = self.users.find_user(self.newuser_login.text(), self.newuser_password_2.text())
            self.create_users_directory()
            self.open_page_main()

    def create_users_directory(self):# Создание собственной директории для пользователя
        os.makedirs(f'{os.getcwd()}/users/{self.user[2]}')
        os.makedirs(f'{os.getcwd()}/users/{self.user[2]}/databases')
        os.makedirs(f'{os.getcwd()}/users/{self.user[2]}/image_profile')

    '''Различные функции для более удобной работы с приложением'''
    def return_text_exception(self, dict_except):# Возвращает текс ошибки если такая есть
        for exception, text in dict_except.items():
            try:
                if not exception():
                    return text
            except Exception as d:
                print(d.__class__.__name__)
        return False


class TableModelItem(QGraphicsRectItem):# Модель представления таблицы
    def __init__(self, table_name, fields, main_window):
        super().__init__(0, 0, 150, 60 + 20 * len(fields))
        self.setBrush(QBrush(QColor(200, 200, 255)))
        self.setFlag(QGraphicsRectItem.GraphicsItemFlag.ItemIsMovable)
        self.setFlag(QGraphicsRectItem.GraphicsItemFlag.ItemSendsGeometryChanges)
        self.table_title = QGraphicsTextItem(table_name, self)
        self.table_title.setPos(10, 10)
        self.mainWindow = main_window

        for i, field in enumerate(fields):
            field_item = QGraphicsTextItem(field, self)
            field_item.setPos(10, 30 + i * 20)

    def itemChange(self, change, value):
        if change == QGraphicsItem.GraphicsItemChange.ItemPositionChange:
            self.mainWindow.update_lines()
        return super().itemChange(change, value)




if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Visual_PO_for_DB()
    ex.show()
    sys.exit(app.exec())