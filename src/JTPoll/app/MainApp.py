import sys
from PySide6.QtWidgets import *
from PySide6.QtCore import *

def RunApp():
    app = QApplication(sys.argv)
    parent = MainWindow()
    parent.show()
    app.exec()

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(QSize(800, 600))
        self.setWindowTitle("JTPoll V5.0.0")
        passwordBox = PasswordBox(self)
        passwordLabel = PasswordLabel(passwordBox,self)

class PasswordBox(QLineEdit):
    def __init__(self,parent):
        super().__init__()
        self.setGeometry(QRect(120,10,150,20))
        self.setPlaceholderText("Password")
        self.setEchoMode(QLineEdit.EchoMode.Password)
        self.setParent(parent)

class PasswordLabel(QLabel):
    def __init__(self,buddy,parent):
        super().__init__("Password")
        self.setGeometry(QRect(10, 10, 100, 20))
        self.setBuddy(buddy)
        self.setParent(parent)