import os
from util.globals import *


class DbParamsProcessor:
    def __init__(self):
        self.db_params = {}

    def process(self, file):
        dir_files = dir.ANSIBLE + 'roles/scan_dbparams/files/'
        full_path = dir_files + file
        self.db_params = {}
        if os.path.exists(full_path):
            with open(full_path) as file:
                for line in file:
                    self.db_params[line.replace("\n", "").split(
                        ";")[0]] = line.replace("\n", "").split(";")[1]
