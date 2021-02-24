from gui.AppView import AppView
from appContext import context

if __name__ == "__main__":
    import sys

    MainWindow = AppView()
    context.app.aboutToQuit.connect(MainWindow.cleanUp)
    MainWindow.show()
    sys.exit(context.app.exec_())
