from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon
from ListOfLettersWidget import ListOfLettersWidget


class MainWindow(QtWidgets.QWidget):

    def __init__(self, imap, autorization_window):
        super().__init__()
        self.Imap = imap
        self.Autoriztion_window = autorization_window
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Imap')
        self.setWindowIcon(QIcon('Icon.jpg'))
        self.setFixedSize(700, 500)

        grid = QtWidgets.QGridLayout()
        self.setLayout(grid)
        self.Grid = grid

        folders_box = QtWidgets.QComboBox()
        self.Folders_box = folders_box
        folders_box.addItems([item[0] for item in self.Imap.parse_list_of_folders()])
        folders_box.activated[str].connect(self.folder_changed)
        grid.addWidget(folders_box, 0, 0)

        logout_button = QtWidgets.QPushButton('Logout')
        grid.addWidget(logout_button, 4, 0)
        logout_button.clicked.connect(self.logout_button_clicked)

        move_button = QtWidgets.QPushButton('Move')
        grid.addWidget(move_button, 1, 0)

        remove_button = QtWidgets.QPushButton('Remove')
        grid.addWidget(remove_button, 2, 0)

        list_of_letters_widget = ListOfLettersWidget(self.Imap, self)

        scroll_area = QtWidgets.QScrollArea()
        self.Scroll_area = scroll_area
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(list_of_letters_widget)
        grid.addWidget(scroll_area, 0, 1, 5, 5)

        self.show()

    def logout_button_clicked(self):
        self.Imap.logout()
        self.Autoriztion_window.show()
        self.hide()

    def folder_changed(self, text):
        self.Scroll_area.setWidget(ListOfLettersWidget(self.Imap, self))
        self.update()

