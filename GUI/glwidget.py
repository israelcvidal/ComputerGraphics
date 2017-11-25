import math

from OpenGL.GL import *
# from OpenGL.GLU import *
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QOpenGLWidget
from PyQt5.QtCore import (pyqtSignal,
                        QPoint,
                        QSize,
                        Qt)

class GLWidget(QOpenGLWidget):
    xRotationChanged = pyqtSignal(int)
    yRotationChanged = pyqtSignal(int)
    zRotationChanged = pyqtSignal(int)

    def __init__(self, parent=None):
        super(GLWidget, self).__init__(parent)

        self.object = 0
        self.xRot = 0
        self.yRot = 0
        self.zRot = 0
        
        self.a = [0,0,0]
        self.b = [1,0,0]
        self.c = [0.5, 0, 0.8660254037844386]
        self.d = [0.5, 0.8164965809277259, 0.29]

        self.lastPos = QPoint()

        self.trolltechGreen = QColor.fromCmykF(0.40, 0.0, 1.0, 0.0)
        self.trolltechPurple = QColor.fromCmykF(0.39, 0.39, 0.0, 0.0)

    def minimumSizeHint(self):
        return QSize(50, 50)

    def sizeHint(self):
        return QSize(400, 400)

    def setXRotation(self, angle):
        angle = self.normalizeAngle(angle)
        if angle != self.xRot:
            self.xRot = angle
            self.xRotationChanged.emit(angle)
            self.update()

    def setYRotation(self, angle):
        angle = self.normalizeAngle(angle)
        if angle != self.yRot:
            self.yRot = angle
            self.yRotationChanged.emit(angle)
            self.update()

    def setZRotation(self, angle):
        angle = self.normalizeAngle(angle)
        if angle != self.zRot:
            self.zRot = angle
            self.zRotationChanged.emit(angle)
            self.update()

    def initializeGL(self):
        self.setClearColor(self.trolltechPurple.darker())
        self.object = self.makeObject()
        glShadeModel(GL_FLAT)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_CULL_FACE)

    def paintGL(self):
        glClear(
                GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        glTranslated(0.0, 0.0, -10.0)
        glRotated(self.xRot / 16.0, 1.0, 0.0, 0.0)
        glRotated(self.yRot / 16.0, 0.0, 1.0, 0.0)
        glRotated(self.zRot / 16.0, 0.0, 0.0, 1.0)
        glCallList(self.object)

    def resizeGL(self, width, height):
        side = min(width, height)
        if side < 0:
            return

        glViewport((width - side) // 2, (height - side) // 2, side,
                side)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(-0.5, +0.5, +0.5, -0.5, 4.0, 15.0)
        glMatrixMode(GL_MODELVIEW)

    def mousePressEvent(self, event):
        self.lastPos = event.pos()

    def mouseMoveEvent(self, event):
        dx = event.x() - self.lastPos.x()
        dy = event.y() - self.lastPos.y()

        if event.buttons() & Qt.LeftButton:
            self.setXRotation(self.xRot + 8 * dy)
            self.setYRotation(self.yRot + 8 * dx)
        elif event.buttons() & Qt.RightButton:
            self.setXRotation(self.xRot + 8 * dy)
            self.setZRotation(self.zRot + 8 * dx)

        self.lastPos = event.pos()

    def makeObject(self):
        genList = glGenLists(1)
        glNewList(genList, GL_COMPILE)

       	glBegin(GL_TRIANGLES)
       	glVertex3f(self.a[0],self.a[1],self.a[2])
       	glVertex3f(self.c[0],self.c[1],self.c[2])
       	glVertex3f(self.d[0],self.d[1],self.d[2])
       	glEnd()
        #
       	glBegin(GL_TRIANGLES)
       	glVertex3f(self.a[0],self.a[1],self.a[2])
       	glVertex3f(self.b[0],self.b[1],self.b[2])
       	glVertex3f(self.d[0],self.d[1],self.d[2])
       	glEnd()
        #
       	glBegin(GL_TRIANGLES)
       	glVertex3f(self.a[0],self.a[1],self.a[2])
       	glVertex3f(self.c[0],self.c[1],self.c[2])
       	glVertex3f(self.b[0],self.b[1],self.b[2])
       	glEnd()
        #
       	glBegin(GL_TRIANGLES)
       	glVertex3f(self.c[0],self.c[1],self.c[2])
       	glVertex3f(self.b[0],self.b[1],self.b[2])
       	glVertex3f(self.d[0],self.d[1],self.d[2])
       	glEnd()
        # x1 = +0.06
        # y1 = -0.14
        # x2 = +0.14
        # y2 = -0.06
        # x3 = +0.08
        # y3 = +0.00
        # x4 = +0.30
        # y4 = +0.22

        # self.quad(x1, y1, x2, y2, y2, x2, y1, x1)
        # self.quad(x3, y3, x4, y4, y4, x4, y3, x3)

        # self.extrude(x1, y1, x2, y2)
        # self.extrude(x2, y2, y2, x2)
        # self.extrude(y2, x2, y1, x1)
        # self.extrude(y1, x1, x1, y1)
        # self.extrude(x3, y3, x4, y4)
        # self.extrude(x4, y4, y4, x4)
        # self.extrude(y4, x4, y3, x3)

        # NumSectors = 200

        # for i in range(NumSectors):
        #     angle1 = (i * 2 * math.pi) / NumSectors
        #     x5 = 0.30 * math.sin(angle1)
        #     y5 = 0.30 * math.cos(angle1)
        #     x6 = 0.20 * math.sin(angle1)
        #     y6 = 0.20 * math.cos(angle1)

        #     angle2 = ((i + 1) * 2 * math.pi) / NumSectors
        #     x7 = 0.20 * math.sin(angle2)
        #     y7 = 0.20 * math.cos(angle2)
        #     x8 = 0.30 * math.sin(angle2)
        #     y8 = 0.30 * math.cos(angle2)

        #     self.quad(x5, y5, x6, y6, x7, y7, x8, y8)

        #     self.extrude(x6, y6, x7, y7)
        #     self.extrude(x8, y8, x5, y5)

        # glEnd()
        glEndList()

        return genList

    def quad(self, x1, y1, x2, y2, x3, y3, x4, y4):
        self.setColor(self.trolltechGreen)

        glVertex3d(x1, y1, -0.05)
        glVertex3d(x2, y2, -0.05)
        glVertex3d(x3, y3, -0.05)
        glVertex3d(x4, y4, -0.05)

        glVertex3d(x4, y4, +0.05)
        glVertex3d(x3, y3, +0.05)
        glVertex3d(x2, y2, +0.05)
        glVertex3d(x1, y1, +0.05)

    def extrude(self, x1, y1, x2, y2):
        self.setColor(self.trolltechGreen.darker(250 + int(100 * x1)))

        glVertex3d(x1, y1, +0.05)
        glVertex3d(x2, y2, +0.05)
        glVertex3d(x2, y2, -0.05)
        glVertex3d(x1, y1, -0.05)

    def normalizeAngle(self, angle):
        while angle < 0:
            angle += 360 * 16
        while angle > 360 * 16:
            angle -= 360 * 16
        return angle

    def setClearColor(self, c):
        glClearColor(c.redF(), c.greenF(), c.blueF(), c.alphaF())

    def setColor(self, c):
        glColor4f(c.redF(), c.greenF(), c.blueF(), c.alphaF())



