from gui.mainApp import UiMainWindow
from PyQt5.QtWidgets import QMainWindow, QApplication

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = UiMainWindow()
    app.aboutToQuit.connect(ui.cleanUp)
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())