from src.ansible.AnsibleCollector import AnsibleCollector, CollectorType
from src.processing.HostSummary import HostSummary
from src.processing.HostSummaryDetails import HostSummaryDetails
from src.report.LogSummaryPdfReport import LogSummaryPdfReport
from src.report.LogSummaryDetailsPdfReport import LogSummaryDetailsPdfReport
from src.telegram.Bot import Bot
from src.telegram.TgLabel import TgLabel
import json
import telebot

user_list = ['valerio_oliveira', 'renatoss32', 'iagopasso', ]
user_id_list = [458353463, 143777026, 1344529758, ]

admin_list = ['valerio_oliveira', ]
admin_id_list = [458353463, ]


def verified(chat_id, chat) -> bool:
    user_name = chat.username
    user_id = chat.id
    v = user_id in user_id_list
    if v:
        print("Authorized user", user_name, user_id)
    else:
        Bot.send_message(chat_id, "Recurso indisponível")
        print("User unknown", user_name, user_id)
    return v


@Bot.bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    chat_id = message.chat.id
    if not verified(chat_id, message.chat):
        return
    Bot.show_mainmenu(message.chat.id)


@Bot.bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    chat_id = call.message.chat.id
    if not verified(chat_id, call.message.chat):
        return
    if call.data == "cb_help":
        Bot.show_mainmenu(chat_id)
    elif call.data == "cb_menu_log":
        Bot.show_menulog(chat_id)
    elif call.data == "cb_collect_log":
        Bot.show_menucollect(chat_id)
    elif type(call.data) == str and str(call.data).startswith("cb_log_collect_"):
        log_pos = int(str(call.data).split("_")[3])
        Bot.repply(
            call.message, f"Coletando {log_pos}º log mais recente.\nAguarde...")

        extra_vars = {"log_file_pos": log_pos}
        collector = AnsibleCollector(
            type=CollectorType.DB_LOG_ERRORS, extra_vars=extra_vars)
        collector.collect()

        hosts_summary = HostSummary()
        hosts_summary.process(get_log_list=True)
        summary = hosts_summary.get()

        host_summary_details = HostSummaryDetails()
        host_summary_details.clear_files()
        for host in summary:
            Bot.repply(
                call.message, f'Preparando {host[0]:>10} : {len(extra_vars["list_lines"])} linhas')
            extra_vars = host_summary_details.get_extra_vars(host)

            print('Preparing ', host[0], ':',
                  len(extra_vars["list_lines"]), 'lines')

            collector.set(type=CollectorType.DB_LOG_FILTER,
                          extra_vars=extra_vars)
            collector.collect()

        Bot.repply(call.message, "Coleta concluída!")
        Bot.show_menulog(chat_id)

# ansible-playbook -i /home/valerio/OneDrive/Projetos/dba_workspace/ansible/inventories -e '{
# "host_name" : "deb35",
# "log_file" : "postgresql-2022-06-14_000000.log",
# "list_lines" : [{ "seq" : "1", "line" : "1711852" },  { "seq" : "2", "line" : "1711848" },  { "seq" : "3", "line" : "1711844" },  { "seq" : "4", "line" : "1711841" },  { "seq" : "5", "line" : "1711836" },  { "seq" : "6", "line" : "1696927" },  { "seq" : "7", "line" : "1696925" },  { "seq" : "8", "line" : "643657" }, ]
# }' /home/valerio/OneDrive/Projetos/dba_workspace/ansible/playbook_log_filter.yaml

    elif call.data == "cb_menu_view_logs" or call.data == "cb_menu_log_details":
        hosts_summary = HostSummary()
        hosts_summary.process(get_log_list=False)
        summary = hosts_summary.get()

        if call.data == "cb_menu_view_logs":
            Bot.show_menuviewlogs(chat_id, summary)
        elif call.data == "cb_menu_log_details":
            Bot.show_menulogdetails(chat_id, summary)
    elif type(call.data) == str and str(call.data).startswith("cb_summary_"):
        txt = str(call.data).split("_")[2]
        Bot.repply(
            call.message, f"Coletando resumo de {txt}.\nAguarde...")
        if txt == TgLabel.LabelAll:
            txt = ''

        hosts_summary = HostSummary()
        hosts_summary.process(host_name=txt, get_log_list=True)
        summary = hosts_summary.get()

        print('Get Log Summary Report...')
        pdf_file = LogSummaryPdfReport.get_pdf(hosts_summary=summary, txt=txt)
        Bot.bot.send_document(chat_id, pdf_file)
    elif type(call.data) == str and str(call.data).startswith("cb_log_details_"):
        Bot.bot.answer_callback_query(call.id, "Falta implementar")
        txt = str(call.data).split("_")[3]
        Bot.repply(
            call.message, f"Coletando detalhes de {txt}.\nAguarde...")
        if txt == TgLabel.LabelAll:
            txt = ''

        hosts_summary = HostSummary()
        hosts_summary.process(host_name=txt, get_log_list=True)
        summary = hosts_summary.get()

        host_summary_details = HostSummaryDetails()
        host_summary_details.process(summary)
        summary_details = host_summary_details.summary_details

        # print('summary[0][5]', summary[0][5])
        # print('summary_details[0:1]', summary_details[0:1])
        print('Get Detailed Log Summary Report...')
        pdf_file = LogSummaryDetailsPdfReport.get(
            hosts_summary=summary,
            summary_details=summary_details,
            txt=txt)
        Bot.bot.send_document(chat_id, pdf_file)

    elif call.data == "cb_yes":
        Bot.bot.answer_callback_query(call.id, "Answer is Yes")
    elif call.data == "cb_no":
        Bot.send_message(chat_id, "This is a message")


@Bot.bot.message_handler(func=lambda message: True)
def echo_all(message):
    chat_id = message.chat.id
    if not verified(chat_id, message.chat):
        return
    # print('Echo', message.text[2:])
    Bot.repply(
        message=message, text=message.text)


Bot.bot.infinity_polling()
