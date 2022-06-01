from os import listdir
from os.path import isfile, join


def getFactParams(dir_ansible):
    print("  - Facts...")
    dir = dir_ansible + 'roles/scan_os/files/'
    files_list = [f for f in listdir(dir) if isfile(join(dir, f))]
    items = []
    for file in files_list:
        dictFacts = facts2Dict(dir+file)
        t = (file, dictFacts)
        items.append(t)
    return items


def facts2Dict(filename):
    myfile = open(filename, "r")
    myline = myfile.readline()
    facts = {}
    while myline:
        if (myline[0] != " " and
                myline.split(" = ")[0][0:3] != 'ssh' and
                " = " in myline and
                myline.split(" = ")[1][0] not in ['{', '['] and
                myline.split(" = ")[1].strip() != 'NA'
            ):
            facts[myline.split(" = ")[0]] = myline.split(" = ")[
                1].replace("\n", "").strip()
        myline = myfile.readline()
    myfile.close()
    return facts
