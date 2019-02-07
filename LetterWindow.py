from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon


class LetterWindow(QtWidgets.QWidget):

    def __init__(self, letter, letter_widget):
        super().__init__()
        self.Letter = letter
        self.Letter_widget = letter_widget
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Imap')
        self.setFixedSize(700, 500)
        self.setWindowIcon(QIcon('Icon.jpg'))
        grid = QtWidgets.QGridLayout()
        self.setLayout(grid)
        self.Grid = grid

        from_label = QtWidgets.QLabel('From')
        grid.addWidget(from_label, 0, 0)

        from_result = QtWidgets.QLabel('-')
        grid.addWidget(from_result, 0, 1)

        subject_label = QtWidgets.QLabel('Subject')
        grid.addWidget(subject_label, 1, 0)

        subject_result = QtWidgets.QLabel(self.Letter.Header)
        grid.addWidget(subject_result, 1, 1)

        body_label = QtWidgets.QLabel('Body')
        grid.addWidget(body_label, 2, 0, 3, 1)

        body_result = QtWidgets.QLabel('-')
        grid.addWidget(body_result, 2, 1, 3, 1)

        download_button = QtWidgets.QPushButton('Download')
        grid.addWidget(download_button, 5, 0, 1, 2)

        self.show()

    def closeEvent(self, QCloseEvent):
        self.Letter_widget.List_of_letters_widget.Main_window.show()
