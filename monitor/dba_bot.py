from fileinput import filename
from tasks.summary import *
from tasks.collector import *
from util.bot_globals import *
import telebot

# import os
# import sys
# import pathlib


@bot.bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.show_mainmenu(message.chat.id)


@bot.bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    chat_id = call.message.chat.id
    if call.data == "cb_help":
        bot.show_mainmenu(chat_id)
    elif call.data == "cb_menu_log":
        bot.show_menulog(chat_id)
    elif call.data == "cb_collect_log":
        bot.show_menucollect(chat_id)
    elif type(call.data) == str and str(call.data).startswith("cb_log_collect_"):
        logPos = int(str(call.data).split("_")[3])
        bot.repply(
            call.message, f"Coletando {logPos}º log mais recente.\nAguarde...")
        collector.RunCollector(
            # runSO=True,
            # runDbParams=True,
            runDbLogs=True,
            setLogPos=logPos
        )
        bot.repply(call.message, "Coleta concluída!")
        bot.show_menulog(chat_id)
    elif call.data == "cb_menu_view_logs":
        hosts_summary = summary.GetHostsSummary(get_loglist=False)
        bot.show_menuviewlogs(chat_id, hosts_summary)
    elif type(call.data) == str and str(call.data).startswith("cb_summary_"):
        txt = str(call.data).split("_")[2]
        bot.repply(
            call.message, f"Coletando resumo de {txt}.\nAguarde...")
        if txt == tglabel.LabelAll:
            txt = ''
        hosts_summary = summary.GetHostsSummary(host_name=txt)
        pdf_file = reports.GetSummaryPdf(hosts_summary=hosts_summary, txt=txt)
        # doc = open('/tmp/file.txt', 'rb')
        bot.bot.send_document(chat_id, pdf_file)
        # hosts_summary = summary.GetHostsSummary(get_loglist=False)
        # bot.show_menuviewlogs(chat_id, hosts_summary)
    elif call.data == "cb_yes":
        bot.bot.answer_callback_query(call.id, "Answer is Yes")
    elif call.data == "cb_no":
        bot.send_message(chat_id, "This is a message")


@ bot.bot.message_handler(func=lambda message: True)
def echo_all(message):
    # print('Echo', message.text[2:])
    bot.repply(
        message=message, text=message.text)


@ bot.bot.message_handler(func=lambda msg: msg.text[:8] == '/summary')
def get_summary(message):
    host = f"{message.text[9:]}"
    # print("Summary for", host[4:])
    bot.repply(message=message, text="Getting summary...")
    summary.getBotSummary(msg_bot=message, host=host[4:])
    bot.repply(message=message, text="Summary finished!")


bot.bot.infinity_polling()
