import sys

try:
    logfile = sys.argv[1]
    pid = '[' + sys.argv[2] + ']'
    lines = sys.argv[3:]
except IndexError:
    # raise SystemExit(
    print(
        f"PARAM ERROR: Usage {sys.argv[0]} <Fully identified log file> <pid> <log1> <log2> ...")

try:
    with open(logfile, 'r') as fp:
        for line in lines:
            # read line number 3 to 5
            # index starts from 0
            l0 = int(line) - 1
            l1 = l0 + 40
            x = fp.readlines()[l0:l1]
            print(x)
except IOError:
    print("ERROR: Log file does not exist")
except Exception as e:
    print(
        type(e).__name__,          # TypeError
        __file__,                  # /tmp/example.py
        e.__traceback__.tb_lineno  # 2
    )
