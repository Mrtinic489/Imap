from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from LetterWindow import LetterWindow


class LetterWidget(QtWidgets.QWidget):

    def __init__(self, letter, list_of_letters_widget):
        super().__init__()
        self.Letter = letter
        self.List_of_letters_widget = list_of_letters_widget
        self.initUI()

    def initUI(self):
        grid = QtWidgets.QGridLayout()
        self.setLayout(grid)
        self.Grid = grid

        check_box = QtWidgets.QCheckBox()
        check_box.stateChanged.connect(self.add_to_marked_list)
        grid.addWidget(check_box, 0, 0)

        date_label = QtWidgets.QLabel(self.Letter.date)
        grid.addWidget(date_label, 0, 1)

        letter_button = QtWidgets.QPushButton(self.Letter.subject)
        letter_button.clicked.connect(self.letter_button_clicked)
        grid.addWidget(letter_button, 0, 2, 1, 2)

        self.show()

    def add_to_marked_list(self, state):
        if state == Qt.Checked:
            self.List_of_letters_widget.List_of_marked.append(self)
        else:
            self.List_of_letters_widget.List_of_marked.remove(self)

    def letter_button_clicked(self):
        self.Letter_window = LetterWindow(self.Letter, self)
        self.List_of_letters_widget.Main_window.hide()
