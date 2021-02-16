import utils.AppDataController as adc
import time


class User:
    def __init__(self, top, username:str, savePath:str):
        """
        Purpose of password is only user confirmation. NOT for security.
        """
        self.productList = adc.findProducts(username=username)
        self.itemCursor = len(self.productList) - 1
        self.username = username
        self.top = top
        self.savePath = savePath
        self.changesMade = False
        self._updateProductView() # displaying current data


    def getUsername(self): return self.username

    def takePhoto(self):
        """
        Fetches data from app and saves photo in user selected directory
        """
        self.top.cameraDisplayFrame.takePicture(self.savePath, self.username)
        photoPath:str = self.top.cameraDisplayFrame.getLastPath()
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


    def newProduct(self):
        """
        Clears data fields from app, and saves that data in json file.
        """
        self.productList.append(adc.createNullProduct())
        self.itemCursor = len(self.productList) - 1
        self.productList[self.itemCursor]["creation_date"] = time.strftime("%d-%m-%Y-%H_%M_%S")
        self._showProduct()


    def nextProduct(self):
        """
        Fetch data for next product of the list
        """
        self._updateProductJson()
        if self.itemCursor == len(self.productList) - 1:
            if self.productList[-1]["id"] != "":
                self.newProduct()
            else:
                self.itemCursor = 0
        else: self.itemCursor += 1
        self._updateProductView()


    def previousPhoto(self):
        """
        switch view to previous product from the productList
        """
        self._updateProductJson()
        self.itemCursor = 0 if self.itemCursor == 0 else self.itemCursor - 1 
        self._updateProductView()


    def changeSaveUrl(self, newPath):   self.savePath = newPath


    def logout(self):
        pass


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


