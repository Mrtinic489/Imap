import unittest
from Imap import Imap


class Test(unittest.TestCase):

    host = 'imap.gmail.com'
    port = '993'
    login = 'pythontestimap2019@gmail.com'
    password = 'testimap'
    imap = Imap(host, port, login, password)
    imap.login()

    def test_show_list_of_folders(self):
        result = self.imap.show_list_of_folders().decode()
        self.assertTrue('INBOX' in result)
        self.assertTrue('Important' in result)
        self.assertTrue('Sent' in result)
        self.assertFalse('BadFolderName' in result)

    def test_select_folder(self):
        result = self.imap.select_folder('INBOX').decode()
        self.assertTrue('OK' in result)
        self.assertTrue('INBOX selected' in result)

    def test_get_count_of_letters(self):
        self.imap.select_folder('INBOX')
        self.assertEqual(int(self.imap.get_count_of_letters()), 3)

    def test_status_of_folder(self):
        self.imap.select_folder('INBOX').decode()
        result = self.imap.status_of_folder('INBOX', 'MESSAGES').decode()
        self.assertTrue('STATUS "INBOX" (MESSAGES 3)' in result)

    def test_close_folder(self):
        self.imap.select_folder('INBOX').decode()
        self.imap.close_folder()
        result = self.imap.get_answer().decode()
        self.assertTrue('Returned to authenticated state' in result)

    def test_search_msg(self):
        self.imap.select_folder('INBOX').decode()
        result = self.imap.search_msg('all').decode()
        self.assertTrue('SEARCH completed' in result)

    def test_choose_msg(self):
        self.imap.select_folder('INBOX').decode()
        result = self.imap.choose_msg(1, 'body[]').decode()
        self.assertTrue('Delivered-To: pythontestimap2019@gmail.com' in result)
        self.assertTrue('Sun, 10 Mar 2019 07:09:50 -0700 (PDT)' in result)
        self.assertTrue('Content-Type: multipart/alternative' in result)


if __name__ == '__main__':
    unittest.main()
