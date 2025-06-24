from PySide6 import *
from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from util.SecurityManager import generateKey
import sys, json

def RunScreen(installFile,installFolder):
    #   Create Main App
    app = QApplication()
    #   Initialize all widget items
    parent = QWidget()
    userfield = UsernameField(parent)
    userlabel = UsernameLabel(parent,userfield)
    voteprefixfield = VotePrefixField(parent)
    voteprefixlabel = VotePrefixLabel(parent,voteprefixfield)
    pollprefixfield = PollPrefixField(parent)
    pollprefixlabel = PollPrefixLabel(parent,pollprefixfield)
    savebutton = SaveConfigButton(parent,installFolder)
    #   Set Properties
    parent.setWindowTitle("JTPoll V5.0.0 Installer")
    parent.setFixedSize(QSize(640, 480))
    parent.setFont(QFont("Calibri", 16))
    #   Show UI
    parent.show()
    #   Fetch Password
    password, ok = QInputDialog.getText(parent, "Choose New Password", "Choose Password", QLineEdit.EchoMode.Password)
    #   Check for ok signal and password is not empty
    if(not ok or password == ""):
        app.shutdown()
        sys.exit(0)
    #   Create The Secure Key for token storage
    generateKey(password,installFile)
    #   Send A Successful Notification Popup
    QMessageBox.information(parent,"Installer","Password setup has completed")
    #   Run main loop
    app.exec()


#   Username Label with properties set
class UsernameLabel(QLabel):
    def __init__(self, parent,buddy):
        super().__init__()
        self.setParent(parent)
        self.setText("Username")
        self.setGeometry(QRect(20,20,100,30))
        self.setBuddy(buddy)

#   Username Input with properties set
class UsernameField(QLineEdit):
    def __init__(self, parent):
        super().__init__()
        self.setParent(parent)
        self.setGeometry(QRect(120,20,200,30))
        self.setPlaceholderText("username")

#   Vote Prefix Label with properties set
class VotePrefixLabel(QLabel):
    def __init__(self, parent,buddy):
        super().__init__()
        self.setParent(parent)
        self.setText("Vote Prefix")
        self.setGeometry(QRect(20,80,100,30))
        self.setBuddy(buddy)

#   Vote Prefix Input with properties set
class VotePrefixField(QLineEdit):
    def __init__(self, parent):
        super().__init__()
        self.setParent(parent)
        self.setGeometry(QRect(120,80,100,30))
        self.setPlaceholderText("vote")

#   Poll Prefix Label with properties set
class PollPrefixLabel(QLabel):
    def __init__(self, parent,buddy):
        super().__init__()
        self.setParent(parent)
        self.setText("Poll Prefix")
        self.setGeometry(QRect(20,140,100,30))
        self.setBuddy(buddy)

#   Poll Prefix Input with properties set
class PollPrefixField(QLineEdit):
    def __init__(self, parent):
        super().__init__()
        self.setParent(parent)
        self.setGeometry(QRect(120,140,100,30))
        self.setPlaceholderText("poll")

#   Save Button with properties set
class SaveConfigButton(QPushButton):
    installfolder = ""
    def __init__(self, parent,installFolder):
        super().__init__()
        self.setProperty("installfolder",installFolder)
        installfolder = installFolder
        self.setParent(parent)
        self.setText("Save")
        self.connect(self, SIGNAL("clicked()"), self.save)
        self.setGeometry(QRect(120,250,100,30))

    # Button Pressed, save json
    def save(self):
        print(self.parent().children())
        username = self.parent().children()[0].text()
        voteprefix = self.parent().children()[2].text()
        pollprefix = self.parent().children()[4].text()
        encoder = json.JSONEncoder(indent=4)
        savdat = encoder.encode({"username":username,"voteprefix":voteprefix,"pollprefix":pollprefix})
        file = self.property("installfolder").joinpath("JTPollConfig.json").open("w+")
        file.write(savdat)
        file.flush()
        file.close()