"""
Display useful dialogs for the application
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
    QFormLayout,
    QVBoxLayout,
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont


def logUserIn():
    lDialog = LoginDialog()
    lDialog.exec()
    login = lDialog.loginText.text()
    password = lDialog.passText.text()
    if lDialog.result() == 0:
        return None, None
    if login or password:
        errorOccured("Fill all fields!!")
        return None, None

    from utils.AppDataController import checkForCredentials

    if checkForCredentials(login, password):
        return login, password

    errorOccured("This user does not exits")
    return None, None


def createAccout():
    cDialog = CreateAccountDialog()
    cDialog.exec()
    login = cDialog.loginText.text()
    password = cDialog.passText.text()
    pass2 = cDialog.passRepText.text()
    if cDialog.result() == 0:
        return None, None
    del cDialog

    if password or login:
        errorOccured("Fill all fields!!")
        return

    if password != pass2:
        errorOccured("Passwords do not match!! Try again")
        return

    from utils.AppDataController import checkForCredentials

    if checkForCredentials(login, password, onlyCheckLogin=True):
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
    return camDialog.deviceComboBox.currentIndex()


def getFolderPath(parent) -> str:
    # note: in windows 10, we need to pass parent reference to
    # the function. Otherwise QFileDialog will emit a silent crash
    return QFileDialog.getExistingDirectory(
        parent, options=QFileDialog.DontUseNativeDialog
    )


class InfoDialog(QDialog):
    def __init__(self):
        super().__init__(None, Qt.WindowSystemMenuHint | Qt.WindowTitleHint)

        self.lo = QVBoxLayout(self)
        font = QFont()
        font.setFamily("Noto Sans")
        font.setPointSize(12)
        font.setBold(True)

        self.titleLabel = QLabel("About")
        self.titleLabel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.titleLabel.setFont(font)

        self.titleLabel_2 = QLabel("Author")
        self.titleLabel_2.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Fixed
        )
        self.titleLabel_2.setFont(font)

        self.authorLabel = QLabel("Michał Wilk - 02.2021")
        self.authorLabel.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        self.authorLabel.setWordWrap(True)

        self.descLabel = QLabel(
            "App for managing products and their photos. License is GPL v3. "
            "Code and useful informations available "
            "on github:\nhttps://github.com/michalwilk123/STManager",
            self,
        )
        self.descLabel.setTextInteractionFlags(Qt.TextSelectableByMouse)

        self.descLabel.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        self.descLabel.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        self.descLabel.setWordWrap(True)
        self.lo.addWidget(self.titleLabel, alignment=Qt.AlignCenter)
        self.lo.addWidget(self.descLabel)
        self.lo.addWidget(self.titleLabel_2, alignment=Qt.AlignCenter)
        self.lo.addWidget(self.authorLabel)
        self.lo.setSpacing(10)

        self.setWindowTitle("About")


class LoginDialog(QDialog):
    def __init__(self):
        super().__init__(None, Qt.WindowSystemMenuHint | Qt.WindowTitleHint)
        self.lo = QFormLayout(self)
        self.loginText = QLineEdit()
        self.loginText.setFixedWidth(170)

        self.passText = QLineEdit()
        self.passText.setEchoMode(QLineEdit.Password)
        self.passText.setFixedWidth(170)
        self.passText.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self.dialogButtons = QDialogButtonBox()
        self.loginText.setFixedSize(170, 30)
        self.dialogButtons.setStandardButtons(
            QDialogButtonBox.Cancel | QDialogButtonBox.Ok
        )

        font = QFont()
        font.setFamily("Noto Sans")
        font.setPointSize(12)
        font.setBold(True)
        self.titleLabel = QLabel("Log in")
        self.titleLabel.setFont(font)

        self.loginLabel = QLabel("Login:")

        self.passLabel = QLabel("Password:")

        self.lo.addRow(self.titleLabel)
        self.lo.addRow(self.loginLabel, self.loginText)
        self.lo.addRow(self.passLabel, self.passText)
        self.lo.addRow(self.dialogButtons)
        self.lo.setVerticalSpacing(10)

        self.setWindowTitle("Log in")
        self.dialogButtons.accepted.connect(lambda: self.done(1))
        self.dialogButtons.rejected.connect(lambda: self.done(0))


class CreateAccountDialog(QDialog):
    def __init__(self):
        super().__init__(None, Qt.WindowSystemMenuHint | Qt.WindowTitleHint)

        self.lo = QFormLayout(self)
        self.loginText = QLineEdit()
        self.loginText.setFixedWidth(170)
        self.loginText.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self.passText = QLineEdit()
        self.passText.setEchoMode(QLineEdit.Password)
        self.passText.setFixedWidth(170)
        self.passText.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self.passRepText = QLineEdit()
        self.passRepText.setEchoMode(QLineEdit.Password)
        self.passRepText.setFixedWidth(170)
        self.passRepText.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self.dialogButtons = QDialogButtonBox()
        self.dialogButtons.setFixedWidth(170)
        self.dialogButtons.setStandardButtons(
            QDialogButtonBox.Cancel | QDialogButtonBox.Ok
        )

        font = QFont()
        font.setFamily("Noto Sans")
        font.setPointSize(12)
        font.setBold(True)
        self.titleLabel = QLabel("Create Account")
        self.titleLabel.setFont(font)

        self.loginLabel = QLabel("Login:")

        self.passLabel = QLabel("Password:")

        self.passRepLabel = QLabel("Repeat password:")
        self.passRepLabel.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.passRepLabel.setAlignment(
            Qt.AlignLeading | Qt.AlignLeft | Qt.AlignTop
        )
        self.passRepLabel.setWordWrap(True)

        self.lo.addRow(self.titleLabel)
        self.lo.addRow(self.loginLabel, self.loginText)
        self.lo.addRow(self.passLabel, self.passText)
        self.lo.addRow(self.passRepLabel, self.passRepText)
        self.lo.addRow(None, self.dialogButtons)
        self.lo.setVerticalSpacing(10)

        self.setWindowTitle("Create Account")
        self.dialogButtons.accepted.connect(lambda: self.done(1))
        self.dialogButtons.rejected.connect(lambda: self.done(0))


class CameraChooserDialog(QDialog):
    def __init__(self, deviceList):
        super().__init__(None, Qt.WindowSystemMenuHint | Qt.WindowTitleHint)
        self.lo = QFormLayout(self)
        self.deviceComboBox = QComboBox(self)
        self.deviceComboBox.addItems(deviceList)

        self.dialogButtons = QDialogButtonBox(self)
        self.dialogButtons.setStandardButtons(
            QDialogButtonBox.Cancel | QDialogButtonBox.Ok
        )

        self.label = QLabel("Choose a device", self)
        self.label.setWordWrap(True)
        self.lo.addRow(self.label, self.deviceComboBox)
        self.lo.addRow(self.dialogButtons)
        self.lo.setVerticalSpacing(10)

        self.setWindowTitle("Choose a device")
        self.dialogButtons.accepted.connect(lambda: self.done(1))
        self.dialogButtons.rejected.connect(lambda: self.done(0))
