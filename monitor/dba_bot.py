from tasks.summary import *
from tasks.collector import *
import telebot
from util.bot_globals import *
# import os
# import sys
# import pathlib


@bot.bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    welcome_message = "*DBA BOT - Database Monitoring Service*  (v0.1)\n" + \
        "By [Valerio Oliveira](tg://user?id=458353463) \n" + \
        "\n" + emoji.ENGINE + "*Available Administrative Tasks:*\n" + \
        "   /collect_log - Runs the log collector\n" + \
        "\n" + emoji.REPORT + "*Available Lists:*\n" + \
        "   /summary - Shows the last log full summary\n" + \
        "\n" + emoji.INFO + "*Additional Options:*\n" + \
        "   /help - Shows this options list"
    # "/getdbparams - Obter informações sobre os parâmetros do banco de dados\n"
#         "/getfacts - Obter informações sobre o hardware do servidor\n" + \
#         "/getdblogs - para obter informações sobre os logs do banco de dados\n" + \

    bot.repply(message, welcome_message, True)


@bot.bot.message_handler(commands=['collect_log'])
def runcollector(message):
    bot.repply(message, "Running the log collector...", True)
    collector.RunCollector(
        # runSO=True,
        # runDbParams=True,
        runDbLogs=True,
        setLogPos=1,
        msg_bot=message,
    )
    bot.send_message(message.chat.id, "Log collection finished!")


@bot.bot.message_handler(func=lambda msg: msg.text[:8] == '/summary')
def get_summary(message):
    host = f"{message.text[9:]}"
    # print("Summary for", host[4:])
    bot.repply(message, "Getting summary...")
    summary.getBotSummary(msg_bot=message, host=host[4:])
    bot.repply(message, "Summary finished!")


@bot.bot.message_handler(func=lambda msg: msg.text[:5] == '/host')
def get_host_options(message):
    host = message.text[1:]
    options_message = f"\n" + emoji.REPORT + "*Lists for [{host.capitalize()}]:*\n" + \
        f"/summary_{host} - Shows collection summary for current host\n" + \
        "\n" + emoji.INFO + "*Additional Options:*\n" + \
        "   /help - Shows the main menu list"
    bot.repply(message, options_message, True)


# @bot.message_handler(commands=['get_summary_details'])
# def get_summary_details(message):
#     bot.send_message(message.chat.id, str(GetSummaryDetails()))


@bot.bot.message_handler(func=lambda message: True)
def echo_all(message):
    # print('Echo', message.text[2:])
    bot.repply(
        message, 'Command unknown ['+message.text[1:]+']')


bot.bot.infinity_polling()
