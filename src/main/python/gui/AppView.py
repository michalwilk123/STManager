from PyQt5.QtCore import QRect, Qt
from PyQt5.QtWidgets import (
    QWidget,
    QAction,
    QMenu,
    QMainWindow,
    QStatusBar,
    QMenuBar,
    QLabel,
)
from gui.productManager import ProductManagerFrame
from gui.settingsButtons import SettingsButtonsFrame
from gui.cameraDisplay import CameraDisplayFrame
from utils.AppController import AppController
from utils.DialogCollection import showInfo, cameraChoice, createAccout


class AppView(QMainWindow):
    def __init__(self, forceRestart: bool = False):
        super().__init__()
        self.resize(1100, 700)
        self.cameraChoice = 0

        self.centralwidget = QWidget(self)
        self.productManagerFrame = ProductManagerFrame(self)
        self.settingButtonsFrame = SettingsButtonsFrame(self)
        self.cameraDisplayFrame = CameraDisplayFrame(self)

        self.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(self)
        self.menubar.setGeometry(QRect(0, 0, 1100, 30))
        self.settingsMenu = QMenu("Settings", self.menubar)
        self.applicationMenu = QMenu("Application", self.menubar)
        self.aboutMenu = QMenu("About", self.menubar)
        self.setMenuBar(self.menubar)

        self.statusbar = QStatusBar(self)
        self.setStatusBar(self.statusbar)
        self.statusbar.setFixedHeight(20)
        self.statusbar.setStyleSheet("font-size: 10px;")

        self.statusUser = QLabel()
        self.statusUser.setGeometry(QRect(0, 0, 20, 20))
        self.statusbar.addWidget(self.statusUser)

        # Actions choices
        self.selectFolderAction = QAction(parent=self, text="Select Folder")
        self.showProductsAction = QAction(
            parent=self, text="Show products (S)")
        self.photoAction = QAction(parent=self, text="Photo (P)")
        self.selectCameraAction = QAction(parent=self, text="Change camera")
        self.changeUserAction = QAction(parent=self, text="Change user")
        self.createUserAction = QAction(parent=self, text="Create new user")
        self.authorAction = QAction(parent=self, text="Author")
        self.scannerModeAction = QAction(parent=self, text="Scanner mode")
        self.scannerModeAction.setCheckable(True)

        self.settingsMenu.addAction(self.selectFolderAction)
        self.settingsMenu.addAction(self.selectCameraAction)
        self.settingsMenu.addAction(self.scannerModeAction)
        self.applicationMenu.addAction(self.showProductsAction)
        self.applicationMenu.addAction(self.photoAction)
        self.applicationMenu.addAction(self.changeUserAction)
        self.applicationMenu.addAction(self.createUserAction)
        self.aboutMenu.addAction(self.authorAction)
        self.menubar.addAction(self.applicationMenu.menuAction())
        self.menubar.addAction(self.settingsMenu.menuAction())
        self.menubar.addAction(self.aboutMenu.menuAction())

        self.setWindowTitle("Stocktake Manager 2021 - version 0.0.1")
        self.setup()

    def getPhotoDestinationPath(self):
        return self.saveDestination

    def updateStatusbar(self):
        self.statusUser.setText(
            f"Logged as user {self.controller.getUsername()}")

    def setup(self):
        self.controller = AppController(self)
        self.productManagerFrame.setup()
        self.settingButtonsFrame.setup()
        self.cameraDisplayFrame.setup(self.controller.getScannerMode())
        self.updateStatusbar()

        # connecting ui buttons signals
        self.productManagerFrame.confirmButton.clicked.connect(
            self.controller.saveCurrentProduct
        )
        self.productManagerFrame.cancelButton.clicked.connect(
            self.controller.deleteCurrentProduct
        )
        self.settingButtonsFrame.photoButton\
            .clicked.connect(self.controller.takePhoto)
        self.settingButtonsFrame.showProductsButton\
            .clicked.connect(self.searchProducts)
        self.settingButtonsFrame.changeUserButton.clicked.connect(
            self.controller.switchUser
        )
        self.settingButtonsFrame.nextProductButton.clicked.connect(
            self.controller.nextProduct
        )
        self.settingButtonsFrame.prevProductButton.clicked.connect(
            self.controller.previousProduct
        )
        self.productManagerFrame.productBarcode.returnPressed.connect(
            self.controller.takePhoto
        )

        # connecting actions buttons singals
        self.selectFolderAction.triggered.connect(
            self.controller.changeSaveUrl)
        self.showProductsAction.triggered.connect(self.searchProducts)
        self.photoAction.triggered.connect(self.controller.takePhoto)
        self.selectCameraAction.triggered.connect(self.showCameraChoice)
        self.changeUserAction.triggered.connect(self.controller.switchUser)
        self.createUserAction.triggered.connect(createAccout)
        self.authorAction.triggered.connect(showInfo)
        self.scannerModeAction.triggered.connect(
            self.controller.toggleScannerMode)

        if self.controller.getScannerMode():
            self.scannerModeAction.setChecked(True)

    def keyPressEvent(self, k):
        key = k.key()
        if key == Qt.Key_P:
            self.controller.takePhoto()
        elif key == Qt.Key_Enter:
            self.controller.saveCurrentProduct()
        elif key == Qt.Key_Delete:
            self.controller.deleteCurrentProduct()

    def setCameraIndex(self, i: int):
        self.cameraChoice = i

    def cleanUp(self):
        """
        Slot connected to signal aboutToQuit from QApplication
        """
        self.controller.cleanUp()
        self.cameraDisplayFrame.turnOffCamera()
        return 0

    def getCameraIndex(self) -> int:
        return self.cameraChoice

    def getController(self) -> AppController:
        return self.controller

    def searchProducts(self):
        from utils.ProductSearcher import ProductSearcher

        p = ProductSearcher()
        p.exec()

    def showCameraChoice(self):
        self.cameraChoice = cameraChoice()
