from src.telegram.TgLabel import TgLabel
from src.telegram.TgButton import TgButton
import telebot


class TgMenu:
    def MenuMainMenu():
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(
            TgButton.BtnErrorLog()
        )
        markup.add(
            TgButton.BtnDirectMessage()
        )
        # markup.row_width = 2
        # markup.add(telebot.types.InlineKeyboardButton("Yes", callback_data="cb_yes"),
        #            telebot.types.InlineKeyboardButton("No", callback_data="cb_no"))
        text = TgLabel.LabelHeader
        text = text.replace('_', '\\_')
        return text, markup

    def MenuLog():
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(
            TgButton.BtnViewLogs(),
            TgButton.BtnLogDetails(),
        )
        markup.add(
            TgButton.BtnNewCollect(),
            TgButton.BtnMainMenu()
        )
        text = TgLabel.LabelErrorLog
        text = text.replace('_', '\\_')
        return text, markup

    def MenuCollect():
        markup = TgButton.BtnCollectButtons(6)
        markup.add(
            TgButton.BtnErrorLog(),
            TgButton.BtnMainMenu(),
        )
        text = TgLabel.LabelNewCollect
        text = text.replace('_', '\\_')
        return text, markup

    def MenuViewLogs(hosts_summary):
        markup = TgButton.BtnLogsButtons(hosts_summary, "cb_summary_")
        markup.add(
            TgButton.BtnErrorLog(),
            TgButton.BtnMainMenu(),
        )
        text = TgLabel.LabelViewLogs
        text = text.replace('_', '\\_')
        return text, markup

    def MenuLogDetails(hosts_summary):
        markup = TgButton.BtnLogsButtons(hosts_summary, "cb_log_details_")
        markup.add(
            TgButton.BtnErrorLog(),
            TgButton.BtnMainMenu(),
        )
        text = TgLabel.LabelLogDetails
        text = text.replace('_', '\\_')
        return text, markup
