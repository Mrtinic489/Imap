from PyQt5 import QtWidgets
from LetterWidget import LetterWidget
from Letter import Letter
from DownloadThread import DownloadThread


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

    def show_more_clicked(self):
        index = self.Index_of_current_letter
        count = int(self.Imap.get_count_of_letters()) - index - 1
        if count <= 0:
            return
        self.trd = DownloadThread(self.Imap, count)
        self.trd.start()
        self.trd.finished.connect(self.finished)
        self.set_disabled(True)

    def filling_list_of_letters(self):
        try:
            name_of_folder = self.Main_window.Folders_box.currentText()
        except Exception:
            name_of_folder = 'INBOX'
        list_of_folders = self.Imap.parse_list_of_folders()
        if len(list_of_folders) == 0:
            self.Grid.addWidget(
                QtWidgets.QLabel('Problems with decode folders'), 0, 0)
        for item in list_of_folders:
            if item[0] == name_of_folder:
                self.Imap.select_folder(item[1])
                break
        try:
            count_of_letters = int(self.Imap.get_count_of_letters())
        except Exception:
            self.Imap.select_folder('INBOX')
            print('не упал')
            count_of_letters = int(self.Imap.get_count_of_letters())
            print('упал')
        if count_of_letters == 0:
            self.Grid.addWidget(QtWidgets.QLabel('No letters'), 0, 0)
        else:
            trd = DownloadThread(self.Imap, count_of_letters)
            self.trd = trd
            trd.start()
            trd.finished.connect(self.finished)
            self.set_disabled(True)

    def finished(self):
        result = self.trd.result.copy()
        self.set_disabled(False)
        for i in range(len(result)):
            self.Grid.addWidget(
                LetterWidget(result[i], self),
                i + self.Index_of_current_letter, 0)
        self.Index_of_current_letter += len(result)
        self.Main_window.autorization_window.hide()
        self.Main_window.show()

    def set_disabled(self, flag):
        for i in range(self.Grid.count()):
            self.Grid.itemAt(i).widget().setDisabled(flag)
        for i in range(self.Main_window.Grid.count()):
            self.Main_window.Grid.itemAt(i).widget().setDisabled(flag)
