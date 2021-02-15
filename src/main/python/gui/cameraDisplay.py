from PyQt5.QtWidgets import QFrame, QPushButton, QWidget, QLabel
from PyQt5.QtCore import QCoreApplication, QRect, Qt, QTimer
from PyQt5.QtGui import QImage, QPixmap
from config.macros import FRAME_RATE, FRAMES_BEETWEEN_SCANS, BEEP_SOUND_PATH
from pyzbar import pyzbar
from playsound import playsound
from threading import Thread
import cv2
import os
import time


class CameraDisplayFrame(QFrame):
    def __init__(self, top):
        super().__init__(top.centralwidget)
        self.top = top
        self.setGeometry(QRect(10, 10, 741, 561))
        self.setAutoFillBackground(False)
        self.setFrameShape(QFrame.StyledPanel)
        self.setFrameShadow(QFrame.Raised)
        self.setObjectName("cameraDisplayFrame")
        self.initUI()


    def initUI(self):
        # create a label
        return 
        self.save_seq = 1
        self.label = QLabel(self)
        self.label.setGeometry(QRect(0, 0, 741, 561))
        self.pictureRequest = False
        self.newProduct = True
        self.camera_name = "qwerty"
        self.barcodes = []

        self.spacingCounter = 0
        self.ovCapture = cv2.VideoCapture(self.top.getCameraIndex())
        self.timer = QTimer(self.top.centralwidget)
        self.timer.setInterval(int((1 / FRAME_RATE) * 1000))
        self.timer.timeout.connect(self.nextFrame)
        self.timer.start()


    def nextFrame(self):
        ret, frame = self.ovCapture.read()

        if self.pictureRequest:
            path = self.top.getPhotoDestinationPath()
            timestamp = time.strftime("%d-%m-%Y-%H_%M_%S")
            print(path)

            cv2.imwrite(
                os.path.join(
                    path, "%s-%04d-%s.jpg" % (
                        self.top.username,
                        self.save_seq,
                        timestamp
                    )
                ),
                frame
            )
            self.save_seq += 1
            self.pictureRequest = False

        
        if self.newProduct:
            # if we already know product barcode, we stop scanning for better performance

            if self.spacingCounter == FRAMES_BEETWEEN_SCANS and ret:
                # looking for barcode in camera input
                self.spacingCounter=0
                self.barcodes = pyzbar.decode(frame)
            else:   self.spacingCounter+=1

            for barcode in self.barcodes:
                # printing highlight of found barcodes
                (x,y,width,height) = barcode.rect
                cv2.rectangle(frame, (x, y), (x + width, y + height), (0, 0, 255), 4)
                barcodeData = barcode.data.decode("utf-8")
                barcodeType = barcode.type

            if self.barcodes:
                Thread(target=lambda:playsound(BEEP_SOUND_PATH)).run()

                self.top.productManagerFrame.setBarcode(
                    self.barcodes[0].data.decode("utf-8")
                )
                self.newProduct = False

        if ret:
            # setting up preview
            rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgbImage.shape
            bytesPerLine = ch * w
            # per interval we switch image from the camera
            self.label.setPixmap(QPixmap.fromImage(
                QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
                    .scaled(640, 480, Qt.KeepAspectRatio)
            ))
        else: print("lost connection")

        

    def takePicture(self):  self.pictureRequest = True

    
    def noDeviceDialog(self):
        print("no device detected")


    def setup(self):
        pass

