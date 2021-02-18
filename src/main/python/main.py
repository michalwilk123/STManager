from gui.mainApp import UiMainWindow
from PyQt5.QtWidgets import QMainWindow, QApplication

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    MainWindow = UiMainWindow()
    app.aboutToQuit.connect(MainWindow.cleanUp)
    MainWindow.show()
    sys.exit(app.exec_())