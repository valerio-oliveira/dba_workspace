import os
from task.getdbs import getDbParams
from task.playbook import runPlaybook
from task.getfacts import getFactParams

dir_workspace = os.path.dirname(os.path.realpath(__file__)) + '/..'
dir_ansible = dir_workspace + '/ansible/'

facts = []
dbs = []


def doCollect():
    print("Collecting data...")
    runPlaybook(dir_ansible)
    return getFactParams(dir_ansible), getDbParams(dir_ansible)


hosts, dbs = doCollect()

# for host in hosts:
#     print(host)

# for db in dbs:
print(dbs[0])
