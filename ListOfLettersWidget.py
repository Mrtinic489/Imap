from PyQt5 import QtWidgets
from LetterWidget import LetterWidget
from Letter import Letter


class ListOfLettersWidget(QtWidgets.QWidget):

    def __init__(self, imap, main_window):
        super().__init__()
        self.Imap = imap
        self.Main_window = main_window
        self.List_of_marked = []
        self.Index_of_current_letter = 0
        self.initUI()

    def initUI(self):
        grid = QtWidgets.QGridLayout()
        self.setLayout(grid)
        self.Grid = grid

        self.filling_list_of_letters()
        self.Main_window.show_more_button.clicked.connect(
            self.show_more_clicked)

        self.show()

    def show_more_clicked(self):
        index = self.Index_of_current_letter
        count = int(self.Imap.get_count_of_letters()) - index - 1
        if count <= 0:
            return
        for i in range(10 if count > 10 else count):
            self.Grid.addWidget(LetterWidget(
                Letter(self.Imap.choose_msg(
                    count - (i + index), 'body[]')), self),
                i + index, 0)
        self.Index_of_current_letter += 10 if count > 10 else count

    def filling_list_of_letters(self):
        name_of_folder = self.Main_window.Folders_box.currentText()
        list_of_folders = self.Imap.parse_list_of_folders()
        for item in list_of_folders:
            if item[0] == name_of_folder:
                self.Imap.select_folder(item[1])
                break
        count_of_letters = int(self.Imap.get_count_of_letters())
        if count_of_letters == 0:
            self.Grid.addWidget(QtWidgets.QLabel('No letters'), 0, 0)
        else:
            for i in range(10 if count_of_letters > 10 else count_of_letters):
                self.Grid.addWidget(LetterWidget(
                    Letter(self.Imap.choose_msg(
                        count_of_letters - i, 'body[]')), self), i, 0)
            self.Index_of_current_letter =\
                10 if count_of_letters > 10 else count_of_letters
