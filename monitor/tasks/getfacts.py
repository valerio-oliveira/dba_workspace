from os import listdir
from os.path import isfile, join
from tasks.getdblogs import *
from tasks.getdbparams import *
from util.globals import *
import ast


def GetFacts():
    dir_files = dir.ANSIBLE + 'roles/scan_os/files/'
    files_list = [f for f in listdir(dir_files) if isfile(join(dir_files, f))]
    items = []
    log_file = ''
    log_size = ''
    for file in files_list:
        dictFacts = __Facts2Dict(dir_files+file)
        dictDbParams = GetDbParams(file.replace("hw_", "p5432_"))
        log_file, log_size, dictDbLogs = GetDbLogs(
            file.replace("hw_", "log5432_"))
        defaultIpV4 = ast.literal_eval(dictFacts['default_ipv4'])
        t = (dictFacts['machine_id'], dictFacts['hostname'],
             defaultIpV4['address'], log_file, log_size, dictFacts, dictDbParams, dictDbLogs)
        items.append(t)
    return items


def __Facts2Dict(filename):
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
