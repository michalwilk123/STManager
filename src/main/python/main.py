from gui.AppView import AppView
from PyQt5.QtWidgets import QApplication

if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    MainWindow = AppView()
    app.aboutToQuit.connect(MainWindow.cleanUp)
    MainWindow.show()
    sys.exit(app.exec_())
