from PyQt5 import QtWidgets


class MainWindow(QtWidgets.QWidget):

    def __init__(self, imap, autorization_window):
        super().__init__()
        self.Imap = imap
        self.Autoriztion_window = autorization_window
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Imap')
        self.setFixedSize(700, 500)

        grid = QtWidgets.QGridLayout()
        self.setLayout(grid)
        self.Grid = grid



        self.show()
