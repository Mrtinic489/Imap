import sys
from PyQt5 import QtWidgets
from AutorizationWindow import AutorizationWindow

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = AutorizationWindow()
    sys.exit(app.exec_())
