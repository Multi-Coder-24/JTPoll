import sys, os, io
from PySide6.QtWidgets import *
from pathlib import Path
from util import SecurityManager
from installer.ui import InstallScreen

homeFolder = Path.home()
installFolder = homeFolder.joinpath("JTPoll")
installFile = installFolder.joinpath("JTPoll.dat")

def isInstalled():
    return False

def prepInstall():
    installFolder.mkdir(parents=True, exist_ok=True)
    InstallScreen.RunScreen(installFile,installFolder)
    sys.exit(0)
    pass