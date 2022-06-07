import os
import ast


def getDbLogs(file, dir_ansible):
    dir = dir_ansible + 'roles/scan_dblog_errors/files/'
    if not os.path.exists(dir+file):
        return 'NA', None, ()
    return __dbLog2Tuple(dir+file)


def __dbLog2Tuple(filename):
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
    line = line.split('	')[1].replace(
        'PostgreSQL JDBC Driver', 'PostgreSQL_JDBC_Driver')
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
    # print('    -->', 'Client', client, '-->', line, '---------------------')
    return (lineNum, date_time, pid, db, user, app, client, line)


def __getGeneralLogMsg(line):
    lineNum = int(line.split('	')[0].strip())
    line = line.split('	')[1]
    return (lineNum, None, None, None, None, None, None, line)
