from os import listdir
from os.path import isfile, join
from src.processing.DbLogsProcessor import DbLogsProcessor
from src.processing.DbParamsProcessor import DbParamsProcessor
from util.globals import *
import ast


class SoProcessor:
    def __init__(self):
        self.facts = []

    def process(self):  # getfacts
        self.facts = []
        dir_files = dir.ANSIBLE + 'roles/scan_os/files/'
        files_list = [f for f in listdir(
            dir_files) if isfile(join(dir_files, f))]
        log_file = ''
        log_size = ''
        for file in files_list:
            dict_facts = self.__2dict(dir_files+file)

            file_db_params = file.replace("hw_", "p5432_")
            db_params_processor = DbParamsProcessor()
            db_params_processor.process(file_db_params)
            dict_db_params = db_params_processor.db_params

            file_db_logs = file.replace("hw_", "log5432_")
            db_log_processor = DbLogsProcessor()
            db_log_processor.process(file_db_logs)
            log_file = db_log_processor.log_file
            log_size = db_log_processor.log_size
            dict_db_logs = db_log_processor.logs

            defaultIpV4 = ast.literal_eval(dict_facts['default_ipv4'])

            t = (dict_facts['machine_id'], dict_facts['hostname'],
                 defaultIpV4['address'], log_file, log_size, dict_facts, dict_db_params, dict_db_logs)
            self.facts.append(t)

    def __2dict(self, filename):
        myfile = open(filename, "r")
        myline = myfile.readline()
        facts = {}
        while myline:
            if (myline[0] != " " and
                myline.find(" = ") != -1 and
                myline.split(" = ")[0][0:3] != 'ssh' and
                myline.split(" = ")[1].strip() != 'NA'
                ):
                facts[myline.split(" = ")[0]] = myline.split(" = ")[
                    1].replace("\n", "").strip()
            myline = myfile.readline()
        myfile.close()
        return facts
