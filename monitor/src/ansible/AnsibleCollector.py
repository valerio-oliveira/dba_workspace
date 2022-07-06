import subprocess
from enum import Enum
from util.globals import *
import json


class CollectorType(Enum):
    SO = 1
    DB_PARAMS = 2
    DB_LOG_ERRORS = 3
    DB_LOG_FILTER = 4


class AnsibleCollector:
    def __init__(self, type: CollectorType, extra_vars: dict = {}):
        self.set(type, extra_vars)

    def set(self, type: CollectorType, extra_vars: dict = {}):
        self.type = type
        if type == CollectorType.SO:
            self.playbook_name = 'playbook_so'
        elif type == CollectorType.DB_PARAMS:
            self.playbook_name = 'playbook_params'
        elif type == CollectorType.DB_LOG_ERRORS:
            self.playbook_name = 'playbook_log_errors'
        elif type == CollectorType.DB_LOG_FILTER:
            self.playbook_name = 'playbook_log_filter'
        self.extra_vars = ''
        if bool(extra_vars):
            vars = json.dumps(extra_vars)  # , indent=1)
            self.extra_vars = f"--extra-vars '{vars}'"

    def collect(self):
        command = f'ansible-playbook -i {dir.ANSIBLE}inventories {self.extra_vars} {dir.ANSIBLE}{self.playbook_name}.yaml'
        print("Collecting", self.type.name)
        # print(command)
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        if process.poll() is None:
            self.output = process.communicate()[0].decode("utf-8")
