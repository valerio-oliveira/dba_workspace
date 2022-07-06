from src.telegram.TgLabel import TgLabel
import telebot


class TgButton:
    def BtnMainMenu():
        return telebot.types.InlineKeyboardButton(
            TgLabel.LabelMainMenu, callback_data="cb_help")

    def BtnErrorLog():
        return telebot.types.InlineKeyboardButton(
            TgLabel.LabelErrorLog, callback_data="cb_menu_log")

    def BtnDirectMessage():
        return telebot.types.InlineKeyboardButton(
            TgLabel.LabelDirectMessage, url='telegram.me/valerio_oliveira')

    def BtnNewCollect():
        return telebot.types.InlineKeyboardButton(
            TgLabel.LabelNewCollect, callback_data="cb_collect_log")

    def BtnCollectButtons(num: int):
        keyboard = []
        buttons = []
        i = 1
        while i <= num:
            buttons.append(telebot.types.InlineKeyboardButton(
                str(i)+TgLabel.LabelLogButton, callback_data="cb_log_collect_"+str(i))
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
            TgLabel.LabelViewLogs, callback_data="cb_menu_view_logs")

    def BtnLogDetails():
        return telebot.types.InlineKeyboardButton(
            TgLabel.LabelLogDetails, callback_data="cb_menu_log_details")

    def BtnLogsButtons(hosts_summary, callback_prefix):
        keyboard = []
        buttons = []
        i = 0
        for host in hosts_summary:
            # print(host)
            hostname = host[0]
            buttons.append(telebot.types.InlineKeyboardButton(
                hostname, callback_data=callback_prefix+hostname)
            )
            if (i % 2) == 1:
                keyboard.append(buttons)
                buttons = []
            i += 1
        callback_lbl = callback_prefix+TgLabel.LabelAll
        buttons.append(telebot.types.InlineKeyboardButton(
            TgLabel.LabelAll, callback_data=callback_lbl)
        )
        keyboard.append(buttons)
        return telebot.types.InlineKeyboardMarkup(keyboard)
