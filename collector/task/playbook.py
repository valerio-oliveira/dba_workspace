from ansible_playbook_runner import Runner


def runPlaybook(dir_ansible):
    print("  - Playbook...")
    Runner(dir_ansible, dir_ansible + 'main.yaml').run()
