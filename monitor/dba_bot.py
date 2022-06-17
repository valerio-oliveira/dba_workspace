from tasks.summary import *
from tasks.collector import *
import telebot
from util.bot_globals import *
# import os
# import sys
# import pathlib


@bot.bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    welcome_message = "GB DBA BOT \n" + \
        "Boas Vindas! ao serviço de monitoramento!\n\n" + \
        "Escolha uma das opções: \n" + \
        "/collect_log - Executa o coletor de logs\n" + \
        "/summary - Exibe resumo geral das coletas\n" + \
        "/help - Exibe ajuda"
    # "/getdbparams - Obter informações sobre os parâmetros do banco de dados\n"
#         "/getfacts - Obter informações sobre o hardware do servidor\n" + \
#         "/getdblogs - para obter informações sobre os logs do banco de dados\n" + \

    bot.repply(message, welcome_message)


@bot.bot.message_handler(commands=['collect_log'])
def runcollector(message):
    bot.repply(message, "Starting to collect...")
    collector.RunCollector(
        # runSO=True,
        # runDbParams=True,
        runDbLogs=True,
        setLogPos=1,
        msg_bot=message,
    )
    bot.send_message(message.chat.id, "OK")


@bot.bot.message_handler(commands=['summary'])
def get_facts(message):
    bot.repply(message, "Getting summary...")
    summary.getBotSummary(msg_bot=message)


# @bot.message_handler(commands=['/get_summary_details'])
# def get_summary_details(message):
#     bot.send_message(message.chat.id, str(GetSummaryDetails()))


@bot.bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.repply(message, message.text)


bot.bot.infinity_polling()
