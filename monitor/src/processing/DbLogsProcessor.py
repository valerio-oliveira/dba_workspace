import os
import ast
from util.globals import *


class DbLogsProcessor:
    def process(self, file_name):
        self.log_file = 'NA'
        self.log_size = None
        dir_files = dir.ANSIBLE + 'roles/scan_dblog_errors/files/'
        file = dir_files+file_name
        if os.path.exists(file):
            self.__process_log(file)
        else:
            self.logs = ()

    def __process_log(self, file):
        line_list = []
        with open(file) as f:
            while (l := f.readline().rstrip()):
                line_list.append(l)
        log_detail = line_list[0].strip().split(' ')
        log_file = log_detail[0]
        log_file = log_file[::-
                            1].split('/')[0][::-1] if log_file.find('/') != -1 else log_file
        log_size = log_detail[1]
        line_list = line_list[1:]
        tupple_list = []
        if line_list:
            for line in line_list:
                if line.find(',user=') != -1:
                    tupple_list.append(self.__common_msg(line))
                else:
                    tupple_list.append(self.__general_msg(line))
        self.log_file = log_file
        self.log_size = log_size
        self.logs = tupple_list

    def __common_msg(self, line):
        lineNum = int(line.split('	')[0].strip())
        line = line.split('	')[1]

        pos_app = line.find(',app=')+5
        pos_client = line.find(',client=')
        len_app = pos_client-1
        line = line[:pos_app] + \
            line[pos_app:len_app+1].replace(' ', '_') + \
            line[pos_client:]

        date = line.split(' ')[0]
        time = line.split(' ')[1]
        utc = line.split(' ')[2]
        if utc == 'UTC':
            utc = '+00:00'
        else:
            utc = utc+':00'
        date_time = date+' '+time+' '+utc
        pid = int(line.split(' ')[3][1:-2])
        conn = "{'"+line.split(' ')[4].replace('=',
                                               "':'").replace(',', "','")+"'}"

        dict_conn = ast.literal_eval(conn)
        db = ''
        user = ''
        app = ''
        client = ''
        for v in dict_conn.items():
            if v[0] == 'db':
                db = v[1]
            if v[0] == 'user':
                user = v[1]
            if v[0] == 'app':
                app = v[1]
            if v[0] == 'client':
                client = v[1]
        line = line.split(',client=')[1][len(client)+1:]
        # print('    -->', 'App', app, '-->', line, '---------------------')
        return (lineNum, date_time, pid, db, user, app, client, line)

    def __general_msg(self, line):
        lineNum = int(line.split('	')[0].strip())
        line = line.split('	')[1]
        return (lineNum, None, None, None, None, None, None, line)
