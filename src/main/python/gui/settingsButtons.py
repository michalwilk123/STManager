from PyQt5.QtWidgets import QFrame, QPushButton
from PyQt5.QtCore import QCoreApplication, QRect

class SettingsButtonsFrame(QFrame):
    def __init__(self, top):
        super().__init__(top.centralwidget)

        self.top = top
        self.setGeometry(QRect(0, 579, 751, 61))
        self.setFrameShape(QFrame.StyledPanel)
        self.setFrameShadow(QFrame.Raised)
        self.setObjectName("settingButtonsFrame")

        self.photoButton = QPushButton(self)
        self.photoButton.setGeometry(QRect(10, 10, 141, 41))
        self.photoButton.setObjectName("photoButton")

        self.showProductsButton = QPushButton(self)
        self.showProductsButton.setGeometry(QRect(160, 10, 141, 41))
        self.showProductsButton.setObjectName("showProductsButton")

        self.changeUserButton = QPushButton(self)
        self.changeUserButton.setGeometry(QRect(310, 10, 131, 41))
        self.changeUserButton.setObjectName("changeUserButton")

        self.switchDeviceButton = QPushButton(self)
        self.switchDeviceButton.setGeometry(QRect(450, 10, 131, 41))
        self.switchDeviceButton.setObjectName("switchDeviceButton")

        # setting up text for buttons
        _translate = QCoreApplication.translate
        self.photoButton.setText(_translate("MainWindow", "Photo"))
        self.showProductsButton.setText(_translate("MainWindow", "Products"))
        self.changeUserButton.setText(_translate("MainWindow", "Switch User"))
        self.switchDeviceButton.setText(_translate("MainWindow", "Scan With Scanner"))


    def setup(self):
        self.photoButton.clicked.connect(
            self.top.cameraDisplayFrame.takePicture
        )