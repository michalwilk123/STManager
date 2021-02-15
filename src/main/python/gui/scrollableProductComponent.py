from PyQt5.QtWidgets import QFrame, QPushButton, QLabel, QSizePolicy, QScrollArea,\
    QVBoxLayout, QSpacerItem, QWidget
from PyQt5.QtCore import QRect, Qt, QMetaObject, QSize


class ScrollPreviewComponent(QFrame):
    def __init__(self, top):
        super().__init__(top)
        self.resize(330, 300)
        self.setMaximumSize(QSize(330,300))
        #self.setStyleSheet("background-color:white;")
        self.scroll = QScrollArea(self)
        self.scroll.setGeometry(QRect(0,0,330,300))
        sp = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        sp.setHorizontalStretch(0)
        sp.setVerticalStretch(0)
        sp.setHeightForWidth(self.scroll.sizePolicy().hasHeightForWidth())
        self.scroll.setSizePolicy(sp)

        self.scroll.setMinimumHeight(100)
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)

        self.scrollContents = QWidget()
        self.scrollContents.setGeometry(QRect(0,0,345,285))
        self.spacer = QSpacerItem(20,40,QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.vLayout = QVBoxLayout(self.scrollContents)
        self.vLayout.addSpacerItem(self.spacer)
        self.scroll.setWidget(self.scrollContents)

        for i in range(10):
            b = ItemPreviewComponent("Przykładowe dane o produkcie")
            b.setStyleSheet("background-color:red;")
            self.vLayout.insertWidget(0,b)

    def addItemPreview(self):
        ip = ItemPreviewComponent(self)
        self.vLayout.insertWidget(-2, ip)



class ItemPreviewComponent(QFrame):
    def __init__(self, productShortInfo):
        super().__init__()
        self.label = QLabel()
        self.label.setGeometry(QRect(110,10,160,60))
        self.label.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.label.setWordWrap(True)

        self.delButton