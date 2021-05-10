import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, Dispatcher
from telegram import Update
from telegram import Bot
from telegram import ReplyKeyboardMarkup
from flask import Flask, request
from utils import get_reply, fetch_news, topics_keyboard
# This gives us all information of all the event that are taking place

# ENABLE LOGGING
logging.basicConfig(
    format='%(asctime)s-%(name)s-%(levelname)s-%(message)s', level=logging.INFO)
# This function return the information of an event in this format:- first the time is given then
# the name/class in which it took place then the level of event if the level is higher we pay more
# attention to it next is the message with the event
logger = logging.getLogger(__name__)

TOKEN = '1573406639:AAFTEAD_lbcezsGfVKK_N-pYjFnHbyUvlrM'

app = Flask(__name__)  # Always have to create an app for starting flask


# This function return Hello! whenever we send a message to telegram
@app.route('/')
def index():
    return "Hello!"

# This method helps to get the dispatcher for the update i.e the message that we sent to the
# telegram is converted to the dispatcher i.e a reponse to our message like for /start say hi,
# for /help display a message for help and etc


@app.route(f'/{TOKEN}', methods=['GET', 'POST'])
def webhook():
    """webhook view which receives updates from telegram"""
    # create update object from json-format request data
    # We get a json object from telegram
    update = Update.de_json(request.get_json(), bot)
    # and we convert it into an update object

    # process update
    dp.process_update(update)  # Then we send the dispatcher
    return "ok"


def start(update: Update, context: CallbackContext):
    print(update)
    # Get the first name of the user from the message
    author = update.message.from_user.first_name
    reply = f"Hi {author}"  # Create a reply message for the user
    # Sending the reply to the chat id of the user
    update.message.reply_text(reply)


def help(update: Update, context: CallbackContext):
    reply = f'This is a help message for {update.message.from_user.first_name}'
    update.message.reply_text(reply)


def news(update: Update, context: CallbackContext):
    chat_id = update['message']['chat']['id']
    bot.send_message(chat_id=chat_id, text="Choose a category",
                     reply_markup=ReplyKeyboardMarkup(keyboard=topics_keyboard, one_time_keyboard=True))


def echo_text(update: Update, context: CallbackContext):
    # To get the message that the user sent
    print(update.to_dict())
    # Converting the given msg to a dictionary and then accessing the message part and inside
    # the message part we are trying to access an element called text that contains our message
    chat_id = update['message']['chat']['id']
    msg = update['message']['text']
    intent, reply = get_reply(msg, chat_id)
    if intent == "get_news":
        articles = fetch_news(reply)
        for article in articles:
            update.message.reply_text(article['link'])
    else:
        update.message.reply_text(reply)


def echo_sticker(update: Update, context: CallbackContext):
    # To get the sticker that the user sent
    # reply = update.message.sticker
    print(update)
    # Converting the given msg to a dictionary and then accessing the message part and inside
    # the message part we are trying to access an element called sticker that contains our our
    # sticker id which we then access it by file_id
    stick = update
    print("\n")
    print(stick)
    s = stick['message']['sticker']['file_id']
    print("\n")
    print(s)
    update.message.reply_sticker(s)


def error(bot, update):
    logger.error(f'Update {update} caused error:- {update.error}')

# Updater checks that if there is a command that a user is sending and if it is then it will
# ask the dispatcher to handle the commands just like in discord in Rythm if we say !play
# it plays that music
bot = Bot(TOKEN)
try:
    bot.set_webhook("https://aqueous-citadel-17101.herokuapp.com/"+TOKEN)
except Exception as e:
    print(e)
dp = Dispatcher(bot, None)
# If a user sends a msg /start to bot then the will send this # info to start function
# and give a reply accordingly
dp.add_handler(CommandHandler("start", start))
# Similary for /help command
dp.add_handler(CommandHandler("help", help))
# Similarly we have a news command
dp.add_handler(CommandHandler("news", news))
# If a user sends any other messsage then we use Message Handler and we get if the messagt type
# is a text or a sticker if it is a text then we send back same text similarly for a sticker
dp.add_handler(MessageHandler(Filters.text, echo_text))
dp.add_handler(MessageHandler(Filters.sticker, echo_sticker))
# This is used to handle the error
dp.add_error_handler(logging.error)


if __name__ == '__main__':
    app.run(port=8443)
