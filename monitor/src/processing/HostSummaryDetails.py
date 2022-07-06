import os
import ast
from pathlib import Path
from util.globals import *


class HostSummaryDetails:
    def __init__(self):
        self.dir = dir.ANSIBLE + 'roles/scan_dblog_filter/files/'

    def process(self, hosts_summary):
        self.summary_details = []
        files = self.__get_file_list(hosts_summary)
        for file_dict in files:
            self.summary_details.append(self.get_db_summary_details(file_dict))

    def __get_file_list(self, hosts_summary):
        files = []
        for host_line in hosts_summary:
            host_name = host_line[0].replace('-', '_')

            for log_line in host_line[5]:
                seq = str(log_line[0])
                files.append({'host_name': host_name, 'seq': seq})
        return files

    def clear_files(self):
        [f.unlink() for f in Path(self.dir).glob("*") if f.is_file()]

    def get_extra_vars(self, summary_host_line):
        host_name = summary_host_line[0].replace('-', '_')
        log_file = summary_host_line[2]
        list_lines = []
        for log in summary_host_line[5]:
            log_seq = str(log[0])
            log_line = str(log[3])
            list_lines.append({"seq": log_seq, "line": log_line})

        return {"host_name": host_name,
                "log_file": log_file, "list_lines": list_lines}

    def get_db_summary_details(self, file_dict):
        host_name = file_dict['host_name']
        error_seq = file_dict['seq']
        filename = f"fil5432_{host_name}_{error_seq}.txt"
        file = self.dir + filename
        if not os.path.exists(file):
            return {}

        line_list = []
        with open(file) as f:
            while (l := f.readline().rstrip()):
                line_list.append(l)
        # file_num = line_list[0].strip().split(';')[0]
        line_list = line_list[1:]
        pid = line_list[0][line_list[0].find('['):line_list[0].find(']')+1]

        err_list = []
        first_run = True
        pos_msg = 0
        date_time, db, user, app, client, msg = '', '', '', '', '', ''
        if line_list:
            for line in line_list:
                if line.find(pid) != -1:
                    if first_run:
                        date_time, db, user, app, client, msg = self.__get_pid_line(
                            line)
                        pos_msg = line.find(msg)
                    else:
                        msg = line[pos_msg:]
                    err_list.append(msg)
                elif line.find('[') != -1 and line.find('[') < line.find(']'):
                    break
                else:
                    err_list.append(line)
                first_run = False
        return {
            "host_name": host_name,
            "error_seq": error_seq,
            "date_time": date_time,
            "db": db,
            "user": user,
            "app": app,
            "client": client,
            "err_list": err_list
        }

    def __get_pid_line(self, line):
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
        # print('    -->', date_time, db, user, app, client,
        #       '-->', line, '---------------------')
        # os._exit(0)
        return date_time, db, user, app, client, line
