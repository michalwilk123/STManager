from fbs_runtime.application_context.PyQt5 import ApplicationContext
from PyQt5.QtWidgets import QMainWindow, QLabel
from PyQt5.QtMultimedia import QCameraInfo, QCamera, QCameraImageCapture
from PyQt5.QtMultimediaWidgets import QCameraViewfinder
import sys

class CameraView(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setGeometry(100,100,800,600)
        self.camera = QCamera(QCameraInfo.availableCameras()[0])
        self.viewfinder = QCameraViewfinder()
        self.viewfinder.show()
        self.setCentralWidget(self.viewfinder)
        self.setWindowTitle("widok z kamery")
        self.camera.setViewfinder(self.viewfinder)
        self.camera.setCaptureMode(QCamera.CaptureStillImage)
        self.camera.error.connect(
            lambda: self.alert(self.camera.errorString())
        )
        self.camera.start()
        self.testLabel = QLabel(self)
        self.testLabel.setText("siemanko")
        self.testLabel.show()

    def keyPressEvent(self,event):
        print(event.key())


if __name__ == "__main__":
    context = ApplicationContext()
    window = CameraView()
    window.show()
    exit_code = context.app.exec_()
    sys.exit(exit_code)