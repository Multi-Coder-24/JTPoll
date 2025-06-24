from PySide6.QtWidgets import *
from PySide6.QtCore import *

# Main Window Class
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(QSize(800, 600))
        self.setWindowTitle("JTPoll")
        self.show()

class PasswordBox(QLineEdit):
    def __init__(self,parent):
        super().__init__()
        self.setGeometry(QRect(57,1,150,20))
        self.setPlaceholderText("Password")
        self.setEchoMode(QLineEdit.EchoMode.Password)
        self.setParent(parent)


class PasswordLabel(QLabel):
    def __init__(self,buddy,parent):
        super().__init__("Password")
        self.setGeometry(QRect(1, 1, 50, 20))
        self.setBuddy(buddy)
        self.setParent(parent)