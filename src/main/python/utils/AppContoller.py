import utils.AppDataController as adc
from gui.cameraDisplay import CameraPreviewThread
import time


class AppController:
    def __init__(self, top, username:str, savePath:str):
        """
        Purpose of password is only user confirmation. NOT for security.
        """
        self.productList = adc.findProducts(username=username)
        self.itemCursor = len(self.productList) - 1
        self.username = username
        self.top = top
        self.savePath = savePath # this value decides where NEW photos will be stored
        self.changesMade = False
        self._updateProductView() # displaying current data


    @staticmethod
    def getCameraList():
        return ["camera1", "camera2", "camera3"]


    def getUsername(self): return self.username


    def switchUser(self):
        print("zmieniam uzytkownika")


    def takePhoto(self):
        """
        Fetches data from app and saves photo in user selected directory
        """
        self.top.cameraDisplayFrame.takePicture(self.savePath, self.username)
        photoPath:str = CameraPreviewThread.getLastPath()
        photoName:str = photoPath.split("/")[-1]
        # adding newly taken photo to preview scrollbar
        self.top.productManagerFrame.getScrollArea().addItemPreview(photoName, photoPath)
        self.productList[self.itemCursor]["filenames"].append(photoPath)
        self.changesMade = True

    
    def deletePhoto(self, photoPath:str):
        """
        Delete photo from the user data
        """
        try:
            self.productList[self.itemCursor]["filenames"].remove(photoPath)
        except ValueError:
            raise NotImplementedError("Tutaj powinien sie pojawic dialog z bledem")
        self.changesMade = True


    def saveCurrentProduct(self):
        self.productList[self.itemCursor]["id"] = self.top\
            .productManagerFrame.productBarcode.text()
        self.productList[self.itemCursor]["desc"] = self.top\
            .productManagerFrame.productDescription.toPlainText()
        self.changesMade = True


    def deleteCurrentProduct(self):
        if len(self.productList) == 1:
            self.productList = [adc.createNullProduct(0)]
            self.itemCursor = 0
            self.changesMade = True
            self._updateProductJson()
            self._updateProductView()
        else:
            self.changesMade = False
            self.previousProduct()


    def nextProduct(self):
        """
        Fetch data for next product of the list
        """
        print("next photo")
        self._updateProductJson()
        if self.itemCursor == len(self.productList) - 1:
            if self.productList[-1]["id"] != "":
                self._newProduct()
            else:
                self.itemCursor = 0
        else: self.itemCursor += 1
        self._updateProductView()


    def previousProduct(self):
        """
        switch view to previous product from the productList
        """
        print("previoous photo")
        self._updateProductJson()
        self.itemCursor = 0 if self.itemCursor == 0 else self.itemCursor - 1 
        self._updateProductView()


    def changeSaveUrl(self, newPath):   self.savePath = newPath


    def logout(self):
        pass


    def cleanUp(self):
        self._updateProductJson()


    def _updateProductJson(self):
        if not self.changesMade: 
            return
            print("aktualizujemy dane w pliku json")

        data = adc.getAllData()
        for userData in data["userData"]:
            if userData["username"] == self.username:
                userData["items"] = self.productList

        adc.setNewData(data)
        self.changesMade = False


    def _updateProductView(self):
        self.top.productManagerFrame.getScrollArea().clearAll()
        product = self.productList[self.itemCursor]

        # setting up previews for all photos
        for path in product["filenames"]:
            self.top.productManagerFrame.getScrollArea().addItemPreview(
                path.split("/")[-1], path
            )

        self.top.productManagerFrame.setBarcode(product["id"])
        self.top.productManagerFrame.setDescription(product["desc"])


    def _newProduct(self):
        """
        Clears data fields from app, and saves that data in json file.
        """
        self.changesMade = True
        self.productList.append(adc.createNullProduct(
            self.itemCursor+1
        ))
        self.itemCursor = len(self.productList) - 1
        self.productList[self.itemCursor]["creation_date"] = time.strftime("%d-%m-%Y-%H_%M_%S")
        self._updateProductView()
