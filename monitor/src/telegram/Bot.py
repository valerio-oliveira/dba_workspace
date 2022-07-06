from src.telegram.TgMenu import *
from src.util.Args import *
from util.globals import *


class Bot:
    token = args.token
    mode = args.parse_mode
    bot = telebot.TeleBot(token, parse_mode=mode)

    def repply(message, text, replace_underscore=False):
        if replace_underscore:
            text = text.replace('_', '\\_')
        Bot.bot.reply_to(message, text)

    def send_message(chat_id, text, replace_underscore=True):
        if replace_underscore:
            text = text.replace('_', '\\_')
        Bot.bot.send_message(chat_id, text)

    def show_mainmenu(chat_id):
        text, markup = TgMenu.MenuMainMenu()
        Bot.bot.send_message(chat_id, text, reply_markup=markup)

    def show_menulog(chat_id):
        text, markup = TgMenu.MenuLog()
        Bot.bot.send_message(chat_id, text, reply_markup=markup)

    def show_menucollect(chat_id):
        text, markup = TgMenu.MenuCollect()
        Bot.bot.send_message(chat_id, text, reply_markup=markup)

    def show_menuviewlogs(chat_id, summary):
        text, markup = TgMenu.MenuViewLogs(summary)
        Bot.bot.send_message(chat_id, text, reply_markup=markup)

    def show_menulogdetails(chat_id, summary):
        text, markup = TgMenu.MenuLogDetails(summary)
        Bot.bot.send_message(chat_id, text, reply_markup=markup)
