from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from MainWindow import MainWindow
from Imap import Imap


class AutorizationWindow(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def center(self):
        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def initUI(self):
        self.setWindowTitle('Imap')
        self.setWindowIcon(QIcon('Icon.jpg'))
        self.setFixedSize(500, 500)
        self.center()

        grid = QtWidgets.QGridLayout()
        self.setLayout(grid)
        self.Grid = grid

        host_label = QtWidgets.QLabel('Host')
        self.Grid.addWidget(host_label, 0, 0)

        host_line = QtWidgets.QLineEdit('imap.gmail.com')
        self.Host_line = host_line
        self.Grid.addWidget(host_line, 0, 1)

        port_label = QtWidgets.QLabel('Port')
        self.Grid.addWidget(port_label, 1, 0)

        port_line = QtWidgets.QLineEdit('993')
        self.Port_line = port_line
        self.Grid.addWidget(port_line, 1, 1)

        login_label = QtWidgets.QLabel('Login')
        self.Grid.addWidget(login_label, 2, 0)

        login_line = QtWidgets.QLineEdit('mrtinic489@gmail.com')
        self.Login_line = login_line
        self.Grid.addWidget(login_line, 2, 1)

        password_label = QtWidgets.QLabel('Password')
        self.Grid.addWidget(password_label, 3, 0)

        password_line = QtWidgets.QLineEdit('Fcbljhf23Akbynjdyf2323')
        self.Password_line = password_line
        self.Grid.addWidget(password_line, 3, 1)
        password_line.setEchoMode(2)

        login_button = QtWidgets.QPushButton('Login')
        self.Grid.addWidget(login_button, 4, 0, 1, 2)
        login_button.clicked.connect(self.login_button_clicked)

        self.show()

    def login_button_clicked(self):
        host = self.Host_line.text()
        port = self.Port_line.text()
        login = self.Login_line.text()
        password = self.Password_line.text()
        try:
            imap = Imap(host, port, login, password)
            imap.login()
            self.set_disabled(True)
            main_window = MainWindow(imap, self)
            self.Main_window = main_window
        except Exception as e:
            self.message_box = QtWidgets.QMessageBox()
            self.message_box.setText(str(e))
            self.message_box.show()

    def keyPressEvent(self, e):
        if e.key() in [Qt.Key_Enter, Qt.Key_Return]:
            self.login_button_clicked()

    def set_disabled(self, flag):
        for i in range(self.Grid.count()):
            self.Grid.itemAt(i).widget().setDisabled(flag)
