import datetime
from PySide6.QtWidgets import QApplication
import sys
from installer.installutil import *
from installer.installutil import Install
from app.MainApp import RunApp

if(not isInstalled()):
    Install()
else:
    RunApp()

sys.exit(0)
