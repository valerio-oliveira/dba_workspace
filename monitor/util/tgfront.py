from util.globals import emoji
from util.pdf_log_erros import reports
import telebot


class tglabel:
    LabelHeader = emoji.DIZZY + " *DBA BOT - Serviço de Monitoramento de Bancos de Dados*" + \
        "\nVersão 0.1\n"
    LabelMainMenu = emoji.DIZZY + ' Menu Principal'
    LabelErrorLog = emoji.TRAY + ' Logs de Erros'
    LabelLogButton = 'º Mais Recente'
    LabelDirectMessage = 'Menssagem direta'
    LabelNewCollect = emoji.RELOAD + ' Nova Coleta'
    LabelViewLogs = emoji.NOTEBOOK + ' Visualizar Logs'
    LabelAll = emoji.SUN + ' Todos'


class tgbutton:
    def BtnMainMenu():
        return telebot.types.InlineKeyboardButton(
            tglabel.LabelMainMenu, callback_data="cb_help")

    def BtnErrorLog():
        return telebot.types.InlineKeyboardButton(
            tglabel.LabelErrorLog, callback_data="cb_menu_log")

    def BtnDirectMessage():
        return telebot.types.InlineKeyboardButton(
            tglabel.LabelDirectMessage, url='telegram.me/valerio_oliveira')

    def BtnNewCollect():
        return telebot.types.InlineKeyboardButton(
            tglabel.LabelNewCollect, callback_data="cb_collect_log")

    def BtnCollectButtons(num: int):
        keyboard = []
        buttons = []
        i = 1
        while i <= num:
            buttons.append(telebot.types.InlineKeyboardButton(
                str(i)+tglabel.LabelLogButton, callback_data="cb_log_collect_"+str(i))
            )
            if (i % 2) == 0:
                keyboard.append(buttons)
                buttons = []
            i += 1
        if (num % 2) == 1:
            keyboard.append(buttons)
        return telebot.types.InlineKeyboardMarkup(keyboard)

    def BtnViewLogs():
        return telebot.types.InlineKeyboardButton(
            tglabel.LabelViewLogs, callback_data="cb_menu_view_logs")

    def BtnLogsButtons(hosts_summary):
        # hosts_summary.append([hostname, address, log_file, log_size, log_dir, log_line])
        keyboard = []
        buttons = []
        i = 0
        for host in hosts_summary:
            # print(host)
            hostname = host[0]
            buttons.append(telebot.types.InlineKeyboardButton(
                hostname, callback_data="cb_summary_"+hostname)
            )
            if (i % 2) == 1:
                keyboard.append(buttons)
                buttons = []
            i += 1
        # if (len(hosts_summary) % 2) == 1:
        #     keyboard.append(buttons)
        buttons.append(telebot.types.InlineKeyboardButton(
            tglabel.LabelAll, callback_data="cb_summary_allhosts")
        )
        keyboard.append(buttons)
        return telebot.types.InlineKeyboardMarkup(keyboard)


class tgmenu:
    def MenuMainMenu():
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(
            tgbutton.BtnErrorLog()
        )
        markup.add(
            tgbutton.BtnDirectMessage(),
            tgbutton.BtnMainMenu()
        )
        # markup.row_width = 2
        # markup.add(telebot.types.InlineKeyboardButton("Yes", callback_data="cb_yes"),
        #            telebot.types.InlineKeyboardButton("No", callback_data="cb_no"))
        text = tglabel.LabelHeader
        text = text.replace('_', '\\_')
        return text, markup

    def MenuLog():
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(
            tgbutton.BtnNewCollect(),
            tgbutton.BtnViewLogs(),
        )
        markup.add(
            tgbutton.BtnMainMenu()
        )
        text = tglabel.LabelErrorLog
        text = text.replace('_', '\\_')
        return text, markup

    def MenuCollect():
        markup = tgbutton.BtnCollectButtons(6)
        markup.add(
            tgbutton.BtnErrorLog(),
            tgbutton.BtnMainMenu(),
        )
        text = tglabel.LabelNewCollect
        text = text.replace('_', '\\_')
        return text, markup

    def MenuViewLogs(hosts_summary):
        markup = tgbutton.BtnLogsButtons(hosts_summary)
        markup.add(
            tgbutton.BtnErrorLog(),
            tgbutton.BtnMainMenu(),
        )
        text = tglabel.LabelNewCollect
        text = text.replace('_', '\\_')
        return text, markup
