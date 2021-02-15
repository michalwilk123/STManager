from PyQt5.QtWidgets import QFrame, QPushButton
from PyQt5.QtCore import QCoreApplication, QRect

class SettingsButtonsFrame(QFrame):
    def __init__(self, top):
        super().__init__(top.centralwidget)

        self.top = top
        self.setGeometry(QRect(10, 590, 740, 60))
        self.setFrameShape(QFrame.StyledPanel)
        self.setFrameShadow(QFrame.Raised)

        self.photoButton = QPushButton(self, text="Photo")
        self.photoButton.setGeometry(QRect(10, 10, 140, 40))

        self.showProductsButton = QPushButton(self, text="Products")
        self.showProductsButton.setGeometry(QRect(160, 10, 140, 40))

        self.changeUserButton = QPushButton(self, text="Switch User")
        self.changeUserButton.setGeometry(QRect(310, 10, 140, 40))

        self.switchDeviceButton = QPushButton(self, text="Scanner Mode")
        self.switchDeviceButton.setGeometry(QRect(460, 10, 140, 40))


    def setup(self):
        self.photoButton.clicked.connect(
            self.top.cameraDisplayFrame.takePicture
        )