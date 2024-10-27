import sys
import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QDialog, QFileDialog, QMessageBox, QTableWidgetItem, QGraphicsView, QGraphicsScene, QGraphicsRectItem, QGraphicsTextItem
from PyQt6.QtGui import QPixmap
from Main_Window import Ui_Main
from DataBases import Database_With_Users, User_Database
from Profile import Ui_Profile
from PIL import Image
from Create_table import Ui_Create_table
from PyQt6.QtGui import QBrush, QColor

class Visual_PO_for_DB(QMainWindow, Ui_Main):
    def __init__(self):
        super().__init__()
        super().setupUi(self)
        self.open_page_login()
        self.initUI()
        self.users = Database_With_Users()

    def initUI(self):
        self.setWindowTitle('VizSQL')
        self.newuser_button_2.clicked.connect(self.open_page_registration)
        self.newuser_button_3.clicked.connect(self.log_in_new_user)
        self.log_in_button.clicked.connect(self.log_in)
        self.return_log_in_button.clicked.connect(self.open_page_login)

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

    def open_page_main(self):
        self.VizSQL.setCurrentIndex(2)
        self.directory = f'users/{self.user[2]}'
        if os.listdir(f'{self.directory}/databases'):
            self.user_db = User_Database(self.user[2], os.listdir(f'{self.directory}/databases')[0])
        else:
            self.user_db = User_Database(self.user[2], f'{self.user[2]}.db')
        print(self.user)

        self.down_menu.setCurrentIndex(0)
        self.createdatabase_button.clicked.connect(lambda _: self.down_menu.setCurrentIndex(3))
        self.save_new_database_button.clicked.connect(self.create_user_databases)
        self.Log_out_button.clicked.connect(self.open_page_login)
        self.profile_button.clicked.connect(self.open_profile_dialog_window)
        self.createtable_button.clicked.connect(self.open_create_table_windows)
        self.scene = QGraphicsScene(self)
        self.graphicsView.setScene(self.scene)
        self.user_db.load_tables_from_db(self.scene)

    def open_create_table_windows(self):
        self.create_table_window = QDialog()
        self.create_table = Ui_Create_table()
        self.create_table.setupUi(self.create_table_window)
        self.create_table.name_used_database.setText(f'{self.user_db.get_name()}')
        self.create_table.save_create_pole_button.clicked.connect(self.create_pole)
        self.create_table.table_with_pole.setColumnCount(10)
        self.create_table.table_with_pole.setHorizontalHeaderLabels(
            ['название', 'тип', 'ключ', 'AutoIncrement', 'Binary', 'Not Null', 'Unsignet', 'Uniqure', 'Zero Fill',
             'Defaut'])
        self.create_table.type_pole.addItems(["INTEGER", "TEXT", "REAL", "BLOB"])
        self.create_table.Not_Key.toggled.connect(self.choose_not_key)
        self.create_table.PrimaryKey_Button.toggled.connect(self.choose_primary_key)
        self.create_table.ForeignKey_Button_2.toggled.connect(self.choose_foreign_key)
        self.create_table.type_pole.clear()
        self.create_table.save_create_pole_button(self.create_pole_in_tables)
        self.create_table.save_create_table_button.clicked.connect(self.save_and_close_create_table_windows)
        self.pols = []
        self.create_table_window.exec()

    def create_pole_in_tables(self):
        if self.create_table.Not_Key.toggle():
            dict_pole = {'название': self.create_table.name_pole.text(), 'тип': self.create_table.type_pole.currentText(),
                         'ключ': not self.create_table.Not_Key.toggle(),
                         'AutoIncrement': self.create_table.AutoIncrement.isChecked(),
                         'Binary': self.create_table.Binary.isChecked(),
                         'Not Null': self.create_table.NotNull.isChecked(),
                         'Unsignet': self.create_table.Unsignet.isChecked(),
                         'Uniqure': self.create_table.Uniqure.isChecked(),
                         'Zero Fill': self.create_table.Zerofill.isChecked(),
                         'Defaut': self.create_table.Defaut.isChecked()}
        elif self.create_table.Not_Key.toggle():
            pass
        elif self.create_table.Not_Key.toggle():
            pass
        self.pols.append(dict_pole)


    def choose_not_key(self):
        try:
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

    def choose_primary_key(self):
        try:
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

    def choose_foreign_key(self):
        try:
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

    def choose_table_PK(self):
        try:
            self.create_table.pole_ForeignKey.clear()
            primary_keys = self.user_db.get_primary_key_tables(
                self.create_table.table_ForeignKey.currentText())
            self.create_table.pole_ForeignKey.addItems(
                primary_keys if primary_keys else ['нет первичных ключей'])
        except Exception as f:
            pass


    def create_pole(self):
        name_table = self.create_table.name_pole.text()

    def save_and_close_create_table_windows(self):
        if self.create_table.name_table.text() and self.create_table.table_with_pole.rowCount() > 0:
            self.user_db.create_custom_table(self.create_table.name_table.text(), self.pols)
            self.create_table_window.close()
            self.open_page_main()
        else:
            print('kkskx')


    def open_profile_dialog_window(self):
        self.profile_window = QDialog()
        self.profile_window_ui = Ui_Profile()
        self.profile_window_ui.setupUi(self.profile_window)
        self.profile_window_ui.user_name_profile.setText(f'{self.user[1]}')
        self.profile_window_ui.profile_image.clear()
        if not os.listdir(f'{self.directory}/image_profile/'):
            self.profile_window_ui.profile_image.setText('Нет изображения')
        else:
            image = QPixmap(f'{self.directory}/image_profile/image_profile.png')
            self.profile_window_ui.profile_image.setPixmap(image)
        self.profile_window_ui.name_profile_text.setText(f'{self.user[1]}!')
        self.profile_window_ui.name_login_text.setText(f'{self.user[2]}')
        self.profile_window_ui.change_image_button.clicked.connect(self.change_and_save_image_profile)
        self.profile_window_ui.save_create_pole.clicked.connect(self.save_and_close_profile_windows)
        self.profile_window.exec()


    # Создание собственной директории для пользователя
    def create_users_directory(self):
        os.makedirs(f'{os.getcwd()}/users/{self.user[2]}')
        os.makedirs(f'{os.getcwd()}/users/{self.user[2]}/databases')
        os.makedirs(f'{os.getcwd()}/users/{self.user[2]}/image_profile')

    def change_and_save_image_profile(self):
        image = QFileDialog.getOpenFileName(self, 'Выбрать картинку', '')[0]
        if image:
            try:
                img = Image.open(image).resize((250, 250))
                save_path = os.path.join(f'{self.directory}/image_profile', 'image_profile.png')
                img.save(save_path)
                image = QPixmap(save_path)
                self.profile_window_ui.profile_image.setPixmap(image)
            except IOError:
                QMessageBox.warning(self, "Ошибка", "Выбранный файл не является изображением.")
        else:
            QMessageBox.warning(self, "Ошибка", "Файл не выбран.")


    def create_user_databases(self):
        self.error_create_database_text.setVisible(False)
        log_in_except = {lambda: self.check_new_database.isChecked(): 'Нажатие на квадратик обязательное условие',
                         lambda: self.name_new_database.text(): 'Название должно быть больше 4 символов и содержать буквы и цифры',
                         lambda: not os.path.exists(f'{self.directory}/databases/{self.name_new_database.text()}.db'): 'База данных с таким названием уже существует',
                         }
        text_except = self.return_text_exception(log_in_except)
        if text_except:
            self.error_create_database_text.setVisible(True)
            self.error_create_database_text.setText('Введите название вашей базы данных')
        else:
            self.user_db.close()
            self.user_db = User_Database(self.user[2], self.name_new_database.text() + '.db')
            QMessageBox.information(self, "Создание завершено", f"База данных {self.name_new_database.text()} создана")
            self.name_new_database.setText('')
            self.check_new_database.setChecked(False)
            self.down_menu.setCurrentIndex(0)
            self.open_page_main()


    def save_and_close_profile_windows(self):
        self.users.update_name_users(self.profile_window_ui.user_name_profile.text(), self.user[0])
        self.user = self.users.find_user(self.user[2], self.user[3])
        self.profile_window.close()

    def log_in(self):
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


    def return_text_exception(self, dict_except):
        for exception, text in dict_except.items():
            try:
                if not exception():
                    return text
            except Exception as d:
                print(text)
                print(exception())
                print(d.__class__.__name__)
        return False


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Visual_PO_for_DB()
    ex.show()
    sys.exit(app.exec())