import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from telegram import Update
# from telegram.ext.filters import Filters
# This gives us all information of all the event that are taking place

# ENABLE LOGGING
logging.basicConfig(
    format='%(asctime)s-%(name)s-%(levelname)s-%(message)s', level=logging.INFO)
# This function return the information of an event in this format:- first the time is given then
# the name/class in which it took place then the level of event if the level is higher we pay more
# attention to it next is the message with the event
logger = logging.getLogger(__name__)

TOKEN = '1573406639:AAFTEAD_lbcezsGfVKK_N-pYjFnHbyUvlrM'


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


def echo_text(update: Update, context: CallbackContext):
    # To get the message that the user sent
    print(update.to_dict())
    # Converting the given msg to a dictionary and then accessing the message part and inside
    # the message part we are trying to access an element called text that contains our message
    text = update.to_dict()['message']['text']
    update.message.reply_text(text)


def echo_sticker(update: Update, context: CallbackContext):
    # To get the sticker that the user sent
    # reply = update.message.sticker
    print(update)
    # Converting the given msg to a dictionary and then accessing the message part and inside
    # the message part we are trying to access an element called sticker that contains our our
    # sticker id which we then access it by file_id
    stick = update.to_dict()
    print("\n")
    print(stick)
    s = stick['message']['sticker']['file_id']
    print("\n")
    print(s)
    update.message.reply_sticker(s)


def error(bot, update):
    logger.error(f'Update {update} caused error:- {update.error}')


def main():
    # Updater checks that if there is a command that a user is sending and if it is then it will
    # ask the dispatcher to handle the commands just like in discord in Rythm if we say !play
    # it plays that music
    updater = Updater(TOKEN)
    dp = updater.dispatcher
    # If a user sends a msg /start to bot then the will send this # info to start function
    # and give a reply accordingly
    dp.add_handler(CommandHandler("start", start))
    # Similary for /help command
    dp.add_handler(CommandHandler("help", help))
    # If a user sends any other messsage then we use Message Handler and we get if the messagt type
    # is a text or a sticker if it is a text then we send back same text similarly for a sticker
    dp.add_handler(MessageHandler(Filters.text, echo_text))
    dp.add_handler(MessageHandler(Filters.sticker, echo_sticker))
    # This is used to handle the error
    dp.add_error_handler(logging.error)

    # We are starting our bot and activating it this function keeps on checking if a user has given a message or not
    updater.start_polling()
    logger.info("Started Polling....")
    updater.idle()  # If we press CTRL+C  the bot should stop executing.


if __name__ == '__main__':
    main()
