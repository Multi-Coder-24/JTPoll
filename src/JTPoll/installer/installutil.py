from pathlib import Path
from util import SecurityManager
from PySide6 import *
from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from util.SecurityManager import generateKey
import sys, json, uuid, webbrowser, urllib.parse
import util.secure.Variables as Variables

homeFolder = Path.home()
installFolder = homeFolder.joinpath("JTPoll")
installFile = installFolder.joinpath("JTPoll.dat")
def Install():
    installFolder.mkdir(parents=True, exist_ok=True)
    #   Create Main App
    app = QApplication()
    #   Initialize all widget items
    parent = InstallerUI()
    #   Show UI
    parent.show()
    #   Fetch Password
    password, ok = QInputDialog.getText(parent, "Choose New Password", "Choose Password", QLineEdit.EchoMode.Password)
    #   Check for ok signal and password is not empty
    if (not ok or password == ""):
        app.shutdown()
        sys.exit(0)
    #   Create The Secure Key for token storage
    generateKey(password, installFile)
    #   Send A Successful Notification Popup
    QMessageBox.information(parent, "Installer", "Password setup has completed")
    #   Run main loop
    app.exec()

def isInstalled():
    return installFolder.exists()

class InstallerUI(QWidget):
    userField = None
    votePrefixField = None
    pollPrefixField = None
    def __init__(self):
        QWidget.__init__(self)
        self.setWindowTitle("JTPoll V5.0.0 Installer")
        self.setFixedSize(QSize(544, 306))
        self.setFont(QFont("Calibri", 16))
        self.userField = UsernameField(self)
        userLabel = UsernameLabel(self,self.userField)
        self.votePrefixField = VotePrefixField(self)
        votePrefixLabel = VotePrefixLabel(self, self.votePrefixField)
        self.pollPrefixField = PollPrefixField(self)
        pollPrefixLabel = PollPrefixLabel(self, self.pollPrefixField)
        saveButton = SaveConfigButton(self)
        authorizeButton = AuthorizeButton(self)
        newPollButton = QPushButton("New Poll")
        runApp = QPushButton("Close Application")
        runApp.setParent(self)
        newPollButton.setParent(self)
        newPollButton.connect(SIGNAL("clicked()"), self.startNewPoll)
        newPollButton.setGeometry(QRect(20,240,100,30))
        runApp.setGeometry(QRect(120,240,175,30))
        saveButton.connect(SIGNAL("clicked()"), self.saveConfig)
        runApp.connect(SIGNAL("clicked()"), self.runApp)

    def startNewPoll(self):
        poll = NewPoll()
        poll.show()
        poll.exec()
    def runApp(self):
        sys.exit(0);

    def saveConfig(self):
        username = self.userField.text()
        voteprefix = self.votePrefixField.text()
        pollprefix = self.pollPrefixField.text()
        encoder = json.JSONEncoder(indent=4)
        savdat = encoder.encode({"username": username, "voteprefix": voteprefix, "pollprefix": pollprefix})
        file = installFolder.joinpath("JTPollConfig.json").open("w+")
        file.write(savdat)
        file.flush()
        file.close()


class UsernameField(QLineEdit):
    def __init__(self, parent):
        super().__init__()
        self.setParent(parent)
        self.setGeometry(QRect(120, 20, 200, 30))
        self.setPlaceholderText("username")

class VotePrefixLabel(QLabel):
    def __init__(self, parent, buddy):
        super().__init__()
        self.setParent(parent)
        self.setText("Vote Prefix")
        self.setGeometry(QRect(20, 80, 100, 30))
        self.setBuddy(buddy)

class VotePrefixField(QLineEdit):
    def __init__(self, parent):
        super().__init__()
        self.setParent(parent)
        self.setGeometry(QRect(120, 80, 100, 30))
        self.setPlaceholderText("vote")

class UsernameLabel(QLabel):
    def __init__(self, parent, buddy):
        super().__init__()
        self.setParent(parent)
        self.setText("Username")
        self.setGeometry(QRect(20, 20, 100, 30))
        self.setBuddy(buddy)

class AuthorizeButton(QPushButton):
    def __init__(self, parent):
        super().__init__()
        self.setText("Authorize Application")
        self.setParent(parent)
        self.connect(self, SIGNAL("clicked()"), self.authorize)
        self.setGeometry(QRect(120, 200, 200, 30))

    def authorize(self):
        state = str(uuid.uuid4().hex)
        url = Variables.AUTHURL + state
        webbrowser.open_new(url)
        resp, ok = QInputDialog.getText(self.parent(), "Enter URL", "Paste The Response From Twitch")
        if(not ok or resp == ""):
            QMessageBox.information(self.parent(), "Authorization Error", "No Response Detected\nApplication Closing")
            sys.exit(1)
        if(str(urllib.parse.urlparse(resp).query).startswith("?error")):
            QMessageBox.information(self.parent, "Authorization Error", "Authorization Error\nApplication Closing")
            sys.exit(2)
        else:
            frag = urllib.parse.urldefrag(resp).fragment
            frag = frag.split("&")
            token = frag[0].split("=")[1]
            retstate = frag[2].split("=")[1]
            if(state != retstate):
                QMessageBox.information(self.parent(), "Authorization Error", "State mismatch error\nApplication Closing")
                sys.exit(3)
            else:
                password, ok = QInputDialog.getText(self.parent(), "Enter Security Password", "Please Enter Your Password", QLineEdit.EchoMode.Password)
                if (not ok or password == ""):
                    QMessageBox.information(self.parent(), "Authorization Error", "No Password Entered\nApplication Closing")
                    sys.exit(4)
                retstate = None
                SecurityManager.SaveToken(self.parent(), password, installFile, token, installFolder)
                password = None
                token = None
                resp = None
            QMessageBox.information(self.parent(), "Authorization Success", "Authorization Successful")

class SaveConfigButton(QPushButton):
    def __init__(self, parent):
        super().__init__()
        self.setParent(parent)
        self.setText("Save")
        self.setGeometry(QRect(20, 200, 100, 30))

class PollPrefixField(QLineEdit):
    def __init__(self, parent):
        super().__init__()
        self.setParent(parent)
        self.setGeometry(QRect(120, 140, 100, 30))
        self.setPlaceholderText("poll")

class PollPrefixLabel(QLabel):
    def __init__(self, parent, buddy):
        super().__init__()
        self.setParent(parent)
        self.setText("Poll Prefix")
        self.setGeometry(QRect(20, 140, 100, 30))
        self.setBuddy(buddy)

class NewPoll(QDialog):
    nameField = None
    options = None
    alphabeticalSort = None
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Create New Poll")
        self.setFixedSize(QSize(352,198))
        self.nameField = QLineEdit()
        nameLabel = QLabel("Name")
        optionsLabel = QLabel("Options")
        self.options = QPlainTextEdit()
        savebutton = QPushButton("Save")
        self.alphabeticalSort = QCheckBox("Alphabetical Sorting")
        nameLabel.setBuddy(self.nameField)
        nameLabel.setParent(self)
        optionsLabel.setParent(self)
        self.nameField.setParent(self)
        self.options.setParent(self)
        self.alphabeticalSort.setParent(self)
        savebutton.setParent(self)
        savebutton.connect(SIGNAL("clicked()"), self.save)
        nameLabel.setGeometry(QRect(10, 10, 50, 30))
        self.nameField.setGeometry(QRect(70, 10, 100, 30))
        self.alphabeticalSort.setGeometry(QRect(10, 40, 150, 30))
        self.options.setGeometry(QRect(175, 30, 160, 155))
        optionsLabel.setGeometry(QRect(235, 5, 100, 30))
        savebutton.setGeometry(QRect(10, 70, 100, 30))

    def save(self):
        installFolder.joinpath("Polls").mkdir(parents=True, exist_ok=True)
        name = self.nameField.text()
        options = self.options.toPlainText().split("\n")
        alphabetic = self.alphabeticalSort.isChecked()
        encoder = json.JSONEncoder(indent=4)
        savedat = encoder.encode({"name": name, "alphabetic": alphabetic, "options": options})
        savefile = installFolder.joinpath("Polls\\" + name + ".json").open("w+")
        savefile.write(savedat)
        savefile.flush()
        savefile.close()
        QMessageBox.information(self, "Save Complete", "Poll " + name + " Saved")