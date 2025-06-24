from PySide6.QtWidgets import QApplication
import sys
from installer.installutil import *
from ui.mainscreen import *



if(not isInstalled()):
    prepInstall()

app = QApplication(sys.argv)
window = MainWindow()
app.exec()
