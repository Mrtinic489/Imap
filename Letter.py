import quopri
import base64


class Letter:

    def __init__(self, raw_data):
        self.raw_data = raw_data.decode()
        self.str_data = raw_data.decode().split('\r\n')
        self.tags_and_values = self.parse_to_dict_of_tags_and_values()
        self.id = self.parse_id()
        self.date = self.parse_date()
        self.from_info = self.parse_from_info()
        self.subject = self.parse_subject()
        self.body = self.parse_body()

    def parse_body(self):
        raw_html = \
            self.raw_data[self.raw_data.rfind('Content-Type: text/html'):]
        if raw_html is None:
            return 'Nothing'
        return raw_html

    def parse_from_info(self):
        try:
            raw_from = self.tags_and_values['From'][0]
            if raw_from.__contains__('UTF-8')\
                    or raw_from.__contains__('utf-8'):
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
            if line.__contains__('UTF-8') or line.__contains__('utf-8'):
                line = line[10:-2]
            try:
                line = base64.decodebytes(line.encode()).decode()
            except Exception:
                pass
            try:
                line = quopri.decodestring(line.encode()).decode()
            except Exception:
                pass
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
                if line.__contains__('FETCH'):
                    fetch_str = line
                    break
            return fetch_str.split(' ')[1]
        except Exception:
            return 0

    def parse_to_dict_of_tags_and_values(self):
        result_dict = dict()
        tag = ''
        for line in self.str_data:
            splitted_line = line.split(': ')
            if len(splitted_line) == 1 and tag == '':
                continue
            if len(splitted_line) == 2:
                tag = splitted_line[0]
                result_dict[tag] = [splitted_line[1]]
            else:
                result_dict[tag].append(line)
        return result_dict

    def parse_attachemnts(self):
        splitted_data = self.raw_data.split('boundary')
        filename = ''
        for line in splitted_data:
            if 'filename' in line:
                start_index = line.find('filename=') + 10
                filename = line[start_index:line.find('\n', start_index) - 2]
                if 'UTF-8' in filename or 'utf-8' in filename:
                    filename = filename[10:-2]
                try:
                    filename = base64.decodebytes(filename.encode()).decode()
                except Exception:
                    pass
                try:
                    filename = quopri.decodestring(filename.encode()).decode()
                except Exception:
                    pass
                index_of_attachment = line.rfind('Content-Transfer-Encoding:')
                index_of_new_line = line.find('\n', index_of_attachment) + 3
                raw_bytes = line[index_of_new_line:line.rfind('---') - 4]
                try:
                    raw_bytes = base64.decodebytes(raw_bytes.encode())
                except:
                    pass
                try:
                    raw_bytes = quopri.decodestring(raw_bytes.encode())
                except Exception:
                    pass
                return filename, raw_bytes
