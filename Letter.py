import base64


class Letter:

    def __init__(self, raw_data):
        self.Raw_data = raw_data.decode()
        self.Id = self.parse_id()
        self.List_of_flags = self.parse_flags()
        self.Date = self.parse_date()
        self.Header = self.parse_header()

    def parse_header(self):
        start_index = self.Raw_data.find('ENVELOPE') + 10
        raw_header = self.Raw_data[start_index:self.Raw_data.find('(', start_index) - 2]
        raw_header = raw_header[raw_header.rfind('"') + 1:]
        if not raw_header.__contains__('=?'):
            return raw_header
        raw_encoding = raw_header[:raw_header.find('B') + 2]
        header = raw_header.replace(raw_encoding, '')
        encoding = raw_encoding[2:raw_encoding.find('?', 3)]
        return base64.b64decode(header.encode(encoding)).decode(encoding)

    def parse_body(self):
        pass

    def parse_id(self):
        return self.Raw_data.split(' ')[1]

    def parse_date(self):
        start_index = self.Raw_data.find('INTERNALDATE') + 14
        date = self.Raw_data[start_index:self.Raw_data.find('"', start_index + 1)]
        return date

    def parse_flags(self):
        start_index = self.Raw_data.find('FLAGS') + 7
        raw_flags = self.Raw_data[start_index:self.Raw_data.find(')', start_index)]
        list_of_flags = raw_flags.split('\\')
        list_of_flags.remove(list_of_flags[0])
        return list_of_flags
