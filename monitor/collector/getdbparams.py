import os


def getDbParams(file, dir_ansible):
    dir = dir_ansible + 'roles/scan_dbparams/files/'
    dictDbs = {}
    if os.path.exists(dir+file):
        dictDbs = dbParam2Dict(dir+file)
    return dictDbs


def dbParam2Dict(filename):
    ret_list = {}
    with open(filename) as file:
        for line in file:
            ret_list[line.replace("\n", "").split(
                ";")[0]] = line.replace("\n", "").split(";")[1]
    return ret_list
