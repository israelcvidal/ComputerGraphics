import sys
sys.path.append("..")

from opengl.GUI.mainwindow import Window
from PyQt5.QtWidgets import QApplication

if __name__ == '__main__':
    width, height = 800, 500
    app = QApplication(sys.argv)
    window = Window(width, height)

    window.show()
    sys.exit(app.exec_())