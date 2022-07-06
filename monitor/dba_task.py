import os
from src.ansible.AnsibleCollector import AnsibleCollector, CollectorType
from src.classes.MessageGroup import MessageGroup
from src.processing.HostSummaryDetails import HostSummaryDetails
from src.processing.HostSummary import HostSummary
from tasks.terminal import *
from util.globals import *
from util.playsound import *


def jobs_collect_report(link: str = ''):
    os.system('clear')
    scr.DisableCursor()
    scr.PrintHeader()

    collector = AnsibleCollector(type=CollectorType.SO)
    collector.collect()
    collector.set(type=CollectorType.DB_PARAMS)
    collector.collect()
    extra_vars = {"log_file_pos": 1}
    collector.set(type=CollectorType.DB_LOG_ERRORS,
                  extra_vars=extra_vars)
    collector.collect()
    del collector

    hosts_summary = HostSummary()
    hosts_summary.process()
    summary = hosts_summary.get()

    terminal.ShowSummary(summary)

    scr.PrintSeparator()

    # print('SetClearSummaryFiles')
    # summary.SetClearSummaryFiles()
    # print('RunDetailCollector')
    # collector.RunDetailCollector(
    #     hosts_summary=hosts_summary,
    # )

    # print('GetSummaryDetails')
    host_summary_details = HostSummaryDetails()
    host_summary_details.process(summary)
    summary_details = host_summary_details.summary_details

    # {
    #     "file_num": file_num,
    #     "date_time": date_time,
    #     "db": db,
    #     "user": user,
    #     "app": app,
    #     "client": client,
    #     "err_list": err_list
    # }
    scr.PrintFooter()
    snd.Beep()

    groups = MessageGroup.list
    # messages = {}
    for g in groups:
        if groups[g]['active']:
            for item in summary_details:
                if item['db'] in groups[g]['databases']:
                    print('---> ', g, item['file_num'],
                          item['db'], 'users', groups[g]['telegram'])

    # terminal.ShowSummaryDetails(summary_details)


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
