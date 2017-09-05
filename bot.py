import telebot
import logging
import const, markups, base


base.create_table()
bot = telebot.TeleBot(const.token)
uploaded_items = {}

logger = logging.getLogger('bot.py')
logger.setLevel(logging.DEBUG)
# create console handler and set level to debug
ch = logging.FileHandler('logs.log')
# create formatter
formatter = logging.Formatter('-----------------------------------------------------------\n'
                              '%(levelname)s %(asctime)s - %(name)s: %(message)s\n'
                              '%(funcName)s - %(lineno)d')
# add formatter to ch
ch.setFormatter(formatter)
# add ch to logger
logger.addHandler(ch)


@bot.message_handler(commands=["start"])
def start(message):
    sent = bot.send_message(message.chat.id, const.welcome_msg, reply_markup=markups.admin(message.chat.id))
    bot.register_next_step_handler(sent, reply_msg)


def reply_msg(message):
    if (message.text != "Админ-панель" and not base.is_in_base(message.chat.id)):
        request_num = base.add_user(message.chat.id)
        if (request_num != -1):
            bot.send_message(message.chat.id, const.reply_msg.format(id = request_num), reply_markup=markups.start())
            bot.send_message(const.admin_id, str(message.from_user.first_name) + " " + str(message.from_user.last_name) + "; @" + str(message.from_user.username) + "; " + str(request_num))
            bot.send_message(const.admin_id_1,
                             str(message.from_user.first_name) + " " + str(message.from_user.last_name) + "; @" + str(
                                 message.from_user.username) + "; " + str(request_num))
        else:
            bot.send_message(message.chat.id, "Сервис временно не доступен. Попробуйте позже")
            bot.send_message(const.admin_id, "Ошибка! Не могу выдать номер заявки")


@bot.message_handler(regexp="Админ-панель")
def admin(message):
    if (message.chat.id == const.admin_id) or (message.chat.id == const.admin_id_1):
        bot.send_message(message.chat.id, "Выберите текст", reply_markup=markups.edit_texts())


@bot.callback_query_handler(func=lambda call: call.data == "text1_edit")
def edit1(call):
    sent = bot.send_message(call.message.chat.id, "Введите новый текст")
    bot.register_next_step_handler(sent, confirm1)

def confirm1(message):
    base.drop_table()
    base.create_table()
    #const.counter = 80
    const.welcome_msg = message.text
    bot.send_message(message.chat.id, "Выберите текст", reply_markup=markups.edit_texts())


@bot.callback_query_handler(func=lambda call: call.data == "text2_edit")
def edit2(call):
    sent = bot.send_message(call.message.chat.id, "Введите текст")
    bot.register_next_step_handler(sent, confirm2)

def confirm2(message):
    base.drop_table()
    base.create_table()
    #const.counter = 80
    const.reply_msg = message.text
    bot.send_message(message.chat.id, "Текст успешно изменен!", reply_markup=markups.edit_texts())


@bot.callback_query_handler(func=lambda call: call.data == "counter")
def counter(call):
    const.counter = 80


bot.polling(none_stop=True, interval=0)
