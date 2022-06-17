import os
import ast
from pathlib import Path
from util.globals import *


def GetDbLogs(file):
    dir_files = dir.ANSIBLE + 'roles/scan_dblog_errors/files/'
    if not os.path.exists(dir_files+file):
        return 'NA', None, ()
    return __dbLog_list(dir_files+file)


def __dbLog_list(filename):
    line_list = []
    with open(filename) as file:
        while (l := file.readline().rstrip()):
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
                tupple_list.append(__getCommonLogMsg(line))
            else:
                tupple_list.append(__getGeneralLogMsg(line))
    return log_file, log_size, tupple_list


def __getCommonLogMsg(line):
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
    conn = "{'"+line.split(' ')[4].replace('=', "':'").replace(',', "','")+"'}"

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


def __getGeneralLogMsg(line):
    lineNum = int(line.split('	')[0].strip())
    line = line.split('	')[1]
    return (lineNum, None, None, None, None, None, None, line)


def __getSummaryDetailsDir():
    return dir.ANSIBLE + 'roles/scan_dblog_filter/files/'


def GetDbSummaryDetails(file):
    dir_files = __getSummaryDetailsDir()
    if not os.path.exists(dir_files+file):
        return 'NA', None, ()
    return __dbSummary_list(dir_files+file)


def __dbSummary_list(filename):
    line_list = []
    with open(filename) as file:
        while (l := file.readline().rstrip()):
            line_list.append(l)
    file_num = line_list[0].strip().split(';')[0]
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
                    date_time, db, user, app, client, msg = __get_pid_line(
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
    # print('    -->', file_num, date_time, db, user,
    #       app, client, err_list, '------------')
    # os._exit(0)
    return {
        "file_num": file_num,
        "date_time": date_time,
        "db": db,
        "user": user,
        "app": app,
        "client": client,
        "err_list": err_list
    }


def __get_pid_line(line):
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
    conn = "{'"+line.split(' ')[4].replace('=', "':'").replace(',', "','")+"'}"

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


def SetClearDbSummaryFiles():
    dir_files = __getSummaryDetailsDir()
    [f.unlink() for f in Path(dir_files).glob("*") if f.is_file()]
