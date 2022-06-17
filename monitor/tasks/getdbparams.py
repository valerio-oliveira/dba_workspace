import os
from util.globals import *


def GetDbParams(file):
    dir_files = dir.ANSIBLE + 'roles/scan_dbparams/files/'
    dictDbs = {}
    if os.path.exists(dir_files+file):
        dictDbs = __dbParam2Dict(dir_files+file)
    return dictDbs


def __dbParam2Dict(filename):
    ret_list = {}
    with open(filename) as file:
        for line in file:
            ret_list[line.replace("\n", "").split(
                ";")[0]] = line.replace("\n", "").split(";")[1]
    return ret_list
