from os import listdir
from os.path import isfile, join
from csv import reader


def getDbParams(dir_ansible):
    print("  - DBs...")
    dir = dir_ansible + 'roles/scan_db/files/'
    files_list = [f for f in listdir(dir) if isfile(join(dir, f))]
    items = []
    for file in files_list:
        dictDbs = db2Tuple(dir+file)
        t = (file, dictDbs)
        items.append(t)
    return items


def db2Tuple(filename):
    with open(filename, 'r') as read_obj:
        # pass the file object to reader() to get the reader object
        csv_reader = reader(read_obj)
        # Pass reader object to list() to get a list of lists
        list_of_rows = list(csv_reader)
        ret_list = []
        for lin in list_of_rows:
            for item in lin:
                ret_list.append(tuple(item.split(";")))
        return ret_list
