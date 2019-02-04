from Socket import Socket


class Imap:

    def __init__(self, host, port, login, password):
        self._Socket = Socket(host, port)
        self.Host = host
        self.Port = int(port)
        self.Login = login
        self.Password = password

    def login(self):
        result_str = 'LOGIN {0} {1}'.format(self.Login, self.Password)
        self._Socket.send_msg(result_str)

    def select_folder(self, folder_name):
        self._Socket.send_msg('SELECT {}'.format(folder_name))

    def delete_folder(self, folder_name):
        self._Socket.send_msg('DELETE {}'.format(folder_name))

    def rename_folder(self, old_name, new_name):
        self._Socket.send_msg('RENAME {0} {1}'.format(old_name, new_name))

    def set_active(self, folder_name):
        self._Socket.send_msg('SUBCRIBE {}'.format(folder_name))

    def set_inactive(self, folder_name):
        self._Socket.send_msg('UNSUBCRIBE {}'.format(folder_name))

    def check_folder(self):
        self._Socket.send_msg('CHECK')
        return self._Socket.get_answer()

    def search_msg(self, flags):
        self._Socket.send_msg('SEARCH {}'.format(flags))
        return self._Socket.get_answer()

    def choose_msg(self, id, flags):
        self._Socket.send_msg('FETCH {0} {1}'.format(id, flags))
        return self._Socket.get_answer()

    def close_folder(self):
        self._Socket.send_msg('CLOSE')

    def logout(self):
        self._Socket.send_msg('LOGOUT')
