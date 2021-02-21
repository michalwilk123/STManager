"""
Display useful dialog widgets for the application
"""
from PyQt5.QtWidgets import (
    QDialog,
    QLabel,
    QSizePolicy,
    QLineEdit,
    QDialogButtonBox,
    QComboBox,
    QMessageBox,
    QFileDialog,
)
from PyQt5.QtCore import QRect, Qt
from PyQt5.QtGui import QFont


def logUserIn():
    lDialog = LoginDialog()
    lDialog.exec()
    login = lDialog.loginText.text()
    password = lDialog.passText.text()
    if lDialog.result() == 0:
        return None, None

    from utils.AppDataController import checkForCredentials

    if checkForCredentials(login, password):
        return login, password
    else:
        errorOccured("This user does not exits")
        return None, None


def createAccout():
    cDialog = CreateAccountDialog()
    cDialog.exec()
    login = cDialog.loginText.text()
    password = cDialog.passText.text()
    pass2 = cDialog.passRepText.text()
    del cDialog

    if password == "" or login == "":
        return

    if password != pass2:
        errorOccured("Passwords do not match!! Try again")
        return

    from utils.AppDataController import checkForCredentials

    if checkForCredentials(login, password):
        errorOccured("This user already exists!")
        return

    # everything is alright. Now we create new user
    from utils.AppDataController import createNewUser

    createNewUser(login, password)


def errorOccured(message):
    msg = QMessageBox()
    msg.setText(message)
    msg.setWindowTitle("Error")
    msg.exec()


def showInfo():
    InfoDialog().exec()


def cameraChoice() -> int:
    from utils.AppController import AppController

    camList = AppController.getCameraList()
    camDialog = CameraChooserDialog(camList)
    camDialog.exec()
    if camDialog.result() == 0:
        return -1
    else:
        return camDialog.deviceComboBox.currentIndex()


def getFolderPath() -> str:
    return QFileDialog.getExistingDirectoryUrl().path()


class InfoDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setFixedSize(260, 260)

        font = QFont()
        font.setFamily("Noto Sans")
        font.setPointSize(12)
        font.setBold(True)

        self.titleLabel = QLabel("About", self)
        self.titleLabel.setGeometry(QRect(100, 20, 51, 31))
        self.titleLabel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.titleLabel.setFont(font)

        self.titleLabel_2 = QLabel("Author", self)
        self.titleLabel_2.setGeometry(QRect(100, 160, 61, 31))
        self.titleLabel_2.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Fixed
        )
        self.titleLabel_2.setFont(font)

        self.authorLabel = QLabel("Michał Wilk - 02.2021", self)
        self.authorLabel.setGeometry(QRect(10, 190, 241, 51))
        self.authorLabel.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        self.authorLabel.setWordWrap(True)

        self.descLabel = QLabel(
            """
App for managing chaos in post packages.
License is GPL v3. Code is available on github: http://github.com
""",
            self,
        )
        self.descLabel.setGeometry(QRect(10, 40, 241, 100))
        self.descLabel.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        self.descLabel.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        self.descLabel.setWordWrap(True)

        self.setWindowTitle("About")


class LoginDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setFixedSize(260, 170)
        self.loginText = QLineEdit(self)
        self.loginText.setGeometry(QRect(80, 50, 170, 30))
        self.loginText.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self.passText = QLineEdit(self)
        self.passText.setEchoMode(QLineEdit.Password)
        self.passText.setGeometry(QRect(80, 90, 170, 30))
        self.passText.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self.dialogButtons = QDialogButtonBox(self)
        self.dialogButtons.setGeometry(QRect(80, 130, 171, 35))
        self.dialogButtons.setStandardButtons(
            QDialogButtonBox.Cancel | QDialogButtonBox.Ok
        )

        font = QFont()
        font.setFamily("Noto Sans")
        font.setPointSize(12)
        font.setBold(True)
        self.titleLabel = QLabel("Log in", self)
        self.titleLabel.setGeometry(QRect(95, 10, 61, 31))
        self.titleLabel.setFont(font)

        self.loginLabel = QLabel("Login:", self)
        self.loginLabel.setGeometry(QRect(5, 50, 58, 31))

        self.passLabel = QLabel("Password:", self)
        self.passLabel.setGeometry(QRect(5, 90, 71, 31))
        self.setWindowTitle("Log in")
        self.dialogButtons.accepted.connect(lambda: self.done(1))
        self.dialogButtons.rejected.connect(lambda: self.done(0))


class CreateAccountDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setFixedSize(260, 210)
        self.loginText = QLineEdit(self)
        self.loginText.setGeometry(QRect(80, 50, 170, 30))
        self.loginText.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self.passText = QLineEdit(self)
        self.passText.setEchoMode(QLineEdit.Password)
        self.passText.setGeometry(QRect(80, 90, 170, 30))
        self.passText.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self.passRepText = QLineEdit(self)
        self.passRepText.setEchoMode(QLineEdit.Password)
        self.passRepText.setGeometry(QRect(80, 130, 170, 30))
        self.passRepText.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self.dialogButtons = QDialogButtonBox(self)
        self.dialogButtons.setGeometry(QRect(80, 170, 171, 35))
        self.dialogButtons.setStandardButtons(
            QDialogButtonBox.Cancel | QDialogButtonBox.Ok
        )

        font = QFont()
        font.setFamily("Noto Sans")
        font.setPointSize(12)
        font.setBold(True)
        self.titleLabel = QLabel("Create Account", self)
        self.titleLabel.setGeometry(QRect(80, 10, 150, 30))
        self.titleLabel.setFont(font)

        self.loginLabel = QLabel("Login:", self)
        self.loginLabel.setGeometry(QRect(5, 50, 58, 31))

        self.passLabel = QLabel("Password:", self)
        self.passLabel.setGeometry(QRect(5, 90, 71, 31))

        self.passRepLabel = QLabel("Repeat password:", self)
        self.passRepLabel.setGeometry(QRect(5, 130, 71, 41))
        self.passRepLabel.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.passRepLabel.setAlignment(
            Qt.AlignLeading | Qt.AlignLeft | Qt.AlignTop
        )
        self.passRepLabel.setWordWrap(True)

        self.setWindowTitle("Create Account")
        self.dialogButtons.accepted.connect(lambda: self.done(1))
        self.dialogButtons.rejected.connect(lambda: self.done(0))


class CameraChooserDialog(QDialog):
    def __init__(self, deviceList):
        super().__init__()
        self.setFixedSize(260, 90)
        self.deviceComboBox = QComboBox(self)
        self.deviceComboBox.addItems(deviceList)
        self.deviceComboBox.setGeometry(QRect(80, 10, 170, 32))

        self.dialogButtons = QDialogButtonBox(self)
        self.dialogButtons.setGeometry(QRect(80, 50, 170, 34))
        self.dialogButtons.setStandardButtons(
            QDialogButtonBox.Cancel | QDialogButtonBox.Ok
        )

        self.label = QLabel("Choose a device", self)
        self.label.setGeometry(QRect(5, 10, 61, 31))
        self.label.setWordWrap(True)

        self.setWindowTitle("Choose a device")
        self.dialogButtons.accepted.connect(lambda: self.done(1))
        self.dialogButtons.rejected.connect(lambda: self.done(0))
