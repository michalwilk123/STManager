"""
Managing camera input and barcode detection
"""
from __future__ import annotations
from PyQt5.QtWidgets import QFrame, QLabel, QSizePolicy
from PyQt5.QtCore import QRect, Qt, QThread, pyqtSlot, pyqtSignal
from PyQt5.QtGui import QImage, QPixmap, QResizeEvent
from config.macros import FRAME_RATE, FRAMES_BEETWEEN_SCANS
from pyzbar import pyzbar
from playsound import playsound
from threading import Thread
import cv2
import os
import time


class CameraPreviewThread(QThread):
    change_pixmap = pyqtSignal(QImage)
    ms_per_frame = int((1 / FRAME_RATE) * 1000)
    pictureRequest = False

    def __init__(
        self,
        parent: CameraDisplayFrame,
        width: int,
        height: int,
        scannerMode: bool = True,
        save_seq: int = 1,
        camera_name: str = "None",
        deviceNum: int = None,
    ):
        super().__init__(parent)
        CameraPreviewThread.top = parent
        CameraPreviewThread._save_seq = save_seq
        CameraPreviewThread.camera_name = camera_name
        CameraPreviewThread.deviceNum = deviceNum
        CameraPreviewThread.width = width
        CameraPreviewThread.height = height
        CameraPreviewThread.scannerMode = scannerMode
        CameraPreviewThread.newProduct = True

    @staticmethod
    def getLastPath() -> str:
        return CameraPreviewThread.currentPath

    def run(self):
        cap = cv2.VideoCapture(CameraPreviewThread.deviceNum)
        spacingCounter = 0
        barcodes = []
        from appContext import context

        beepSoundPath = context.get_resource("beep.mp3")

        while (
            not self.isInterruptionRequested()
            and CameraPreviewThread.deviceNum is not None
        ):

            ret, frame = cap.read()

            if CameraPreviewThread.pictureRequest:
                cv2.imwrite(CameraPreviewThread.currentPath, frame)
                CameraPreviewThread._save_seq += 1
                CameraPreviewThread.pictureRequest = False

            if (
                CameraPreviewThread.newProduct
                and not CameraPreviewThread.scannerMode
            ):

                if spacingCounter == FRAMES_BEETWEEN_SCANS and ret:
                    # looking for barcode in camera input
                    spacingCounter = 0
                    barcodes = pyzbar.decode(frame)
                else:
                    spacingCounter += 1

                for barcode in barcodes:
                    # printing highlight of found barcodes
                    (x, y, width, height) = barcode.rect
                    cv2.rectangle(
                        frame, (x, y), (x + width, y + height), (0, 0, 255), 4
                    )

                if barcodes:
                    t = Thread(target=lambda: playsound(beepSoundPath))
                    t.start()

                    CameraPreviewThread.top.top.productManagerFrame.setBarcode(
                        barcodes[0].data.decode("utf-8")
                    )
                    CameraPreviewThread.newProduct = False
                    barcodes = []
                    CameraPreviewThread.top.top.controller.saveCurrentProduct()

            if ret:
                rgbImage = cv2.resize(
                    cv2.cvtColor(frame, cv2.COLOR_BGR2RGB),
                    (CameraPreviewThread.width, CameraPreviewThread.height),
                )

                h, w, ch = rgbImage.shape
                bytesPerLine = ch * w
                self.change_pixmap.emit(
                    QImage(
                        rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888
                    ).scaled(
                        CameraPreviewThread.width,
                        CameraPreviewThread.height,
                        Qt.KeepAspectRatio,
                    )
                )
            else:
                CameraPreviewThread.deviceNum = None
            QThread.msleep(CameraPreviewThread.ms_per_frame)


class CameraDisplayFrame(QFrame):
    def __init__(self, top):
        """
        top - appView to connect component to
        the rest of the application
        """
        super().__init__()
        self.top = top
        self.setMinimumSize(800,640)
        self.setAutoFillBackground(False)
        self.setFrameShape(QFrame.StyledPanel)
        self.setFrameShadow(QFrame.Raised)
        self.setObjectName("cameraDisplayFrame")
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # UNCOMMENT BELOW COMMENT FOR CAMERA OUTPUT
        self.initUI()

    def initUI(self):
        """
        Initializing live camera preview
        """
        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignTop)

        self.label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.label.setMinimumSize(self.width(), self.height())

        self.cameraThread = CameraPreviewThread(
            self, self.width(), self.height(), deviceNum=0
        )
        self.cameraThread.change_pixmap.connect(self.setImage)
        self.cameraThread.start()

        self.resizeEvent = self.cameraDisplayResize

    def setScannerMode(self, mode: bool):
        CameraPreviewThread.scannerMode = mode

    @pyqtSlot(QImage)
    def setImage(self, image):
        self.label.setPixmap(QPixmap.fromImage(image))

    def cameraDisplayResize(self, e):
        """
        Method that executes when widget is resized
        """
        CameraPreviewThread.width = self.width()
        CameraPreviewThread.height = self.height()
        self.label.setMinimumHeight(self.height())
        self.label.setMinimumWidth(self.width())

    def takePicture(self, savePath: str, username: str = "Anonim"):
        timestamp = time.strftime("%d-%m-%Y-%H_%M_%S")
        CameraPreviewThread.currentPath = os.path.join(
            savePath,
            "%s-%04d-%s.jpg"
            % (username, CameraPreviewThread._save_seq, timestamp),
        )
        CameraPreviewThread.user = username
        CameraPreviewThread.pictureRequest = True
        # below we are wating 2 frames for the saving to take place
        # after that we expect for the picture to be loaded correctly
        QThread.msleep(CameraPreviewThread.ms_per_frame * 2)

    def noDeviceDialog(self):
        from utils.DialogCollection import errorOccured

        errorOccured("no device detected")

    def setup(self, mode: bool):
        CameraPreviewThread.scannerMode = mode

    def turnOffCamera(self):
        self.cameraThread.requestInterruption()
        self.cameraThread.wait()