from PyQt5 import QtWidgets
from LetterWidget import LetterWidget
from Letter import Letter


class ListOfLettersWidget(QtWidgets.QWidget):

    def __init__(self, imap, main_window):
        super().__init__()
        self.Imap = imap
        self.Main_window = main_window
        self.List_of_marked = []
        self.initUI()

    def initUI(self):
        grid = QtWidgets.QGridLayout()
        self.setLayout(grid)
        self.Grid = grid

        self.filling_list_of_letters()

        self.show()

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
                self.Grid.addWidget(LetterWidget(Letter(self.Imap.choose_msg(i + 1, 'full')), self))
