from PyQt5.QtCore import QRect, QMetaObject, QCoreApplication 
from PyQt5.QtWidgets import QWidget, QFrame, QScrollArea, \
    QPushButton, QAction, QMenu, QApplication, QMainWindow, \
    QStatusBar, QTextEdit, QMenuBar, QLabel
from gui.productManager import ProductManagerFrame
from gui.settingsButtons import SettingsButtonsFrame
from gui.cameraDisplay import CameraDisplayFrame
from utils.AppContoller import AppController
import utils.AppDataController as adc
import pathlib


class UiMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(1100, 700)

        from utils.DialogCollection import logUserIn, createAccout, \
            showInfo, cameraChoice, getFolderPath
        # l, p = logUserIn()
        # l, p = createAccout()
        # showInfo()
        # c = cameraChoice()
        # print(c)
        # c = getFolderPath()
        # print(c)
        # print(f"login: {l}\npassword: {p}")

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
        self.statusbar.setStyleSheet(
            "font-size: 10px;"
        )

        self.statusInfo = QLabel()
        self.statusInfo.setGeometry(QRect(0,0,20,20))
        self.statusbar.addWidget(self.statusInfo)

        # Actions choices
        self.selectFolderAction = QAction(parent=self, text="Select Folder")
        self.historyAction = QAction(parent=self, text="History")
        self.themeAction = QAction(parent=self, text="Theme")
        self.showProductsAction = QAction(parent=self, text="Show products (S)")
        self.nextProductAction = QAction(parent=self, text="Next product (N)")
        self.photoAction = QAction(parent=self, text="Photo (P)")
        self.importDbAction = QAction(parent=self, text="Import database")
        self.changeUserAction = QAction(parent=self, text="Change user")
        self.authorAction = QAction(parent=self, text="Author")
        self.contactAction = QAction(parent=self, text="Contact")

        self.settingsMenu.addAction(self.selectFolderAction)
        self.settingsMenu.addAction(self.historyAction)
        self.settingsMenu.addAction(self.themeAction)
        self.settingsMenu.addAction(self.importDbAction)
        self.applicationMenu.addAction(self.showProductsAction)
        self.applicationMenu.addAction(self.nextProductAction)
        self.applicationMenu.addAction(self.photoAction)
        self.applicationMenu.addAction(self.changeUserAction)
        self.aboutMenu.addAction(self.authorAction)
        self.aboutMenu.addAction(self.contactAction)
        self.menubar.addAction(self.applicationMenu.menuAction())
        self.menubar.addAction(self.settingsMenu.menuAction())
        self.menubar.addAction(self.aboutMenu.menuAction())

        self.setWindowTitle("Product Archiver 2021 - version 0.0.1")
        self.setup()


    def getPhotoDestinationPath(self):
        return self.saveDestination

    
    def setup(self):
        configuration = adc.getConfiguration()
        self.saveDestination = configuration["savePath"]
        self.controller = AppController(self, configuration["loggedUser"], self.saveDestination)
        self.scannerMode = configuration["scanner_mode"]
        self.productManagerFrame.setup()
        self.settingButtonsFrame.setup()
        self.cameraDisplayFrame.setup()
        self.statusInfo.setText(f"Logged as user {self.controller.getUsername()}")

        # connecting ui buttons signals
        self.productManagerFrame.confirmButton.clicked.connect(
            self.controller.saveCurrentProduct
        )
        self.productManagerFrame.cancelButton.clicked.connect(
            self.controller.deleteCurrentProduct
        )

        self.settingButtonsFrame.photoButton.clicked.connect(
            self.controller.takePhoto
        )
        self.settingButtonsFrame.showProductsButton.clicked.connect(
            lambda:print("tutaj powinno sie wyswietlic okno z wyborem produktu")
        )
        self.settingButtonsFrame.changeUserButton.clicked.connect(
            self.controller.switchUser
        )
        self.settingButtonsFrame.nextProductButton.clicked.connect(
            self.controller.nextProduct
        )
        self.settingButtonsFrame.prevProductButton.clicked.connect(
            self.controller.previousProduct
        )

    
    def getCameraIndex(self):
        return 0

    
    def cleanUp(self):
        """
        Slot connected to signal aboutToQuit from QApplication
        """
        self.controller.cleanUp()
        self.cameraDisplayFrame.turnOffCamera()
        return 0

    def getController(self) -> AppController:
        return self.controller