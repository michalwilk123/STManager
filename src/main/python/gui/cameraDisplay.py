from __future__ import annotations
from PyQt5.QtWidgets import QFrame, QPushButton, QWidget, QLabel, QSizePolicy
from PyQt5.QtCore import QCoreApplication, QRect, Qt, QThread, \
    pyqtSlot, pyqtSignal
from PyQt5.QtGui import QImage, QPixmap
from config.macros import FRAME_RATE, FRAMES_BEETWEEN_SCANS, BEEP_SOUND_PATH
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

    def __init__(self, parent, width:int, 
        height:int, 
        save_seq:int=1, camera_name:str="None", deviceNum:int=0):
        super().__init__(parent)
        CameraPreviewThread._save_seq = save_seq
        CameraPreviewThread.camera_name = camera_name
        CameraPreviewThread.deviceNum = deviceNum
        CameraPreviewThread.width = width
        CameraPreviewThread.height = height

    @staticmethod
    def getLastPath() -> str: return CameraPreviewThread.currentPath

    def run(self):
        cap = cv2.VideoCapture(CameraPreviewThread.deviceNum)
        newProduct = True
        spacingCounter = 0
        barcodes = []

        while not self.isInterruptionRequested():
            ret, frame = cap.read()

            if CameraPreviewThread.pictureRequest:

                cv2.imwrite(CameraPreviewThread.currentPath, frame)
                CameraPreviewThread._save_seq += 1
                CameraPreviewThread.pictureRequest = False

        
            if newProduct:
                # if we already know product barcode, we stop scanning for better performance
                if spacingCounter == FRAMES_BEETWEEN_SCANS and ret:
                    # looking for barcode in camera input
                    spacingCounter=0
                    barcodes = pyzbar.decode(frame)
                else:   spacingCounter+=1

                for barcode in barcodes:
                    # printing highlight of found barcodes
                    (x,y,width,height) = barcode.rect
                    cv2.rectangle(frame, (x, y), (x + width, y + height), (0, 0, 255), 4)
                    barcodeData = barcode.data.decode("utf-8")
                    barcodeType = barcode.type

                if barcodes:
                    Thread(target=lambda:playsound(BEEP_SOUND_PATH)).run()

                    top.productManagerFrame.setBarcode(
                        barcodes[0].data.decode("utf-8")
                    )
                    newProduct = False

            if ret:
                rgbImage = cv2.resize(
                    cv2.cvtColor(frame, cv2.COLOR_BGR2RGB),
                    (CameraPreviewThread.width, CameraPreviewThread.height)
                )
            
                h, w, ch = rgbImage.shape
                bytesPerLine = ch * w
                self.change_pixmap.emit(
                    QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
                        .scaled(
                            CameraPreviewThread.width, 
                            CameraPreviewThread.height, 
                            Qt.KeepAspectRatio
                        )
                )
            else: print("lost connection")
            QThread.msleep(CameraPreviewThread.ms_per_frame)



class CameraDisplayFrame(QFrame):
    def __init__(self, top:UiMainWindow):
        super().__init__(top.centralwidget)
        self.top = top
        self.setGeometry(QRect(10,10, 740, 570))
        self.setAutoFillBackground(False)
        self.setFrameShape(QFrame.StyledPanel)
        self.setFrameShadow(QFrame.Raised)
        self.setObjectName("cameraDisplayFrame")
        # UNCOMMENT BELOW COMMENT FOR CAMERA OUTPUT
        # self.initUI() 


    def initUI(self):
        """
        Initializing live camera preview
        """
        self.label = QLabel(self)
        self.label.setGeometry(QRect(0, 0, self.width(), self.height()))

        self.cameraThread = CameraPreviewThread(
            self, self.width(), self.height()
        )
        self.cameraThread.change_pixmap.connect(
            self.setImage
        )
        self.cameraThread.start()


    @pyqtSlot(QImage)
    def setImage(self, image):
        self.label.setPixmap(QPixmap.fromImage(image))


    def takePicture(self, savePath:str, username:str="Anonim"):  
        timestamp = time.strftime("%d-%m-%Y-%H_%M_%S")
        CameraPreviewThread.currentPath = os.path.join(
                savePath,
                "%s-%04d-%s.jpg" % (
                username,
                CameraPreviewThread._save_seq,
                timestamp
            )
        )
        CameraPreviewThread.user = username
        CameraPreviewThread.pictureRequest = True

    
    def noDeviceDialog(self):
        print("no device detected")


    def setup(self):
        pass

    def turnOffCamera(self):
        self.cameraThread.requestInterruption()
        self.cameraThread.wait()

