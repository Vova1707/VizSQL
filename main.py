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
        self.create_table_window_ui = Ui_Create_table()
        self.create_table_window_ui.setupUi(self.create_table_window)
        self.create_table_window_ui.name_used_database.setText(f'{self.user_db.get_name()}')
        self.create_table_window_ui.table_with_pole.setColumnCount(9)
        self.pols = {}
        self.create_table_window_ui.table_with_pole.setHorizontalHeaderLabels(['название', 'тип', 'PK', 'NN', 'UQ', 'B', 'UN', 'ZF', 'Defaut'])
        self.create_table_window_ui.type_pole.addItems(["INTEGER", "TEXT", "REAL", "BLOB"])
        self.create_table_window_ui.save_create_pole_button.clicked.connect(self.create_pole)
        self.create_table_window_ui.save_create_table_button.clicked.connect(self.save_and_close_create_table_windows)
        self.create_table_window.exec()

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

    def create_pole(self):
        name = self.create_table_window_ui.name_pole.text()
        dict_pole = {}
        dict_pole['type'] = self.create_table_window_ui.type_pole.currentText()
        dict_pole['primary_key'] = self.create_table_window_ui.PrimaryKey.isChecked()
        dict_pole['not_null'] = self.create_table_window_ui.NotNull.isChecked()
        dict_pole['unique'] = self.create_table_window_ui.Uniqure.isChecked()
        dict_pole['binary'] = self.create_table_window_ui.Binary.isChecked()
        dict_pole['unsigned'] = self.create_table_window_ui.Unsignet.isChecked()
        dict_pole['zero_fill'] = self.create_table_window_ui.Zerofill.isChecked()
        dict_pole['Defaut'] = self.create_table_window_ui.defaut.text()
        self.create_table_window_ui.NotNull.setChecked(False)
        self.create_table_window_ui.PrimaryKey.setChecked(False)
        self.create_table_window_ui.Uniqure.setChecked(False)
        self.create_table_window_ui.Binary.setChecked(False)
        self.create_table_window_ui.Unsignet.setChecked(False)
        self.create_table_window_ui.Zerofill.setChecked(False)
        self.create_table_window_ui.defaut.setText('')
        self.pols[name] = dict_pole
        list_param = list(map(lambda x: 'да' if x else 'нет', [dict_pole['primary_key'], dict_pole['not_null'],
                                                               dict_pole['unique'], dict_pole['binary'],
                                                               dict_pole['unsigned'], dict_pole['zero_fill']]))
        row_count = self.create_table_window_ui.table_with_pole.rowCount()
        a = [name, dict_pole['type'], *list_param, dict_pole['Defaut']]
        self.create_table_window_ui.table_with_pole.insertRow(row_count)
        for i in range(len(a)):
            self.create_table_window_ui.table_with_pole.setItem(row_count, i, QTableWidgetItem(f'{a[i]}'))

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
        if self.check_new_database.isChecked():
            if self.name_new_database.text():
                if not os.path.exists(f'{self.directory}/databases/{self.name_new_database.text()}.db'):
                    self.user_db = User_Database(self.user[2], self.name_new_database.text() + '.db')
                    QMessageBox.information(self, "Создание завершено", f"База данных {self.name_new_database.text()} создана")
                    self.name_new_database.setText('')
                    self.check_new_database.setChecked(False)
                    self.down_menu.setCurrentIndex(0)
                    self.open_page_main()
                else:
                    self.error_create_database_text.setText('База данных с таким названием уже существует')
            else:
                self.error_create_database_text.setText('Введите название вашей базы данных')
        else:
            self.error_create_database_text.setText('Нажмите на квадратик')


    def save_and_close_profile_windows(self):
        self.users.update_name_users(self.profile_window_ui.user_name_profile.text(), self.user[0])
        self.user = self.users.find_user(self.user[2], self.user[3])
        self.profile_window.close()

    def save_and_close_create_table_windows(self):
        if self.create_table_window_ui.name_table.text() and self.create_table_window_ui.table_with_pole.rowCount() > 0:
            self.user_db.create_custom_table(self.create_table_window_ui.name_table.text(), self.pols)
            self.create_table_window.close()
            self.open_page_main()
        else:
            print('kkskx')


    def log_in(self):
        if self.users.find_user(self.login.text(), self.password.text()) and self.login.text() != '' and self.password.text() != '':
            self.user = self.users.find_user(self.login.text(), self.password.text())
            self.open_page_main()
        else:
            self.error_Log_in_text.setVisible(True)

    def log_in_new_user(self):
        if self.newuser_name.text() and self.newuser_login.text() and self.newuser_password_2.text():
            if self.CHECK.isChecked():
                if self.users.add_user(self.newuser_name.text(), self.newuser_login.text(), self.newuser_password_2.text()):
                    self.user = self.users.find_user(self.newuser_login.text(), self.newuser_password_2.text())
                    self.create_users_directory()
                    self.open_page_main()
                else:
                    self.newuser_error_text.setText('Пользователь с таким логином уже существует')
                    self.newuser_error_text.setVisible(True)
            else:
                self.newuser_error_text.setText('Нажатие на квадратик обязательное условие')
                self.newuser_error_text.setVisible(True)
        else:
            self.newuser_error_text.setText('Вы заполнили не все поля')
            self.newuser_error_text.setVisible(True)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Visual_PO_for_DB()
    ex.show()
    sys.exit(app.exec())