import socket
import ssl


class Socket:

    def __init__(self, host, port):
        self.Sock = socket.socket()
        self.Sock = ssl.wrap_socket(self.Sock)
        self.Sock.connect((host, int(port)))
        self.Tag = b'A0'

    def send_msg(self, text):
        result_msg = self.Tag + ' {}\r\n'.format(text).encode()
        self.Sock.send(result_msg)
        self.generate_new_tag()

    def get_answer(self):
        answers = []
        is_break = False
        while True:
            if is_break:
                break
            if len(answers) > 0:
                try:
                    temp = answers[-1].decode()
                except UnicodeDecodeError:
                    pass
                if temp[-11:] == '(Success)\r\n' or temp[-9:] == 'Success\r\n' or 'ready' in temp:
                    is_break = True
                    break
                else:
                    answers.append(self.Sock.recv(1024))
            else:
                answers.append(self.Sock.recv(1024))
        # try:
        #     self.Sock.settimeout(1)
        #     while True:
        #         answers.append(self.Sock.recv(1024))
        # except Exception:
        result = b''.join(answers)
        return result

    def generate_new_tag(self):
        decoded_str = self.Tag.decode()
        number_of_request = int(decoded_str[-1])
        self.Tag = ('A' + str(number_of_request + 1)).encode()
