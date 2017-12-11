from PyQt5.QtWidgets import (QVBoxLayout, QWidget)

from glwidget import GLWidget

class Window(QWidget):
    def __init__(self, width, height):
        super(Window, self).__init__()
        self.setFixedSize(width, height)

        self.glWidget = GLWidget()
        mainLayout = QVBoxLayout(self)
        mainLayout.addWidget(self.glWidget)
        self.setLayout(mainLayout)
