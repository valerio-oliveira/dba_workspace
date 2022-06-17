import datetime
import os
from time import sleep


class dir:
    UTIL = os.path.dirname(__file__) + '/'
    WORKSPACE = os.path.abspath(UTIL + '/../..') + '/'
    ANSIBLE = WORKSPACE + 'ansible/'


class scr:
    HEADER = 'DBA Monitor for PostgreSQL v1.0'
    BAR_WIDTH = 120

    def PrintSeparator():
        print(f'{col.BPURPLE}{"-"*scr.BAR_WIDTH}{col.E}')

    def PrintHeader():
        scr.PrintSeparator()

    def PrintFooter():
        print(f'{col.BPURPLE}{scr.HEADER:^{scr.BAR_WIDTH}}{col.E}')
        print(f'{col.BPURPLE}{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"):^{scr.BAR_WIDTH}}{col.E}')
        print(f'{col.BPURPLE}{"-"*scr.BAR_WIDTH}{col.E}')

    def CleanLine():
        print(f'\r{" ":>{scr.BAR_WIDTH}} ', end='\r')

    def DisableCursor():
        print('\033[?25l', end="")

    # def EnableCursor():
    #     print('\033[?25h', end="")


class col:
    # --
    WHITE = '\033[97m'
    CYAN = '\033[96m'
    PURPLE = '\033[95m'
    BLUE = '\033[94m'
    YELLOW = '\033[93m'
    GREEN = '\033[92m'
    RED = '\033[91m'
    GRAY = '\033[90m'
    #-- BOLD
    BWHITE = '\033[1;97m'
    BCYAN = '\033[1;96m'
    BPURPLE = '\033[1;95m'
    BBLUE = '\033[1;94m'
    BYELLOW = '\033[1;93m'
    BGREEN = '\033[1;92m'
    BRED = '\033[1;91m'
    BGRAY = '\033[1;90m'
    #-- UNDERLINE
    UWHITE = '\033[4;97m'
    UCYAN = '\033[4;96m'
    UPURPLE = '\033[4;95m'
    UBLUE = '\033[4;94m'
    UYELLOW = '\033[4;93m'
    UGREEN = '\033[4;92m'
    URED = '\033[4;91m'
    UGRAY = '\033[4;90m'
    #-- ITALIC
    IWHITE = '\033[3;97m'
    ICYAN = '\033[3;96m'
    IPURPLE = '\033[3;95m'
    IBLUE = '\033[3;94m'
    IYELLOW = '\033[3;93m'
    IGREEN = '\033[3;92m'
    IRED = '\033[3;91m'
    IGRAY = '\033[3;90m'
    #-- DARK
    DWHITE = '\033[2;37m'
    DCYAN = '\033[2;36m'
    DPURPLE = '\033[2;35m'
    DBLUE = '\033[2;34m'
    DYELLOW = '\033[2;33m'
    DGREEN = '\033[2;32m'
    DRED = '\033[2;31m'
    DGRAY = '\033[2;30m'
    # Background
    BGWHITE = '\033[47m'
    BGCYAN = '\033[46m'
    BGPURPLE = '\033[45m'
    BGBLUE = '\033[44m'
    BGYELLOW = '\033[43m'
    BGGREEN = '\033[42m'
    BGRED = '\033[41m'
    BGGRAY = '\033[40m'

    B = '\033[1m'
    U = '\033[4m'
    I = '\033[3m'
    D = '\033[2m'
    #-- END
    E = '\033[0m'


def Processing(witem, pos, message, direction, msg_bot):
    if msg_bot:
        return witem, pos, direction

    printEnd = '\r'
    limmit = scr.BAR_WIDTH-len(message)
    waiting = ['┗(◔◡◔)┓', '┏(◔◡◔)┓', '┏(◔◡◔)┛', '┗(◔◡◔)┛']
    sleep(.3)
    print(
        f'\r{message}{waiting[witem]:>{pos}} ', end=printEnd)
    witem = (witem + 1) % len(waiting)
    if direction == 1 and pos >= limmit:
        direction = -1
    elif direction == -1 and pos <= len(message)+1:
        direction = 1
    pos += direction
    return witem, pos, direction
