from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon
from ListOfLettersWidget import ListOfLettersWidget


class MainWindow(QtWidgets.QWidget):

    def __init__(self, imap, autorization_window):
        super().__init__()
        self.Imap = imap
        self.autorization_window = autorization_window
        self.initUI()

    def center(self):
        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def initUI(self):
        self.setWindowTitle('Imap')
        self.setWindowIcon(QIcon('Icon.jpg'))
        self.setFixedSize(700, 500)
        self.center()

        grid = QtWidgets.QGridLayout()
        self.setLayout(grid)
        self.Grid = grid

        folders_box = QtWidgets.QComboBox()
        self.Folders_box = folders_box
        if len(self.Imap.parse_list_of_folders()) != 0:
            folders_box.addItems(
                [item[0] for item in self.Imap.parse_list_of_folders()])
        folders_box.activated[str].connect(self.folder_changed)
        grid.addWidget(folders_box, 0, 0)

        move_button = QtWidgets.QPushButton('Move')
        grid.addWidget(move_button, 1, 0)

        remove_button = QtWidgets.QPushButton('Remove')
        grid.addWidget(remove_button, 2, 0)

        show_more_button = QtWidgets.QPushButton('Show more')
        self.show_more_button = show_more_button
        grid.addWidget(show_more_button, 5, 1, 1, 5)

        list_of_letters_widget = ListOfLettersWidget(self.Imap, self)
        self.list_of_letters = list_of_letters_widget

        scroll_area = QtWidgets.QScrollArea()
        self.Scroll_area = scroll_area
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(list_of_letters_widget)
        grid.addWidget(scroll_area, 0, 1, 5, 5)

        # self.show()

    def folder_changed(self, text):
        self.Scroll_area.setWidget(ListOfLettersWidget(self.Imap, self))
        self.update()
