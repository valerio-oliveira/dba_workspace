import os
# import threading
# import time
# import schedule
from tasks.collector import *
from tasks.summary import *
from tasks.terminal import *
from util.globals import *
from util.playsound import *
# from util.multithread import run_continuously

# os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'


def jobs_collect_report(link: str = ''):
    os.system('clear')
    scr.DisableCursor()
    scr.PrintHeader()

    collector.RunCollector(
        # runSO=True,
        # runDbParams=True,
        # runDbLogs=True,
        setLogPos=1,
    )
    hosts_summary = summary.GetHostsSummary()
    terminal.ShowSummary(hosts_summary)

    # scr.PrintSeparator()

    # summary.SetClearSummaryFiles()
    # collector.RunDetailCollector(
    #     hosts_summary=hosts_summary,
    # )

    # summary_details = summary.GetSummaryDetails(hosts_summary)

    # print(summary_details)
    # terminal.ShowSummaryDetails(summary_details)

    scr.PrintFooter()
    snd.Beep()


# def run_threaded(task):
#     job_thread = threading.Thread(target=task)
#     job_thread.start()


jobs_collect_report()

# run_threaded(jobs_collect_report)

# ----- scheduled task

# schedule.every(1).hours.do(run_threaded, jobs_collect_report)
# stop_collect = run_continuously()
# while True:
#     schedule.run_pending()
#     time.sleep(1)
# stop_collect.set()

# -----

# https://docs.ansible.com/ansible-core/2.12/user_guide/become.html#risks-of-becoming-an-unprivileged-user
