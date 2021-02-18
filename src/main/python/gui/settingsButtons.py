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

        self.showProductsButton = QPushButton(self, text="Search Products")
        self.showProductsButton.setGeometry(QRect(155, 10, 140, 40))

        self.changeUserButton = QPushButton(self, text="Switch User")
        self.changeUserButton.setGeometry(QRect(300, 10, 140, 40))

        self.prevProductButton = QPushButton(self, text="Previous")
        self.prevProductButton.setGeometry(QRect(445, 10, 140, 40))

        self.nextProductButton = QPushButton(self, text="Next")
        self.nextProductButton.setGeometry(QRect(590, 10, 140, 40))

    def setup(self):    
        pass