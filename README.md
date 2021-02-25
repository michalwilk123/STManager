# __Stocktake Manager__
### ![There should be big app icon](src/main/icons/githubIcon.png)
---

* __Do you lose revenue from false customer complains?__
* __Do you need to manage many unrelated products?__
* __Are you strugging to find a way to organise your products?__
* __Do you want need small and easy program to organise product data for a stocktake?__

#### If answered YES to any of the above question then i have a perfect app for you!

### Short description
__Stocktake Manager__ takes photos of your products, corelates them with their product barcode
and then lets you go through them.

App manages to detect barcodes from camera or from hand scanner(_when scanner mode selected_).
You can then search through the products and chose many of the available filters to find the
exact item you are looking for.

---

### Download prebuild version:
* [Windows](dnjsak)
* [Linux](dsadsa)
* ~Mac~

<br/>

### Technologies:

* __python 3.9__ - used annotation available in only python version 3.8+
* __PyQt5__  - interface
* __opencv__ - middleman beetween qt5 and pyzbar
* __pyzbar__ - barcode detection

<br/>

### Other python tools used:
* __flake8__ - linting
* __black__  - small reformatting improvments
* __pipenv__ - managing packages

<br/>

### Build intructions:
__Run application from source__
```bash
git clone https://github.com/michalwilk123/StocktakeManager.git
make install
make
```

__Create an executable for the app__
```bash
git clone https://github.com/michalwilk123/StocktakeManager.git
make install
make build
```
