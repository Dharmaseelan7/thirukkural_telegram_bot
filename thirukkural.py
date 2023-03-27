import requests
import json
import telegram.ext

Token = "6184270165:AAF-wCzNzn50K8NSK83KxLOtR6-lcHIdKD0"


updater = telegram.ext.Updater(
    Token, use_context=True)

dispatcher = updater.dispatcher


def start(update, context):
    update.message.reply_text(
        "Hi welcome to thirukkural bot.Please write /help to see the commands available.")


def help(update, context):
    update.message.reply_text("""Available commands:
    /thirukkural""")


def tk_lang(update, context):

    update.message.reply_text("""Choose the language.
    1.Tamil
    2.English""")

    return 'thirukkural'


def tk(update, context):
    global t_lang
    t_lang = update.message.text
    global lang
    lang = t_lang.lower()

    while (lang != 'tamil' and lang != 'english'):
        tk_lang(update, context)
        return 'thirukkural'

    update.message.reply_text("""
    1.Write the thirukkural no to get the corresponding thirukkural.
    2.To exit - write exit  """)
    return 'get_thirukkural'


def get_tk(update, context):
    t_no = update.message.text
    t_no = t_no.lower()

    try:

        if (t_no == 'exit'):
            update.message.reply_text("Bye!")
            return telegram.ext.ConversationHandler.END

        elif (int(t_no) <= 1330):

            while (t_no != "exit"):

                response_api = requests.get(
                    "https://api-thirukkural.vercel.app/api?num={}".format(t_no))
                data = response_api.text

                parse_json = json.loads(data)
                if lang == "english":
                    update.message.reply_text("""{}
                            """.format(parse_json['eng']))

                elif lang == "tamil":
                    update.message.reply_text("""{0}
                        {1}""".format(
                        parse_json['line1'], parse_json['line2']))
                return 'get_thirukkural'
    except:
        pass
    get_tk_warn(update, context)


def cancel(update, context):
    update.message.reply_text('Bye!')
    return telegram.ext.ConversationHandler.END


def get_tk_warn(update, context):
    update.message.reply_text("""
        1.Write the thirukkural no to get the corresponding thirukkural.
        2.To exit - write exit  """)

    return 'get_thirukkural'


conv_handler = telegram.ext.ConversationHandler(
    entry_points=[telegram.ext.CommandHandler("thirukkural", tk_lang)],
    states={
        'thirukkural': [telegram.ext.MessageHandler(telegram.ext.Filters.text, tk)],
        'get_thirukkural': [telegram.ext.MessageHandler(telegram.ext.Filters.text, get_tk)],
        'get_thirukkural_warn': [telegram.ext.MessageHandler(telegram.ext.Filters.text, get_tk_warn)]
    },
    fallbacks=[telegram.ext.CommandHandler("cancel", cancel)]
)

dispatcher.add_handler(telegram.ext.CommandHandler('start', start))
dispatcher.add_handler(telegram.ext.CommandHandler('help', help))


dispatcher.add_handler(conv_handler)
updater.start_polling()
updater.idle()
