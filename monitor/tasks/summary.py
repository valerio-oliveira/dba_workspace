from tasks.terminal import terminal
from tasks.collector import *
from tasks.getfacts import *
from util.globals import *


class summary:
    def __sort_by_index_value(d, reverse=False):
        return sorted(d.items(), key=lambda x: x[1], reverse=reverse)

    def __getDictLogSummary(dbLogs):
        dictLog = {}
        for item in dbLogs:
            last_line = item[0]
            last_date = item[1]
            last_pid = item[2]
            last_db = item[3]
            last_user = item[4]
            last_app = item[5]
            last_ip = item[6]
            last_msg = item[7]
            line_value = dictLog.get(last_msg, [])
            if line_value:
                count = int(line_value[0]) + 1
            else:
                count = 1

            dictLog[last_msg] = [count, last_line, last_date,
                                 last_pid, last_db, last_user, last_app, last_ip]
        dictLog = summary.__sort_by_index_value(dictLog, reverse=True)
        return dictLog

    def getBotSummary(msg_bot=None, host=''):
        hosts_summary = summary.GetHostsSummary()
        terminal.ShowBotSummary(hosts_summary, msg_bot=msg_bot, host=host)

    def GetHostsSummary():
        hosts_summary = []
        for host in GetFacts():
            machine_id = host[0]
            hostname = host[1]
            address = host[2]
            log_file = host[3]
            log_size = host[4].split('\t')[0]
            log_dir = host[4].split('\t')[1]
            facts = host[5]
            dbParams = host[6]
            dbLogs = host[7]
            listLogSummary = summary.__getDictLogSummary(dbLogs)
            log_line = []
            seq = 0
            for key, value in listLogSummary:
                seq += 1
                log_line.append(([seq, key, ]+value))

            hosts_summary.append(
                [hostname, address, log_file, log_size, log_dir, log_line])
        return tuple(hosts_summary)

    def GetSummaryDetails(hosts_summary) -> dict:
        summary_details = []
        files = summary.__getSummaryDetailsFileList(hosts_summary)
        for file in files:
            summary_details.append(GetDbSummaryDetails(file))

        # print('-->', summary_details)
        # os._exit(0)
        return summary_details

    def SetClearSummaryFiles():
        SetClearDbSummaryFiles()

    def __getSummaryDetailsFileList(hosts_summary):
        files = []
        for host_line in hosts_summary:
            host_name = host_line[0].replace('-', '_')

            for log_line in host_line[5]:
                seq = str(log_line[0])
                files.append(f'fil5432_{host_name}_{seq}.txt')
        return files
