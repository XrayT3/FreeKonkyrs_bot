import const
import telebot


def admin(user_id):
    markup = telebot.types.ReplyKeyboardMarkup(True, False)
    if (user_id == const.admin_id) or (user_id == const.admin_id_1):
        markup.row("Админ-панель")
    return markup


def edit_texts():
    markup = telebot.types.InlineKeyboardMarkup()
    text1 = telebot.types.InlineKeyboardButton(text="Изменить основной текст", callback_data="text1_edit")
    text2 = telebot.types.InlineKeyboardButton(text="Изменить текст получения заявки", callback_data="text2_edit")
    counter = telebot.types.InlineKeyboardButton(text="Обнулить счетчик", callback_data="counter")
    markup.row(text1)
    markup.row(text2)
    markup.row(counter)
    return markup


def start():
    markup = telebot.types.ReplyKeyboardMarkup(True, False)
    markup.row("/start")
    return markup
