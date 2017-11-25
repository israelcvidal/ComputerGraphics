from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage,QPixmap
from PyQt5.QtWidgets import (QHBoxLayout,
							QVBoxLayout,
							QSlider,
        					QWidget,
        					QLabel,
        					QTabWidget)

from glwidget import GLWidget

class Window(QWidget):
    def __init__(self,width,height):
        super(Window, self).__init__()
        self.setFixedSize(width,height);

        self.gl_tab = QWidget()
        self.ray_casting_tab = QWidget()
        self.tablewidget = QTabWidget()
        self.mainLayout = QVBoxLayout(self)
        
        ############################################
        # Ray Casting
        # 
        rayCastingLayout = QVBoxLayout()
        self.imageLabel = QLabel()
        
        rayCastingLayout.addWidget(self.imageLabel)
        self.ray_casting_tab.setLayout(rayCastingLayout)
        
        ############################################
        # OpenGL
        self.glWidget = GLWidget()

        self.xSlider = self.createSlider()
        self.ySlider = self.createSlider()
        self.zSlider = self.createSlider()

        self.xSlider.valueChanged.connect(self.glWidget.setXRotation)
        self.glWidget.xRotationChanged.connect(self.xSlider.setValue)
        self.ySlider.valueChanged.connect(self.glWidget.setYRotation)
        self.glWidget.yRotationChanged.connect(self.ySlider.setValue)
        self.zSlider.valueChanged.connect(self.glWidget.setZRotation)
        self.glWidget.zRotationChanged.connect(self.zSlider.setValue)

        self.horizontalx = QHBoxLayout()
        self.horizontaly = QHBoxLayout()
        self.horizontalz = QHBoxLayout()

        self.labelx = QLabel("X axis")
        self.labely = QLabel("Y axis")
        self.labelz = QLabel("Z axis")

        self.horizontalx.addWidget(self.labelx)
        self.horizontalx.addWidget(self.xSlider)
        self.horizontaly.addWidget(self.labely)
        self.horizontaly.addWidget(self.ySlider)
        self.horizontalz.addWidget(self.labelz)
        self.horizontalz.addWidget(self.zSlider)

        glLayout = QVBoxLayout()
        glLayout.addWidget(self.glWidget)
        glLayout.addLayout(self.horizontalx)
        glLayout.addLayout(self.horizontaly)
        glLayout.addLayout(self.horizontalz)
        self.gl_tab.setLayout(glLayout)

        self.xSlider.setValue(15 * 16)
        self.ySlider.setValue(345 * 16)
        self.zSlider.setValue(0 * 16)
        ############################################

        self.tablewidget.addTab(self.ray_casting_tab,"RayCasting")
        self.tablewidget.addTab(self.gl_tab,"OpenGL")

        self.mainLayout.addWidget(self.tablewidget)
        self.setLayout(self.mainLayout)
        self.setWindowTitle("Computer Graphics Project")

    def createSlider(self):
        slider = QSlider(Qt.Horizontal)

        slider.setRange(0, 360 * 16)
        slider.setSingleStep(16)
        slider.setPageStep(15 * 16)
        slider.setTickInterval(15 * 16)
        slider.setTickPosition(QSlider.TicksRight)

        return slider

    def computeOpeningSize(self):
        width = self.ray_casting_tab.frameGeometry().width()
        height = self.ray_casting_tab.frameGeometry().height()
        return width,height


    def paint(self, screen):
        image = QImage(screen, screen.shape[1],\
                            screen.shape[0],QImage.Format_RGB888)
        
        pix = QPixmap.fromImage(image)
        self.imageLabel.setPixmap(pix)
