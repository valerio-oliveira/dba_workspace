from ansible_playbook_runner import Runner
# from collector.runner import Runner


def runPlaybookSo(dir_ansible):
    Runner([dir_ansible], dir_ansible + 'playbook_so.yaml').run()


def runPlaybookDbParams(dir_ansible):
    Runner([dir_ansible], dir_ansible + 'playbook_params.yaml').run()


def runPlaybookDbLogs(dir_ansible, log_file_pos=1):
    kwargs = {'extravars': {'log_file_pos': str(log_file_pos)}}
    Runner(inventory_files=[dir_ansible + 'inventories'], playbook_file=dir_ansible +
           '/playbook_log_errors.yaml', context_cli_args=kwargs).run()


# def __runCommand(command):
#     process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
#     for line in process.stdout:
#         print(line)
#     process.wait()
#     print('Playbook', process.returncode)
