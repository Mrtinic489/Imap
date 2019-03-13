from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon


class LetterWindow(QtWidgets.QWidget):

    def __init__(self, letter, letter_widget):
        super().__init__()
        self.Letter = letter
        self.Letter_widget = letter_widget
        self.initUI()

    def center(self):
        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def initUI(self):
        self.setWindowTitle('Imap')
        self.setFixedSize(700, 500)
        self.setWindowIcon(QIcon('Icon.jpg'))
        self.center()
        grid = QtWidgets.QGridLayout()
        self.setLayout(grid)
        self.Grid = grid

        from_label = QtWidgets.QLabel('From')
        grid.addWidget(from_label, 0, 0)

        from_result = QtWidgets.QLabel(self.Letter.from_info)
        grid.addWidget(from_result, 0, 1)

        subject_label = QtWidgets.QLabel('Subject')
        grid.addWidget(subject_label, 1, 0)

        subject_result = QtWidgets.QLabel(self.Letter.subject)
        grid.addWidget(subject_result, 1, 1)

        body_label = QtWidgets.QLabel('Body')
        grid.addWidget(body_label, 2, 0, 3, 1)

        body_result = QtWidgets.QLabel(self.Letter.body)
        scroll_area = QtWidgets.QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(body_result)
        grid.addWidget(scroll_area, 2, 1, 3, 1)

        download_button = QtWidgets.QPushButton('Download')
        download_button.clicked.connect(self.download_button_clicked)
        grid.addWidget(download_button, 5, 0, 1, 2)

        self.show()

    def download_button_clicked(self):
        result_of_parse = self.Letter.parse_attachemnts()
        if result_of_parse is not None:
            with open(result_of_parse[0], 'ab+') as f:
                f.write(result_of_parse[1])

    def closeEvent(self, QCloseEvent):
        self.Letter_widget.List_of_letters_widget.Main_window.show()
