from collector.collect import *
from collector.getfacts import *


class col:
    # --
    WHITE = '\033[97m'
    CYAN = '\033[96m'
    PURPLE = '\033[95m'
    BLUE = '\033[94m'
    YELLOW = '\033[93m'
    GREEN = '\033[92m'
    RED = '\033[91m'
    GRAY = '\033[90m'
    #-- BOLD
    BWHITE = '\033[1;97m'
    BCYAN = '\033[1;96m'
    BPURPLE = '\033[1;95m'
    BBLUE = '\033[1;94m'
    BYELLOW = '\033[1;93m'
    BGREEN = '\033[1;92m'
    BRED = '\033[1;91m'
    BGRAY = '\033[1;90m'
    #-- UNDERLINE
    UWHITE = '\033[4;97m'
    UCYAN = '\033[4;96m'
    UPURPLE = '\033[4;95m'
    UBLUE = '\033[4;94m'
    UYELLOW = '\033[4;93m'
    UGREEN = '\033[4;92m'
    URED = '\033[4;91m'
    UGRAY = '\033[4;90m'
    #-- ITALIC
    IWHITE = '\033[3;97m'
    ICYAN = '\033[3;96m'
    IPURPLE = '\033[3;95m'
    IBLUE = '\033[3;94m'
    IYELLOW = '\033[3;93m'
    IGREEN = '\033[3;92m'
    IRED = '\033[3;91m'
    IGRAY = '\033[3;90m'
    #-- DARK
    DWHITE = '\033[2;97m'
    DCYAN = '\033[2;96m'
    DPURPLE = '\033[2;95m'
    DBLUE = '\033[2;94m'
    DYELLOW = '\033[2;93m'
    DGREEN = '\033[2;92m'
    DRED = '\033[2;91m'
    DGRAY = '\033[2;90m'
    #-- ADDITIONAL
    B = '\033[1m'
    U = '\033[4m'
    I = '\033[3m'
    #-- END
    E = '\033[0m'


def showSummary():
    print('>> -------')
    host_count = 0
    for host_line in __getHostsSummary():
        hostname = f'{host_line[0]:8}'
        hostip = f'{host_line[1]:15}'
        loglen = f'{host_line[3]}'
        logfile = f'{host_line[2]}'
        # print()
        print(
            f'{col.BPURPLE}Host-{str(host_count)}{col.E} | {col.BPURPLE}{hostname}{col.E} | {col.YELLOW}{hostip}{col.E} | {col.BPURPLE}{loglen}{logfile}{col.E}')
        for log_line in host_line[4]:
            seq = f'{log_line[0]:3}'
            lin = f'{log_line[1]:8}'
            msg_cnt = f'{log_line[2]:>6}'
            msg = log_line[3]
            print(
                f'{col.IWHITE}{seq}{col.E} {lin} {col.CYAN}{msg_cnt}{col.E}', msg)
        host_count += 1
        print()
    print('------- <<')


def __getHostsSummary():
    summary_list = []
    for host in getFacts(dir_ansible):
        # host = getFacts(dir_ansible)[2]
        machine_id = host[0]
        hostname = host[1]
        address = host[2]
        log_file = host[3]
        log_size = host[4]
        facts = host[5]
        dbParams = host[6]
        dbLogs = host[7]
        dictLog, dictLogLast = __getDictLog(dbLogs)
        log_line = []
        count = 0
        for key, value in dictLog.items():
            count += 1
            log_last = dictLogLast[key]
            log_line.append((count, log_last, value, key))

        summary_list.append([hostname, address, log_file, log_size, log_line])

    return tuple(summary_list)


def __sort_dict_by_value(d, reverse=False):
    return dict(sorted(d.items(), key=lambda x: x[1], reverse=reverse))


def __getDictLog(dbLogs):
    dictLog = {}
    dictLogLast = {}
    for item in dbLogs:
        dictLog[item[7]] = dictLog.get(item[7], 0) + 1
        dictLogLast[item[7]] = item[0]
    dictLog = __sort_dict_by_value(dictLog, reverse=True)
    return dictLog, dictLogLast
