from PyQt5.QtCore import QThread
from Letter import Letter


class DownloadThread(QThread):

    def __init__(self, imap, count):
        super().__init__()
        self.imap = imap
        self.count = count
        self.result = []

    def run(self):
        for i in range(min(10, self.count)):
            self.result.append(Letter(
                self.imap.choose_msg(self.count - i, 'body[]')))
