from gui.AppView import AppView
from appContext import context
from qtmodern.styles import dark as darkStyleSheet

if __name__ == "__main__":
    import sys
    
    darkStyleSheet(context.app)
    MainWindow = AppView()
    context.app.aboutToQuit.connect(MainWindow.cleanUp)
    MainWindow.show()
    sys.exit(context.app.exec_())
