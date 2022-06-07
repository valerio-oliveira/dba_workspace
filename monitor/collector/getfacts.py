from os import listdir
from os.path import isfile, join
from collector.getdblogs import getDbLogs
from collector.getdbparams import getDbParams
import ast


def getFacts(dir_ansible):
    dir = dir_ansible + 'roles/scan_os/files/'
    files_list = [f for f in listdir(dir) if isfile(join(dir, f))]
    items = []
    log_file = ''
    log_size = ''
    for file in files_list:
        dictFacts = __facts2Dict(dir+file)
        dictDbParams = getDbParams(file.replace("hw_", "p5432_"), dir_ansible)
        log_file, log_size, dictDbLogs = getDbLogs(
            file.replace("hw_", "log5432_"), dir_ansible)
        defaultIpV4 = ast.literal_eval(dictFacts['default_ipv4'])
        t = (dictFacts['machine_id'], dictFacts['hostname'],
             defaultIpV4['address'], log_file, log_size, dictFacts, dictDbParams, dictDbLogs)
        items.append(t)
    return items


def __facts2Dict(filename):
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
