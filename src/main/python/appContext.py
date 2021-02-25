from fbs_runtime.application_context.PyQt5 import ApplicationContext
from PyQt5.QtGui import QPixmap

context = ApplicationContext()

noImagePixmap = QPixmap()
noImagePixmap.load(
    context.get_resource("noImageAvailable.png")
)