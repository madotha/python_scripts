# This tutorial was created according to the tutorial from python-telegram-bot
# Version 12.0.0b1 was used for this
# https://github.com/python-telegram-bot/python-telegram-bot/wiki/Extensions-%E2%80%93-Your-first-Bot

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, InlineQueryHandler
from telegram import InlineQueryResultArticle, InputTextMessageContent
from telegram.error import BadRequest
import logging

# The following sets configuration for your Logging
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                           level=logging.INFO)

# Create an instance of your logger, for easier access in your code
LOG = logging.getLogger(__name__)

# /start command, returns preconfigured welcome text
def start(update, context):
    username = update.message.from_user.username
    chatid = update.message.chat_id

    context.bot.send_message(chat_id=chatid, text="I'm a bot, please talk to me!")
    LOG.info("User [%s][%s]: Start received, echo back start text", username, chatid)

# Inline command to convert the sent argument into uppercase text
# To use inline command, turn on Inline mode in @BotFather for your bot
# This command is being accessed by typing @{NameOfYourBot} in a chat or group
def inline_caps(update, context):
    query = update.inline_query.query
    if not query:
        return
    results = list()
    results.append(
        InlineQueryResultArticle(
            id=query.upper(),
            title='Caps',
            input_message_content=InputTextMessageContent(query.upper())
        )
    )
    context.bot.answer_inline_query(update.inline_query.id, results)


# /caps command, converts text sent with this command into uppercase text
def caps(update, context):
    username = update.message.from_user.username
    chatid = update.message.chat_id
    text = update.message.text
    text_caps = ' '.join(context.args).upper()
    try:
        context.bot.send_message(chat_id=chatid, text=text_caps)
        LOG.info("User [%s][%s]: received [%s] for caps", username, chatid, text)
    except BadRequest:
        LOG.error("User [%s][%s]: typed /caps without an argument", username, chatid)

# If text isn't a command, echo back the message to the user
def echo(update, context):
    username = update.message.from_user.username
    chatid = update.message.chat_id
    text = update.message.text

    context.bot.send_message(chat_id=chatid, text=text)
    LOG.info("User [%s][%s]: echoed back [%s]", username, chatid, text)

# If a command is unknown to the bot, return preconfigured "error" message
def unknown(update, context):
    username = update.message.from_user.username
    chatid = update.message.chat_id
    text = update.message.text

    context.bot.send_message(chat_id=chatid, text="Sorry, I don't know that command.")

# Main method, contains all commands executed when running the bot
def main():
    # Hand over Bot token to the Updater
    updater = Updater(token='TOKEN', use_context=True)
    # Initialize Dispatcher for your Updater
    dispatcher = updater.dispatcher
    # Add handlers for commands and messages
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('caps', caps))
    dispatcher.add_handler(MessageHandler(Filters.text, echo))
    dispatcher.add_handler(InlineQueryHandler(inline_caps))
    dispatcher.add_handler(MessageHandler(Filters.command, unknown))
    # Start receiving messages with your bot
    updater.start_polling()


if __name__ == '__main__':
    main()
