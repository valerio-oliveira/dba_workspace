import os
from collector.playbook import runPlaybookDbLogs, runPlaybookSo, runPlaybookDbParams
from collector.getfacts import getFacts

global dir_workspace
dir_workspace = os.path.dirname(os.path.realpath(__file__)) + '/../..'
global dir_ansible
dir_ansible = dir_workspace + '/ansible/'


def runCollect(log_file_pos=1):
    runPlaybookSo(dir_ansible)
    runPlaybookDbParams(dir_ansible)
    runPlaybookDbLogs(dir_ansible, log_file_pos)


# def doCollectLines(start_line, end_line):
#     summary_list = []
#     for host in getFacts(dir_ansible):
#         dictLog = getDictLog(host)
#         log_line = []
#         count = 0
#         for key, value in dictLog.items():
#             count += 1
#             if count >= start_line and count <= end_line:
#                 log_line.append((count, value, key))
#         summary_list.append([host[1], host[2], host[3], log_line])
#     return tuple(summary_list)
