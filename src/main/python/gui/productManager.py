from PyQt5.QtWidgets import QFrame, QPushButton, QWidget, \
    QTextEdit, QScrollArea, QLabel, QVBoxLayout, QSizePolicy
from PyQt5.QtCore import QCoreApplication, QRect, Qt
from gui.scrollableProductComponent import ScrollPreviewComponent


class ProductManagerFrame(QFrame):
    def __init__(self, top):
        super().__init__(top.centralwidget)
        self.top = top
        self.setGeometry(QRect(760, 10, 331, 631))
        self.setFrameShape(QFrame.StyledPanel)
        self.setFrameShadow(QFrame.Raised)
        self.setObjectName("productManagerFrame")

        self.scrollArea = ScrollPreviewComponent(self)


        self.productBarcode = QTextEdit(self)
        self.productBarcode.setGeometry(QRect(10, 310, 311, 41))
        self.productBarcode.setObjectName("productBarcode")

        self.productDescription = QTextEdit(self)
        self.productDescription.setGeometry(QRect(10, 360, 311, 191))
        self.productDescription.setObjectName("productDescription")

        self.confirmButton = QPushButton(self)
        self.confirmButton.setGeometry(QRect(160, 560, 161, 61))
        self.confirmButton.setObjectName("confirmButton")

        self.cancelButton = QPushButton(self)
        self.cancelButton.setGeometry(QRect(10, 560, 141, 61))
        self.cancelButton.setObjectName("cancelButton")

        _translate = QCoreApplication.translate
        self.confirmButton.setText(_translate("MainWindow", "Confirm"))
        self.cancelButton.setText(_translate("MainWindow", "Cancel"))


    def setBarcode(self, text):
        self.productBarcode.setText(
            text
        )



    def setup(self):
        pass