"""
Buttons located on the bottom of the app
"""
from PyQt5.QtWidgets import QFrame, QPushButton, QHBoxLayout, QSizePolicy
from PyQt5.QtCore import QRect


class SettingsButtonsFrame(QFrame):
    def __init__(self, top):
        super().__init__()
        self.top = top
        # self.setGeometry(QRect(10, 590, 780, 80))
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.layout = QHBoxLayout(self)
        # self.setMinimumSize(800,40)
        self.setFixedSize(800,40)
        self.setFrameShape(QFrame.StyledPanel)
        self.setFrameShadow(QFrame.Raised)

        self.photoButton = QPushButton(text="Photo")
        self.photoButton.setFixedHeight(40)
        self.photoButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self.showProductsButton = QPushButton(text="Search Products")
        self.showProductsButton.setFixedHeight(40)
        self.showProductsButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self.changeUserButton = QPushButton(text="Switch User")
        self.changeUserButton.setFixedHeight(40)
        self.changeUserButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self.prevProductButton = QPushButton(text="Previous")
        self.prevProductButton.setFixedHeight(40)
        self.prevProductButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self.nextProductButton = QPushButton(text="Next")
        self.nextProductButton.setFixedHeight(40)
        self.nextProductButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self.layout.addWidget(self.photoButton)
        self.layout.addWidget(self.showProductsButton)
        self.layout.addWidget(self.changeUserButton)
        self.layout.addWidget(self.prevProductButton)
        self.layout.addWidget(self.nextProductButton)

    def setup(self):
        pass
