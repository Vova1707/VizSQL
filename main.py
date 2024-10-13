import sys
import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QDialog, QFileDialog, QMessageBox
from PyQt6.QtGui import QPixmap
from Main_Window import Ui_Main
from DataBases import Database_With_Users
from Profile import Ui_Profile
from PIL import Image

class Visual_PO_for_DB(QMainWindow, Ui_Main):
    def __init__(self):
        super().__init__()
        super().setupUi(self)
        self.open_page_login()
        self.initUI()
        self.users = Database_With_Users()

    def initUI(self):
        self.newuser_button_2.clicked.connect(self.open_page_registration)
        self.newuser_button.clicked.connect(self.log_in_new_user)
        self.log_in_button.clicked.connect(self.log_in)
        self.Log_out_button.clicked.connect(self.open_page_login)
        self.profile_button.clicked.connect(self.open_profile_dialog_window)

    def open_profile_dialog_window(self):
        self.profile_window = QDialog()
        self.profile_window_ui = Ui_Profile()
        self.profile_window_ui.setupUi(self.profile_window)
        try:
            self.profile_window_ui.user_name_profile.setText(f'{self.user[1]}')
        except Exception as s:
            print(s.__class__.__name__)

        self.profile_window_ui.profile_image.clear()
        try:
            if not os.listdir(f'{self.directory}/image_profile/'):
                self.profile_window_ui.profile_image.setText('Нет изображения')
            else:
                image = QPixmap(f'{self.directory}/image_profile/image_profile.png')
                self.profile_window_ui.profile_image.setPixmap(image)
        except Exception as s:
            print(s.__class__.__name__)
        self.profile_window_ui.name_profile_text.setText(f'{self.user[1]}!')
        self.profile_window_ui.name_login_text.setText(f'{self.user[2]}')
        self.profile_window_ui.change_image_button.clicked.connect(self.change_and_save_image_profile)
        self.profile_window_ui.save_create_pole.clicked.connect(self.save_and_close_profile_windows)
        self.profile_window.exec()


    def save_and_close_profile_windows(self):
        self.users.update_name_users(self.profile_window_ui.user_name_profile.text(), self.user[0])
        self.user = self.users.find_user(self.user[2], self.user[3])
        self.profile_window.close()


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

    def open_page_registration(self):
        self.newuser_name.setText('')
        self.newuser_login.setText('')
        self.newuser_password_2.setText('')
        self.VizSQL.setCurrentIndex(1)
        self.newuser_error_text.setVisible(False)

    def open_page_login(self):
        self.VizSQL.setCurrentIndex(0)
        self.login.setText('')
        self.password.setText('')
        self.error_Log_in_text.setVisible(False)
        self.user = None

    def open_page_main(self):
        self.VizSQL.setCurrentIndex(2)
        self.directory = f'users/{self.user[2]}'
        print(self.user)

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


    def create_users_directory(self):
        os.makedirs(f'{os.getcwd()}/users/{self.user[1]}')
        os.makedirs(f'{os.getcwd()}/users/{self.user[1]}/databases')
        os.makedirs(f'{os.getcwd()}/users/{self.user[1]}/image_profile')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Visual_PO_for_DB()
    ex.show()
    sys.exit(app.exec())