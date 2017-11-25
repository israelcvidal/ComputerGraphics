import sys
sys.path.append("..")

from GUI.mainwindow import Window
from PyQt5.QtWidgets import QApplication
import numpy as np
from PyQt5.QtGui import QImage
from PyQt5.QtCore import Qt
from test import room_scenario

if __name__ == '__main__':
    width, height = 800, 500
    app = QApplication(sys.argv)
    window = Window(width, height)
    
    screen = 255*room_scenario.main()

    window.paint(screen.astype(np.uint8))
    window.show()
    sys.exit(app.exec_())