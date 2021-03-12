"""
All components to the right of the main
app view
"""
from __future__ import annotations
from PyQt5.QtWidgets import QFrame, QPushButton, QTextEdit, QLineEdit, QFormLayout, QSizePolicy
from PyQt5.QtCore import QRect
from gui.scrollableProductComponent import ScrollPreviewComponent


class ProductManagerFrame(QFrame):
    def __init__(self, top):
        super().__init__()
        self.top = top
        # self.setGeometry(QRect(760, 10, 330, 640))
        self.setFixedWidth(400)
        self.setMinimumHeight(700)
        self.setFrameShape(QFrame.StyledPanel)
        self.setFrameShadow(QFrame.Raised)
        self.layout = QFormLayout(self)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.scrollArea = ScrollPreviewComponent(self)

        self.productBarcode = QLineEdit()
        self.productBarcode.setMinimumWidth(310)
        # self.productBarcode.setGeometry(QRect(10, 340, 310, 30))

        self.productDescription = QTextEdit()
        self.productDescription.setMinimumHeight(270)
        self.productDescription.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Expanding
        )

        self.confirmButton = QPushButton(text="Save")
        self.confirmButton.setMinimumSize(160,40)
        # self.confirmButton.setGeometry(QRect(160, 580, 160, 50))

        self.cancelButton = QPushButton(text="Delete")
        self.cancelButton.setMinimumSize(140,40)
        # self.cancelButton.setGeometry(QRect(10, 580, 140, 50))

        self.layout.addRow(self.scrollArea)
        self.layout.addRow(self.productBarcode)
        self.layout.addRow(self.productDescription)
        self.layout.addRow(self.cancelButton, self.confirmButton)

    def getScrollArea(self) -> ScrollPreviewComponent:
        return self.scrollArea

    def setup(self):
        pass

    def setBarcode(self, text: str):
        self.productBarcode.setText(text)

    def setDescription(self, desc: str):
        self.productDescription.setText(desc)

    def getBarcode(self) -> str:
        return self.productBarcode.text()

    def anyProduct(self):
        if self.getBarcode():
            return True

        if self.productDescription.toPlainText():
            return True

        if self.scrollArea.getPreviewList():
            return True

        return False
