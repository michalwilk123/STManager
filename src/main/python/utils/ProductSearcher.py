from __future__ import annotations
from PyQt5.QtWidgets import (QDialog, QTableWidget,
    QScrollArea, QWidget, QVBoxLayout, QLabel, QPushButton, QFrame,
    QDateEdit, QComboBox, QLineEdit, QCheckBox, QTableWidgetItem,
    QHeaderView, QAbstractScrollArea)
from PyQt5.QtCore import QRect, Qt
from PyQt5.QtGui import QFont, QPixmap
from utils.AppController import AppController
from utils.AppDataController import findProducts, getUsrList

smallFont = QFont()
smallFont.setPointSize(9)
bigFont = QFont()
bigFont.setPointSize(14)

class ProductSearcher(QDialog):
    def __init__(self):
        super().__init__()
        self.setFixedSize(880,560) 
        self.tableScrollArea = ProductTable(self)
        self.usrList = getUsrList()

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
        self.userComboBox.addItems(self.usrList)

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
        self.tableScrollArea.displayProductList(
            findProducts()
        )
        self.findButton.clicked.connect(self.findButtonClicked)
        self.nextPhotoButton.clicked.connect(self.nextPhotoClicked)
        self.prevPhotoButton.clicked.connect(self.previousPhotoClicked)


    def findButtonClicked(self):
        id = self.idLEdit.text() if self.idCBox.isChecked() else None
        usr = self.userComboBox.currentText() if self.userCBox.isChecked() else None
        phrase = self.phraseLEdit.text() if self.phraseCBox.isChecked() else None
        dateFrom = self.dateFromDEdit.text() if\
            self.dateFromCBox.isChecked() else None
        dateTo = self.dateToDEdit.text() if\
            self.dateToCBox.isChecked() else None
        self.tableScrollArea.displayProductList(
            findProducts(
                id=id, username=usr, phrase=phrase,
                timeFrom=dateFrom, timeTo=dateTo
            ),
            usr
        )


    def nextPhotoClicked(self):
        if self.currentItem is None:    return 
        self.photoCursor += 1
        if len(self.currentItem["filenames"]) == self.photoCursor:  self.photoCursor = 0
        self.reloadPhoto()


    def previousPhotoClicked(self):
        if self.currentItem is None:    return 
        self.photoCursor -= 1
        if self.photoCursor < 0:    self.photoCursor = len(self.currentItem["filenames"]) - 1
        self.reloadPhoto()

    
    def selectCurrentProduct(self, item):
        self.currentItem = item
        self.photoCursor = 0

        self.reloadPhoto()
        self.idLabel.setText("Id: {}".format(item["id"]))
        self.descriptionLabel.setText(item["desc"])
        self.createdDate.setText(item["creation_date"])
        self.lastModLabel.setText(item["last_updated"])


    def reloadPhoto(self):
        if not self.currentItem["filenames"]:   return 

        pixmap = QPixmap()
        loaded = pixmap.load(self.currentItem["filenames"][self.photoCursor])
        self.photoLabel.setPixmap(
            pixmap.scaled(
                self.photoLabel.width(),
                self.photoLabel.height(),
                Qt.IgnoreAspectRatio,
                Qt.FastTransformation
            )
        )



class ProductTable(QScrollArea):
    def __init__(self, top:ProductSearcher):
        super().__init__(top)
        self.top = top
        self.setGeometry(QRect(470,30,400,440))
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setWidgetResizable(True)
        self.contents = QWidget()
        self.contents.setGeometry(0,0,400,430)
        self.layout = QVBoxLayout(self.contents)
        self.table = QTableWidget(self.contents)
        microfont = QFont()
        microfont.setPointSize(7)
        self.table.setFont(microfont)
        self.table.setColumnCount(5)
        self.table.setRowCount(2)
        self.layout.addWidget(self.table)
        self.setWidget(self.contents)
        self.table.verticalHeader().setDefaultSectionSize(40)
        self.table.setSizeAdjustPolicy(
            QAbstractScrollArea.AdjustToContents
        )

        heading = ["Nr", "Name", "User", "Created", "Description"]
        for i, h in enumerate(heading):
            e = QTableWidgetItem()
            e.setText(h)
            e.setTextAlignment(Qt.AlignTop|Qt.AlignLeft)
            self.table.setItem(0, i,e)

        self.table.setRowHeight(0,20)
        self.table.cellClicked.connect(self.cellClicked)


    def displayProductList(self, prodList, user:str=None):
        self.clearTable()
        self.table.setRowCount(len(prodList)+1)
        self.top.titleLabel.setText(f"Results:    {len(prodList)}")
        self.prodList = prodList
        for i, row in enumerate(prodList, 1):
            e = QTableWidgetItem()
            e.setText(str(i))
            self.table.setItem(i,0,e)
            
            row = [
                row["id"][0:20],
                row["user"] if user is None else user,
                row["creation_date"],
                row["desc"]
            ]

            for j, col in enumerate(row, 1):
                e = QTableWidgetItem()
                e.setText(str(col))
                e.setTextAlignment(Qt.AlignTop|Qt.AlignLeft)
                self.table.setItem(i,j, e)
        if len(prodList):
            self.top.selectCurrentProduct(
                prodList[0]
            )
        self.table.resizeColumnsToContents()

    
    def clearTable(self):
        self.prodList = []
        for i in range(self.table.rowCount() - 1):
            self.table.removeRow(1)


    def newEntry(self, value:str):
        e = QTableWidgetItem()
        e.setText(value)
        return e


    def cellClicked(self, row:int, column:int):
        print(f"row: {row} | col: {column}")
        if row > len(self.prodList):
            print("no item exist")
            return 

        self.top.selectCurrentProduct(
            self.prodList[row-1]
        )