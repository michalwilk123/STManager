from __future__ import annotations
from PyQt5.QtWidgets import (QDialog, QTableWidget,
    QScrollArea, QWidget, QVBoxLayout, QLabel, QPushButton, QFrame,
    QDateEdit, QComboBox, QLineEdit, QCheckBox, QTableWidgetItem)
from PyQt5.QtCore import QRect, Qt
from PyQt5.QtGui import QFont
from utils.AppContoller import AppController

smallFont = QFont()
smallFont.setPointSize(9)
bigFont = QFont()
bigFont.setPointSize(14)

class ProductSearcher(QDialog):
    def __init__(self, controller:AppController):
        super().__init__()
        self.setFixedSize(880,560) 
        self.tableScrollArea = ProductTable(self)

        self.photoLabel = QLabel("NO PHOTO FOUND", self)
        self.photoLabel.setGeometry(QRect(10, 10, 450, 310))
        self.photoLabel.setStyleSheet(
"""
background-color: white;\n
color: red;\n
font-size: 40px;
"""
        )

        self.prevPhotoButton = QPushButton("Previous", self)
        self.prevPhotoButton.setGeometry(QRect(10, 330, 88, 21))
        self.prevPhotoButton.setFont(smallFont)
        self.nextPhotoButton = QPushButton("Next", self)
        self.nextPhotoButton.setGeometry(QRect(110, 330, 88, 21))
        self.nextPhotoButton.setFont(smallFont)
        self.idLabel = QLabel("Id: ", self)
        self.idLabel.setGeometry(QRect(220, 330, 241, 18))
        self.idLabel.setFont(smallFont)
        self.idLabel.setStyleSheet(
"""
border: 1px solid black;\n
background-color: white;\n
color: black;
"""
        )
        
        self.line = QFrame(self)
        self.line.setGeometry(QRect(10, 470, 861, 20))
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.titleLabel = QLabel("Results:    0", self)
        self.titleLabel.setGeometry(QRect(470, 10, 121, 20))
        self.titleLabel.setFont(bigFont)

        self.dateToDEdit = QDateEdit(self)
        self.dateToDEdit.setGeometry(QRect(690, 520, 100, 30))

        self.dateFromDEdit = QDateEdit(self)
        self.dateFromDEdit.setGeometry(QRect(580, 520, 100, 30))

        self.userComboBox = QComboBox(self)
        self.userComboBox.setGeometry(QRect(250, 520, 140, 30))

        self.phraseLEdit = QLineEdit(self)
        self.phraseLEdit.setGeometry(QRect(400, 520, 170, 30))

        self.findButton = QPushButton("Find", self)
        self.findButton.setGeometry(QRect(800, 490, 70, 61))

        self.idLEdit = QLineEdit(self)
        self.idLEdit.setGeometry(QRect(10, 520, 230, 30))

        self.dateFromCBox = QCheckBox("Date from", self)
        self.dateFromCBox.setGeometry(QRect(580, 490, 100, 20))
        self.dateFromCBox.setFont(smallFont)

        self.dateToCBox = QCheckBox("Date to", self)
        self.dateToCBox.setGeometry(QRect(690, 490, 100, 20))
        self.dateToCBox.setFont(smallFont)

        self.phraseCBox = QCheckBox("Phrase", self)
        self.phraseCBox.setGeometry(QRect(400, 490, 100, 20))
        self.phraseCBox.setFont(smallFont)

        self.userCBox = QCheckBox("User", self)
        self.userCBox.setGeometry(QRect(250, 490, 100, 20))
        self.userCBox.setFont(smallFont)

        self.idCBox = QCheckBox("Id", self)
        self.idCBox.setGeometry(QRect(10, 490, 100, 20))
        self.idCBox.setFont(smallFont)

        self.createdDate = QLabel("Created: ", self)
        self.createdDate.setGeometry(QRect(10, 460, 201, 16))
        self.createdDate.setFont(smallFont)

        self.lastModLabel = QLabel("Last modified:", self)
        self.lastModLabel.setGeometry(QRect(240, 460, 221, 16))
        self.lastModLabel.setFont(smallFont)

        self.descriptionLabel = QLabel(self)
        self.descriptionLabel.setGeometry(QRect(10, 360, 451, 91))
        self.descriptionLabel.setFont(smallFont)
        self.descriptionLabel.setStyleSheet(
"""
border: 1px solid black;\n
background-color: white;\n
color: black;
"""
        )
        self.descriptionLabel.setAlignment(
            Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.setWindowTitle("ProductSearcher")



class ProductTable(QScrollArea):
    def __init__(self, top:ProductSearcher):
        super().__init__(top)
        self.setGeometry(QRect(470,30,400,440))
        self.setWidgetResizable(True)
        self.contents = QWidget()
        self.contents.setGeometry(0,0,400,430)
        self.layout = QVBoxLayout(self.contents)
        self.table = QTableWidget(self.contents)
        self.table.setFont(smallFont)
        self.table.setColumnCount(2)
        self.table.setRowCount(2)
        self.layout.addWidget(self.table)
        ti = QTableWidgetItem()
        ti.setText("siema")
        self.table.setItem(0,0,ti)

        self.setWidget(self.contents)

    def displayProductList(self, prodList):
        pass

    
    def clearTable(self):
        pass
