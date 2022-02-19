from scripts.Gui import WelcomeScreen
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QDialog
from PyQt5 import QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt


if __name__ == '__main__':
    app = QApplication(sys.argv)
    welcome = WelcomeScreen()
    widget = QtWidgets.QStackedWidget()
    widget.setWindowIcon(QIcon('resources/icon/icon.png'))
    widget.addWidget(welcome)
    widget.setFixedHeight(605)
    widget.setFixedWidth(1024)

    title = "FBWhoozupBot Pro+"
    widget.setWindowTitle(title)

    widget.setWindowFlag(Qt.FramelessWindowHint)
    widget.show()
    try:
        sys.exit(app.exec_())
    except:
        print("Exiting")