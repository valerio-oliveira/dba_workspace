from util.bot_globals import bot
import subprocess
# import datetime
# from ansible_playbook_runner import Runner
from util.globals import *


def RunPlaybookSo(witem: int = 0, pos: int = 0, direction: int = 1, msg_bot=None):
    # Runner([dir_ansible], dir_ansible + 'playbook_so.yaml').run()
    message = 'Reading SO...  '
    if msg_bot:
        bot.repply(msg_bot, message)

    command = f'ansible-playbook -i {dir.ANSIBLE}inventories {dir.ANSIBLE}playbook_so.yaml'
    witem, pos, direction = __runCommand(
        command, witem, pos, message, direction, msg_bot)
    return witem, pos, direction


def RunPlaybookDbParams(witem: int = 0, pos: int = 0, direction: int = 1, msg_bot=None):
    # Runner([dir_ansible], dir_ansible + 'playbook_params.yaml').run()
    message = 'Reading Params...'
    if msg_bot:
        bot.repply(msg_bot, message)

    command = f'ansible-playbook -i {dir.ANSIBLE}inventories {dir.ANSIBLE}playbook_params.yaml'
    witem, pos, direction = __runCommand(
        command, witem, pos, message, direction, msg_bot)
    return witem, pos, direction


def RunPlaybookDbLogs(witem: int = 0, pos: int = 0, direction: int = 1, log_file_pos=1, msg_bot=None):
    message = 'Reading Logs...'
    if msg_bot:
        bot.repply(msg_bot, message)

    command = f'ansible-playbook -i {dir.ANSIBLE}inventories -e "log_file_pos={log_file_pos}" {dir.ANSIBLE}playbook_log_errors.yaml'
    # if msg_bot:
    #     bot.bot.reply_to(msg_bot, command)

    witem, pos, direction = __runCommand(
        command, witem, pos, message, direction, msg_bot)
    return witem, pos, direction


def RunPlaybookDbLogFilter(witem: int = 0, pos: int = 0, direction: int = 1, host_name: str = '', log_file: str = '', list_lines: str = '', msg_bot=None):
    message = f'Filtering [{host_name}] ...'
    if msg_bot:
        bot.repply(msg_bot, message)

    printEnd = '\r'
    command = 'ansible-playbook -i ' + dir.ANSIBLE + 'inventories ' + \
        '-e \'{' + \
        '"host_name" : "' + host_name + '", ' + \
        '"log_file" : "'+log_file + '", ' + \
        list_lines + '}\' ' + dir.ANSIBLE + 'playbook_log_filter.yaml'
    if msg_bot:
        bot.repply(msg_bot, command)

    if not msg_bot:
        print(message, printEnd)
    # print('Start ', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    if process.poll() is None:
        output = process.communicate()[0].decode("utf-8")
    return witem, pos, direction


def __runCommand(command: str = '', witem: int = 0, pos: int = 0, message: str = 'Wait...', direction: int = 1, msg_bot=None):
    # process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    with subprocess.Popen(command, shell=True, stdout=subprocess.PIPE) as process:
        while process.poll() is None:
            witem, pos, direction = Processing(
                witem, pos, message, direction, msg_bot)
    return witem, pos, direction
