from tasks.playbook import *
from util.globals import *


class collector:
    def RunCollector(runSO: bool = False, runDbParams: bool = False, runDbLogs: bool = False, setLogPos: int = 1):
        witem = 1
        pos = 0
        direction = 1
        if runSO:
            witem, pos, direction = RunPlaybookSo(
                witem=witem, pos=pos, direction=direction)
        if runDbParams:
            witem, pos, direction = RunPlaybookDbParams(
                witem=witem, pos=pos, direction=direction)
        if runDbLogs:
            witem, pos, direction = RunPlaybookDbLogs(
                witem=witem, pos=pos, direction=direction, log_file_pos=setLogPos)
        scr.CleanLine()

    def RunDetailCollector(hosts_summary):
        for host_line in hosts_summary:
            host_name = host_line[0]
            log_file = host_line[2]
            list_lines = ''
            for log_line in host_line[5]:
                if list_lines == '':
                    list_lines = '"list_lines" : [{ "seq" : "' + \
                        str(log_line[0]) + '", "line" : "' + \
                        str(log_line[3]) + '" }, '
                else:
                    list_lines += ' { "seq" : "' + \
                        str(log_line[0]) + '", "line" : "' + \
                        str(log_line[3]) + '" }, '
            list_lines = list_lines[:-2] + ', ]'
            collector.__collectFilter(
                host_name, log_file, list_lines)

    def __collectFilter(host_name: str = '', log_file: str = '', list_lines: str = ''):
        witem = 1
        pos = 0
        direction = 1
        witem, pos, direction = RunPlaybookDbLogFilter(
            witem=witem,
            pos=pos,
            direction=direction,
            host_name=host_name.replace('-', '_'),
            log_file=log_file,
            list_lines=list_lines
        )
        scr.CleanLine()
