import utils.AppDataController as adc
from gui.cameraDisplay import CameraPreviewThread
from functools import cmp_to_key
import time


class AppController:
    def __init__(self, view):
        data = adc.getAllData(debug=True)
        self.username = data["configuration"]["loggedUser"]
        self.scannerMode = data["configuration"]["scanner_mode"]
        self.savePath = data["configuration"]["savePath"]

        self.productList = next(
            filter(lambda x: x["username"] == self.username, data["userData"])
        )["items"]

        self.productList.sort(
            key=cmp_to_key(
                lambda x, y: adc.compareDatetimes(
                    x["last_updated"], y["last_updated"]
                )
            )
        )

        if len(self.productList) == 0:
            from utils.AppDataController import createNullProduct

            self.productList = [createNullProduct(0)]

        self.itemCursor = len(self.productList) - 1
        self.view = view
        self.changesMade = False
        self._updateProductView()  # displaying current data

    @staticmethod
    def getCameraList():
        from PyQt5.QtMultimedia import QCameraInfo

        return [c.description() for c in QCameraInfo.availableCameras()]

    def getScannerMode(self):
        return self.scannerMode

    def toggleScannerMode(self):
        self.scannerMode = not self.scannerMode
        if self.scannerMode:
            self.view.productManagerFrame.productBarcode.setReadOnly(False)
            self.view.productManagerFrame.productBarcode.setFocus()
        else:
            self.view.productManagerFrame.productBarcode.setReadOnly(True)

        self.view.cameraDisplayFrame.setScannerMode(self.scannerMode)
        self.changesMade = True

    def getUsername(self) -> str:
        return self.username

    def switchUser(self):
        from utils.DialogCollection import logUserIn

        login, password = logUserIn()
        if login is None:
            return

        self.productList = adc.findProducts(username=login)
        self.itemCursor = len(self.productList) - 1
        self.username = login
        self.changesMade = True
        self.view.updateStatusbar()
        self._updateProductView()  # displaying current data

    def getNumOfProducts(self) -> int:
        return len(self.productList)

    def takePhoto(self):
        """
        Fetches data from app and saves photo in user selected directory
        """
        if CameraPreviewThread.deviceNum is None:
            print("no camera :(")
            return

        photoPath = self.view.cameraDisplayFrame.takePicture(
            self.savePath, self.username
        )

        if not photoPath:
            print("Could not create photo")
            return

        photoName: str = photoPath.split("/")[-1]
        # adding newly taken photo to preview scrollbar
        self.view.productManagerFrame.getScrollArea().addItemPreview(
            photoName, photoPath
        )
        self.productList[self.itemCursor]["filenames"].append(photoPath)
        self.productList[self.itemCursor]["last_updated"] = time.strftime(
            "%d-%m-%Y-%H_%M_%S"
        )
        self.changesMade = True

    def deletePhoto(self, photoPath: str):
        """
        Delete photo from the user data
        """
        self.productList[self.itemCursor]["filenames"].remove(photoPath)
        self.changesMade = True

    def saveCurrentProduct(self):
        """
        When you click this, information will be saved even if you
        prematuraly close the app.
        """
        cItem = self.productList[self.itemCursor]

        cItem["id"] = self.view.productManagerFrame.productBarcode.text()
        cItem[
            "desc"
        ] = self.view.productManagerFrame.productDescription.toPlainText()

        cItem["last_updated"] = time.strftime("%d-%m-%Y-%H_%M_%S")
        self.changesMade = True

    def deleteCurrentProduct(self):
        """
        deletes only INFO in json, photos ARE STAYING IN
        """
        if len(self.productList) == 1:
            self.productList = [adc.createNullProduct(0)]
            self.itemCursor = 0
            self.changesMade = True
            self._updateProductJson()
            self._updateProductView()
        else:
            self.changesMade = False
            cursor = self.itemCursor
            self.previousProduct()
            self.productList.pop(cursor)

    def nextProduct(self):
        """
        Fetch data for next product of the list
        """
        self._updateProductJson()
        if self.itemCursor == len(self.productList) - 1:
            if self.view.productManagerFrame.anyProduct():
                self._newProduct()
            else:
                self.itemCursor = 0
        else:
            self.itemCursor += 1
        self._updateProductView()

    def previousProduct(self):
        """
        switch view to previous product from the productList
        """
        self._updateProductJson()
        self.itemCursor = 0 if self.itemCursor == 0 else self.itemCursor - 1
        self._updateProductView()

    def changeSaveUrl(self, newPath: str):
        from utils.DialogCollection import getFolderPath

        self.savePath = getFolderPath(self.view)

    def cleanUp(self):
        self._updateProductJson()

    def _updateProductJson(self):
        if not self.changesMade:
            return

        data = adc.getAllData()
        for userData in data["userData"]:
            if userData["username"] == self.username:
                userData["items"] = self.productList

        data["configuration"]["loggedUser"] = self.username
        data["configuration"]["scanner_mode"] = self.scannerMode
        data["configuration"]["savePath"] = self.savePath
        adc.setNewData(data)
        self.changesMade = False

    def _updateProductView(self):
        self.view.productManagerFrame.getScrollArea().clearAll()

        product = self.productList[self.itemCursor]

        # setting up previews for all photos
        for path in product["filenames"]:
            self.view.productManagerFrame.getScrollArea().addItemPreview(
                path.split("/")[-1], path
            )

        self.view.productManagerFrame.setBarcode(product["id"])
        self.view.productManagerFrame.setDescription(product["desc"])
        if self.scannerMode:
            self.view.productManagerFrame.productBarcode.setFocus()
        else:
            self.view.productManagerFrame.productBarcode.setReadOnly(True)
        CameraPreviewThread.newProduct = True

    def _newProduct(self):
        """
        Clears data fields from app, and saves that data in json file.
        """
        self.changesMade = True
        self.productList.append(adc.createNullProduct(self.itemCursor + 1))
        self.itemCursor = len(self.productList) - 1
        self.productList[self.itemCursor]["creation_date"] = time.strftime(
            "%d-%m-%Y-%H_%M_%S"
        )
        self.productList[self.itemCursor]["last_updated"] = time.strftime(
            "%d-%m-%Y-%H_%M_%S"
        )
        self._updateProductView()
