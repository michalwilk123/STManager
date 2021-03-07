"""
This classes are responsible for the
scrollable components to the right of the app
"""
from PyQt5.QtWidgets import (
    QFrame,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QSpacerItem,
    QScrollArea,
    QWidget,
    QLabel,
)
from PyQt5.QtCore import QRect, Qt
from PyQt5.QtGui import QPixmap
from utils.DialogCollection import errorOccured
from appContext import noImagePixmap


class ScrollPreviewComponent(QFrame):
    def __init__(self, top):
        super().__init__()
        self.top = top
        self.setMinimumSize(380, 330)
        self.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        self.scroll = QScrollArea(self)
        self.scroll.setFixedSize(380,330)

        self.scroll.setMinimumHeight(100)
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignTop)

        self.scrollContents = QWidget()
        self.scrollContents.setGeometry(QRect(0, 0, 350, 330))
        self.spacer = QSpacerItem(
            20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding
        )

        self.vLayout = QVBoxLayout(self.scrollContents)
        self.vLayout.addSpacerItem(self.spacer)
        self.scroll.setWidget(self.scrollContents)
        self.itemPreviewList = []

    def addItemPreview(self, description: str, imgPath: str):
        ip = ItemPreviewComponent(self, description, imgPath)
        self.vLayout.insertWidget(0, ip)
        self.itemPreviewList.append(ip)

    def clearAll(self):
        while self.itemPreviewList:
            self.vLayout.removeWidget(self.itemPreviewList[0])
            self.itemPreviewList.pop(0)

    def getLayout(self) -> QVBoxLayout:
        return self.vLayout

    def getPreviewList(self):
        return self.itemPreviewList


class ItemPreviewComponent(QFrame):
    parent: ScrollPreviewComponent = None

    def __init__(
        self, parent: ScrollPreviewComponent, description: str, imgPath: str
    ):
        super().__init__()
        if ItemPreviewComponent.parent is None:
            ItemPreviewComponent.parent = parent

        self.setFixedHeight(80)
        self.imgPath = imgPath
        self.label = QLabel(description, self)
        self.label.setGeometry(QRect(110, 10, 130, 60))
        self.label.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignTop)
        self.label.setWordWrap(True)

        self.delButton = QPushButton(text="X", parent=self)
        self.delButton.setGeometry(QRect(260, 10, 30, 60))
        self.delButton.setStyleSheet(
            """
color: red;
font: 75 20pt;
"""
        )
        self.delButton.setFlat(True)
        self.delButton.clicked.connect(self.delButtonClicked)

        self.thbSeparator = QFrame(self)
        self.thbSeparator.setGeometry(QRect(100, 10, 5, 60))
        self.thbSeparator.setFrameShape(QFrame.VLine)
        self.thbSeparator.setFrameShadow(QFrame.Sunken)

        self.thbLabel = QLabel(self)
        self.thbLabel.setGeometry(QRect(10, 10, 80, 60))
        self.thbLabel.setWordWrap(True)

        pixmap = QPixmap()
        if not pixmap.load(imgPath):
            pixmap = noImagePixmap

        self.thbLabel.setPixmap(
            pixmap.scaled(80, 60, Qt.IgnoreAspectRatio, Qt.FastTransformation)
        )

        self.delSeparator = QFrame(self)
        self.delSeparator.setGeometry(QRect(250, 10, 5, 60))
        self.delSeparator.setFrameShape(QFrame.VLine)
        self.delSeparator.setFrameShadow(QFrame.Sunken)

        self.setFrameStyle(QFrame.StyledPanel)

    def delButtonClicked(self):
        ItemPreviewComponent.parent.vLayout.removeWidget(self)
        ItemPreviewComponent.parent.itemPreviewList.remove(self)
        ItemPreviewComponent.parent.top.top.controller.deletePhoto(
            self.imgPath
        )

        from os import remove, path

        if path.exists(self.imgPath):
            remove(self.imgPath)
        else:
            errorOccured("Image does not exist anymore!!")
