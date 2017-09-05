#-*- coding: utf-8 -*-
import cherrypy, telebot
import base, const, markups

WEBHOOK_HOST = '77.244.215.222'
WEBHOOK_PORT = 8443  # 443, 80, 88, 8443
WEBHOOK_LISTEN = '0.0.0.0'

WEBHOOK_SSL_CERT = 'webhook_cert.pem'
WEBHOOK_SSL_PRIV = 'webhook_pkey.pem'

WEBHOOK_URL_BASE = "https://%s:%s" % (WEBHOOK_HOST, WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/%s/" % (const.token)

bot = telebot.TeleBot(const.token)


class WebhookServer(object):
    @cherrypy.expose
    def index(self):
        if 'content-length' in cherrypy.request.headers and \
                        'content-type' in cherrypy.request.headers and \
                        cherrypy.request.headers['content-type'] == 'application/json':
            length = int(cherrypy.request.headers['content-length'])
            json_string = cherrypy.request.body.read(length).decode("utf-8")
            update = telebot.types.Update.de_json(json_string)
            # Эта функция обеспечивает проверку входящего сообщения
            bot.process_new_updates([update])
            return ''
        else:
            raise cherrypy.HTTPError(403)


@bot.message_handler(commands=["start"])
def start(message):
    sent = bot.send_message(message.chat.id, const.welcome_msg, reply_markup=markups.admin(message.chat.id))
    bot.register_next_step_handler(sent, reply_msg)


def reply_msg(message):
    if (message.text != "Админ-панель" and not base.is_in_base(message.chat.id)):
        request_num = base.add_user(message.chat.id)
        if (request_num != -1):
            bot.send_message(message.chat.id, const.reply_msg.format(id = request_num), reply_markup=markups.start())
            bot.send_message(const.admin_id,
                             str(message.from_user.first_name) + " " + str(message.from_user.last_name) + "; @" + str(
                                 message.from_user.username) + "; " + str(request_num))
            bot.send_message(const.admin_id_1,
                             str(message.from_user.first_name) + " " + str(message.from_user.last_name) + "; @" + str(
                                 message.from_user.username) + "; " + str(request_num))
            bot.send_message(const.admin_id, "%s %s Заявка номер: %d"%message.from_user.first_name %message.from_user.last_name %request_num)
        else:
            bot.send_message(message.chat.id, "Сервис временно не доступен. Попробуйте позже")
            bot.send_message(const.admin_id, "Ошибка! Не могу выдать номер заявки")


@bot.message_handler(regexp="Админ-панель")
def admin(message):
    if (message.chat.id == const.admin_id):
        bot.send_message(message.chat.id, "Выберите текст", reply_markup=markups.edit_texts())


@bot.callback_query_handler(func = lambda call: call.data == "text1_edit")
def edit1(call):
    sent = bot.send_message(call.message.chat.id, "Введите новый текст")
    bot.register_next_step_handler(sent, confirm1)

def confirm1(message):
    base.drop_table()
    base.create_table()
    #const.counter = 0
    const.welcome_msg = message.text
    bot.send_message(message.chat.id, "Выберите текст", reply_markup=markups.edit_texts())


@bot.callback_query_handler(func=lambda call: call.data == "tetx2_edit")
def edit2(call):
    sent = bot.send_message(call.message.chat.id, "Текст успешно изменен!")
    bot.register_next_step_handler(sent, confirm2)

def confirm2(message):
    base.drop_table()
    base.create_table()
    #const.counter = 0
    const.reply_msg = message.text
    bot.send_message(message.chat.id, "Текст успешно изменен!", reply_markup=markups.edit_texts())


@bot.callback_query_handler(func=lambda call: call.data == "counter")
def counter(call):
    const.counter = 80


#print(bot.get_webhook_info())
bot.remove_webhook()
#bot.set_webhook(url=WEBHOOK_URL_BASE + WEBHOOK_URL_PATH,
           #     certificate=open(WEBHOOK_SSL_CERT, 'r'))

cherrypy.config.update({
    'server.socket_host': WEBHOOK_LISTEN,
    'server.socket_port': WEBHOOK_PORT,
    'server.ssl_module': 'builtin',
    'server.ssl_certificate': WEBHOOK_SSL_CERT,
    'server.ssl_private_key': WEBHOOK_SSL_PRIV
})


cherrypy.quickstart(WebhookServer(), WEBHOOK_URL_PATH, {'/': {}})
