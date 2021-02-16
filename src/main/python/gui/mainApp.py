from PyQt5.QtCore import QRect, QMetaObject, QCoreApplication 
from PyQt5.QtWidgets import QWidget, QFrame, QScrollArea, \
    QPushButton, QAction, QMenu, QApplication, QMainWindow, \
    QStatusBar, QTextEdit, QMenuBar, QLabel
from gui.productManager import ProductManagerFrame
from gui.settingsButtons import SettingsButtonsFrame
from gui.cameraDisplay import CameraDisplayFrame
from utils.User import User
import utils.AppDataController as adc
import pathlib


class UiMainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1100, 700)
        configuration = adc.getConfiguration()
        self.saveDestination = configuration["savePath"]
        self.user = User(self, configuration["loggedUser"], self.saveDestination)
        self.scannerMode = configuration["scanner_mode"]

        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.productManagerFrame = ProductManagerFrame(self)
        self.settingButtonsFrame = SettingsButtonsFrame(self)

        self.cameraDisplayFrame = CameraDisplayFrame(self)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setGeometry(QRect(0, 0, 1100, 30))
        self.menubar.setObjectName("menubar")

        self.settingsMenu = QMenu(self.menubar)
        self.settingsMenu.setObjectName("settingsMenu")

        self.applicationMenu = QMenu(self.menubar)
        self.applicationMenu.setObjectName("applicationMenu")

        self.aboutMenu = QMenu(self.menubar)
        self.aboutMenu.setObjectName("aboutMenu")
        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.statusbar.setFixedHeight(20)
        self.statusbar.setStyleSheet(
            "font-size: 10px;"
        )

        self.statusInfo = QLabel(f"Logged as user {self.user.getUsername()}")
        self.statusInfo.setGeometry(QRect(0,0,20,20))
        self.statusbar.addWidget(self.statusInfo)

        # Actions choices
        self.selectFolderAction = QAction(MainWindow)
        self.selectFolderAction.setObjectName("selectFolderAction")
        self.historyAction = QAction(MainWindow)
        self.historyAction.setObjectName("historyAction")
        self.themeAction = QAction(MainWindow)
        self.themeAction.setObjectName("themeAction")
        self.showProductsAction = QAction(MainWindow)
        self.showProductsAction.setObjectName("showProductsAction")
        self.nextProductAction = QAction(MainWindow)
        self.nextProductAction.setObjectName("nextProductAction")
        self.photoAction = QAction(MainWindow)
        self.photoAction.setObjectName("photoAction")
        self.importDbAction = QAction(MainWindow)
        self.importDbAction.setObjectName("importDbAction")
        self.changeUserAction = QAction(MainWindow)
        self.changeUserAction.setObjectName("changeUserAction")
        self.authorAction = QAction(MainWindow)
        self.authorAction.setObjectName("authorAction")
        self.contactAction = QAction(MainWindow)
        self.contactAction.setObjectName("contactAction")

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

        self.retranslateUi(MainWindow)
        QMetaObject.connectSlotsByName(MainWindow)
        self.setup()


    def retranslateUi(self, MainWindow):
        _translate = QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Product Archiver 2021 - version 0.0.1"))
        self.settingsMenu.setTitle(_translate("MainWindow", "Settings"))
        self.applicationMenu.setTitle(_translate("MainWindow", "Application"))
        self.aboutMenu.setTitle(_translate("MainWindow", "About"))
        self.selectFolderAction.setText(_translate("MainWindow", "Select Folder"))
        self.historyAction.setText(_translate("MainWindow", "History"))
        self.themeAction.setText(_translate("MainWindow", "Theme"))
        self.showProductsAction.setText(_translate("MainWindow", "Show products (S)"))
        self.nextProductAction.setText(_translate("MainWindow", "Next product (N)"))
        self.photoAction.setText(_translate("MainWindow", "Photo (P)"))
        self.importDbAction.setText(_translate("MainWindow", "Import database"))
        self.changeUserAction.setText(_translate("MainWindow", "Change user"))
        self.authorAction.setText(_translate("MainWindow", "Author"))
        self.contactAction.setText(_translate("MainWindow", "Contact"))

    
    def getPhotoDestinationPath(self):
        return self.saveDestination

    
    def setup(self):
        self.productManagerFrame.setup()
        self.settingButtonsFrame.setup()
        self.cameraDisplayFrame.setup()

    
    def getCameraIndex(self):
        return 0

    
    def cleanUp(self):
        """
        Slot connected to signal aboutToQuit from QApplication
        """
        self.cameraDisplayFrame.turnOffCamera()
        return 0

    def getCurrentUser(self) -> User:
        return self.user