from tasks.summary import *
from tasks.collector import *
from tasks.getfacts import *
from util.globals import *
from util.bot_globals import bot


class terminal:
    def ShowSummary(hosts_summary: tuple):
        print('>> -------  DBA SCAN HOSTS SUMMARY -------')
        print()
        host_count = 0
        for host_line in hosts_summary:
            host_name = f'{host_line[0]:8}'
            host_ip = f'{host_line[1]:15}'
            log_size = f'{host_line[3]}'
            log_file = f'{host_line[2]}'
            log_dir = f'{host_line[4]}'
            print(
                f'{col.BPURPLE}Host-{str(host_count)}{col.E} | {col.BPURPLE}{host_name}{col.E} | {col.YELLOW}{host_ip}{col.E} | {col.BPURPLE}{log_size}     {log_dir}{log_file}{col.E}')

            print(
                f"{col.YELLOW}seq  {'line':8}  {'count':>5}  {'day/time':11}   {'pid':>6}  {'db':10}  {'user':22}  {'app':15}{col.E}")
            for log_line in host_line[5]:
                seq_num = f'{log_line[0]:3}'
                seq_target = f"python3 {dir.WORKSPACE}/monitor/dba_log_detail.py"
                seq = f"\u001b]8;;{seq_target}\u001b\\{seq_num}\u001b]8;;\u001b\\"
                msg = f'{log_line[1]}'
                count = f'{log_line[2]}'
                line = f'{log_line[3]}'
                date = f'{log_line[4]}'.replace(
                    '-', '') if log_line[4] else f"{'':20}"
                pid = f'{log_line[5]}'
                db = f'{log_line[6]}' if log_line[6] else f"{'':10}"
                user = f'{log_line[7]}' if log_line[7] else f"{'':20}"
                app = f'{log_line[8]}' if log_line[8] else f"{'':39}"
                ip = f'{log_line[9]}' if log_line[9] else f"{'':15}"

                # text = "This is a link"
                # target = "http://example.com"
                # print(f"\u001b]8;;{target}\u001b\\{text}\u001b]8;;\u001b\\")
                print(
                    f'{col.IWHITE}{seq}{col.E}  {col.GREEN}{line:8}  {col.CYAN}{count:>5}  {col.GREEN}{date[6:8]} {date[9:18]}  {col.CYAN}{pid:>6}  {col.GREEN}{db:10}  {col.CYAN}{user:22}  {col.GREEN}{app:15}{col.E} \n' +
                    f'    {col.WHITE}{msg}{col.E}', )
            host_count += 1
            print()
        print('<< ------- DBA SCAN HOSTS SUMMARY -------')

    def ShowBotSummary(hosts_summary: tuple, msg_bot, host):
        if not msg_bot:
            print("Bot not found")
            return

        host_count = 0
        for host_line in hosts_summary:
            host_name = f'{host_line[0]:8}'
            host_ip = f'{host_line[1]:15}'
            log_size = f'{host_line[3]}'
            log_file = f'{host_line[2]}'
            log_dir = f'{host_line[4]}'

            msg_ret = ''
            if host == '' or host == str(host_count):
                # @GM_DBA_bot  /summary_h{str(host_count)}    (tg://user?id=2084753743)
                msg_ret = f'/host{str(host_count)} | {host_name} | Log size: {log_size}\n'
                # bot.repply(msg_bot, msg_ret)
                msg_ret += f"`{'quant'}|{'db':10}|{'user':25}|app`\n"
                # msg_ret = ''
                line_count = 0
                for log_line in host_line[5]:
                    seq_num = f'{log_line[0]}'
                    # seq_target = f"python3 {dir.WORKSPACE}/monitor/dba_log_detail.py"
                    # seq = f"{seq_target}{seq_num}"
                    msg = f'  {log_line[1]}\n' if log_line[1] else ''
                    msg = msg.replace('_', '\\_')
                    count = f'{log_line[2]}'
                    # line = f'{log_line[3]}'
                    # date = f'{log_line[4]}'.replace(
                    #     '-', '') if log_line[4] else f"{'':20}"
                    # pid = f'{log_line[5]}'
                    db = f'{log_line[6]}' if log_line[6] else "(local)"
                    user = f'{log_line[7]}' if log_line[7] else ""
                    app = f'{log_line[8]}' if log_line[8] else ""
                    # ip = f'{log_line[9]}' if log_line[9] else f"{'':15}"

                    # text = "This is a link"
                    # target = "http://example.com"
                    # print(f"\u001b]8;;{target}\u001b\\{text}\u001b]8;;\u001b\\")

                    try:
                        msg_ret += f"`{count:5}|{db:10}|{user:25}|{app}`\n{msg}"
                        # bot.repply(msg_bot, msg_ret)
                    except Exception as e:
                        print('Inloop -->', e)
                        print(msg_ret)
                        continue
                    line_count += 1
                    if line_count > 25:
                        break

                msg_ret += '\n'

                try:
                    bot.repply(msg_bot, msg_ret)
                except Exception as e:
                    print(e)
                    print(msg_ret)
                    continue
            host_count += 1
