"""
All components to the right of the main
app view
"""
from __future__ import annotations
from PyQt5.QtWidgets import QFrame, QPushButton, QTextEdit, QLineEdit
from PyQt5.QtCore import QRect
from gui.scrollableProductComponent import ScrollPreviewComponent


class ProductManagerFrame(QFrame):
    def __init__(self, top):
        super().__init__(top.centralwidget)
        self.top = top
        self.setGeometry(QRect(760, 10, 330, 640))
        self.setFrameShape(QFrame.StyledPanel)
        self.setFrameShadow(QFrame.Raised)

        self.scrollArea = ScrollPreviewComponent(self)

        self.productBarcode = QLineEdit(self)
        self.productBarcode.setFixedWidth(310)
        self.productBarcode.move(10,340)
        # self.productBarcode.setGeometry(QRect(10, 340, 310, 30))

        self.productDescription = QTextEdit(self)
        s = self.productBarcode.size()
        p = self.productBarcode.pos()
        x0, y0, = 320, 570 # coords of the SE point of the Rect
        self.productDescription.setGeometry(
            QRect(
                10, p.y() + s.height(), 
                x0 - 10, y0 - p.y() - s.height()))

        self.confirmButton = QPushButton(parent=self, text="Save")
        self.confirmButton.setGeometry(QRect(160, 580, 160, 50))

        self.cancelButton = QPushButton(parent=self, text="Delete")
        self.cancelButton.setGeometry(QRect(10, 580, 140, 50))

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
        elif self.productDescription.toPlainText():
            return True
        elif self.scrollArea.getPreviewList():
            return True
        else:
            return False
