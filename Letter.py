import quopri
import base64
import locale


class Letter:

    def __init__(self, raw_data):
        self.raw_data = raw_data.decode()
        self.platform = locale.getdefaultlocale()
        self.str_data = raw_data.decode().split('\r\n')
        self.tags_and_values = self.parse_to_dict_of_tags_and_values()
        if self.tags_and_values is None:
            self.id = 0
            self.date = 'No date'
            self.from_info = 'No from info'
            self.subject = 'No subject'
            self.body = 'No body'
        self.id = self.parse_id()
        self.date = self.parse_date()
        self.from_info = self.parse_from_info()
        self.subject = self.parse_subject()
        self.body = self.parse_body()

    def parse_body(self):
        try:
            raw_html = \
                self.raw_data[self.raw_data.rfind('Content-Type: text/html'):]
        except Exception:
            return 'No body'
        return raw_html

    def parse_from_info(self):
        try:
            raw_from = self.tags_and_values['From'][0]
            if 'UTF-8' in raw_from or 'utf-8' in raw_from:
                raw_from = raw_from[10:2]
            return raw_from
        except Exception:
            return 'No from info'

    def parse_subject(self):
        try:
            list_of_subject = self.tags_and_values['Subject']
        except KeyError:
            return 'No subject'
        result_line = ''
        for raw_line in list_of_subject:
            line = raw_line
            codec = self.platform[-1]
            if 'UTF-8' in line or 'utf-8' in line:
                line = line[10:-2]
                codec = 'utf8'
            try:
                line = base64.decodebytes(line.encode())
            except Exception:
                pass
            try:
                line = quopri.decodestring(line.encode())
            except Exception:
                pass
            line = line.decode(codec)
            result_line += line
        return result_line

    def parse_date(self):
        try:
            return self.tags_and_values['Date'][0]
        except Exception:
            return 'No Date'

    def parse_id(self):
        fetch_str = ''
        try:
            for line in self.str_data:
                if 'FETCH' in line:
                    fetch_str = line
                    break
            return fetch_str.split(' ')[1]
        except Exception:
            return 0

    def parse_to_dict_of_tags_and_values(self):
        result_dict = dict()
        tag = ''
        try:
            for line in self.str_data:
                splitted_line = line.split(': ')
                if len(splitted_line) == 1 and tag == '':
                    continue
                if len(splitted_line) == 2:
                    tag = splitted_line[0]
                    result_dict[tag] = [splitted_line[1]]
                else:
                    result_dict[tag].append(line)
        except Exception:
            return None
        return result_dict

    def parse_attachemnts(self):
        splitted_data = self.raw_data.split('boundary')
        filename = ''
        for line in splitted_data:
            if 'filename' in line:
                codec = self.platform[-1]
                start_index = line.find('filename=') + 10
                filename = line[start_index:line.find('\n', start_index) - 2]
                if 'UTF-8' in filename or 'utf-8' in filename:
                    filename = filename[10:-2]
                try:
                    filename = base64.decodebytes(filename.encode())
                except Exception:
                    pass
                try:
                    filename = quopri.decodestring(filename.encode())
                except Exception:
                    pass
                filename = filename.decode(codec)
                index_of_attachment = line.rfind('Content-Transfer-Encoding:')
                index_of_new_line = line.find('\n', index_of_attachment) + 3
                raw_bytes = line[index_of_new_line:line.rfind('---') - 4]
                try:
                    raw_bytes = base64.decodebytes(raw_bytes.encode())
                except Exception:
                    pass
                try:
                    raw_bytes = quopri.decodestring(raw_bytes.encode())
                except Exception:
                    pass
                return filename, raw_bytes
