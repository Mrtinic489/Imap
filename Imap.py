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
        answer = self.get_answer().decode()
        if answer.__contains__('AUTHENTICATIONFAILED'):
            raise Exception

    def select_folder(self, folder_name):
        self._Socket.send_msg('SELECT {}'.format(folder_name))

    def delete_folder(self, folder_name):
        self._Socket.send_msg('DELETE {}'.format(folder_name))

    def rename_folder(self, old_name, new_name):
        self._Socket.send_msg('RENAME {0} {1}'.format(old_name, new_name))

    def show_list(self):
        self._Socket.send_msg('LIST "" *')
        return self.get_answer()

    def parse_list_of_folders(self):
        result = []
        bytestr = self.show_list().decode()
        splitted_str = bytestr.split('*')
        splitted_str.remove(splitted_str[0])
        print(splitted_str)
        for item in splitted_str:
            if item.__contains__('INBOX'):
                result.append(tuple(['Inbox', 'INBOX']))
                continue
            raw_name_of_folder = item[item.find('(') + 1:item.find(')')]
            raw_name_of_folder = raw_name_of_folder.replace('\\HasNoChildren', '')
            raw_name_of_folder = raw_name_of_folder.replace('\\HasChildren', '')
            raw_name_of_folder = raw_name_of_folder.replace('\\Noselect', '')
            name_of_folder = raw_name_of_folder[raw_name_of_folder.find('\\') + 1:]
            if name_of_folder == '' or name_of_folder == ' ':
                continue
            print(name_of_folder)
            id_of_folder = item[item.rfind('/') + 1:item.rfind('"')]
            result.append(tuple([name_of_folder, id_of_folder]))
        return result


    def set_active(self, folder_name):
        self._Socket.send_msg('SUBCRIBE {}'.format(folder_name))

    def set_inactive(self, folder_name):
        self._Socket.send_msg('UNSUBCRIBE {}'.format(folder_name))

    def check_folder(self):
        self._Socket.send_msg('CHECK')
        return self.get_answer()

    def status_of_folder(self, folder_name, flags):
        self._Socket.send_msg('STATUS {0} ({1})'.format(folder_name, flags))
        return self.get_answer()

    def search_msg(self, flags):
        self._Socket.send_msg('SEARCH {}'.format(flags))
        return self.get_answer()

    def choose_msg(self, id, flags):
        self._Socket.send_msg('FETCH {0} {1}'.format(id, flags))
        return self.get_answer()

    def close_folder(self):
        self._Socket.send_msg('CLOSE')

    def get_answer(self):
        return self._Socket.get_answer()

    def logout(self):
        self._Socket.send_msg('LOGOUT')
