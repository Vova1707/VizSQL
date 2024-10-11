import sys

from PyQt6.QtWidgets import QApplication, QMainWindow
from PO_for_DB import Ui_MainWindow
from Db import Users

class Visual_PO_for_DB(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        super().setupUi(self)
        self.initUI()
        self.users = Users()
        self.user = ''

    def initUI(self):
        self.newlog_in_button.clicked.connect(self.log_in_new_user_1)
        self.Newregistration_button.clicked.connect(self.log_in_new_user_2)
        self.log_in_button.clicked.connect(self.log_in_old_user)
    def log_in_old_user(self):
        if self.users.find_user(self.login.text(), self.password.text()):
            self.user = self.users.find_user(self.login.text(), self.password.text())
            self.VizSQL.setCurrentIndex(self.VizSQL.currentIndex() + 2)

    def log_in_new_user_1(self):
        self.VizSQL.setCurrentIndex(self.VizSQL.currentIndex() + 1)

    def log_in_new_user_2(self):
        if self.CHECK.isChecked():
            self.users.add_user(self.NEW_NAME.text(), self.NEW_LOGIN.text(), self.NEWPASSWORD.text())
            self.VizSQL.setCurrentIndex(self.VizSQL.currentIndex() + 1)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Visual_PO_for_DB()
    ex.show()
    sys.exit(app.exec())