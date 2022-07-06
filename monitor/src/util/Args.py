import argparse


parser = argparse.ArgumentParser()
parser.add_argument('--token', dest='token',
                    type=str, help='Telegram token')
parser.add_argument('--parse_mode', dest='parse_mode',
                    type=str, help='Telegram parse mode')

global args
args = parser.parse_args()
