from Imap import Imap
import os


class Console:

    def __init__(self):
        self.Host = None
        self.Port = None
        self.Login = None
        self.Password = None
        self.Imap = None
        self.get_input()

    def get_input(self):
        print('Input host and port')
        self.Host = input()
        self.Port = input()
        os.system('cls')
        print('Input login and password')
        self.Login = input()
        self.Password = input()
        self.login()

    def login(self):
        os.system('cls')
        print('Wait...')
        self.Imap = Imap(self.Host, self.Port, self.Login, self.Password)
        answer = self.Imap.login().decode()
        if 'NO' in answer.split(' '):
            print('Incorrect data, try again')
            self.get_input()
        else:
            print('OK')


console = Console()
