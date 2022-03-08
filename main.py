import json
import re
import requests
from telegram import Update
from telegram.ext import CallbackContext
from telegram.ext import Updater
from telegram.ext import Filters
from telegram.ext import MessageHandler, CommandHandler, ConversationHandler
from COIN_MARKET_CAP import price_of_crypto

CRYPT = "USD"
CURRENCY = "BITCOIN"


def start(update: Update, context: CallbackContext):
    update.message.reply_text(text="Какую криптовалюту вы хотите?")
    return 1


def get_crypto(update: Update, context: CallbackContext):
    global CRYPT
    CRYPT = update.message.text
    print(CRYPT)
    update.message.reply_text(text="Какую валюту вы хотите?")
    return 2


def get_price(update: Update, context: CallbackContext):
    global CURRENCY
    CURRENCY = update.message.text
    print(CURRENCY)
    price = price_of_crypto(CRYPT, CURRENCY)
    update.message.reply_text(text=f"Цена {CRYPT} в {CURRENCY}: {price}")
    return ConversationHandler.END


def stop(update: Update, context: CallbackContext):
    update.message.reply_text(text="dialog has been stopped")
    return ConversationHandler.END


def main():
    updater = Updater(
        token="5160776370:AAH50HwNs07N_6SvuTxK82gDSpV2OD03Iuw",
        use_context=True
    )

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],

        states={
            1: [MessageHandler(Filters.text, get_crypto, pass_user_data=True)],
            2: [MessageHandler(Filters.text, get_price, pass_user_data=True)]
        },

        fallbacks=[CommandHandler("stop", stop)]
    )

    updater.dispatcher.add_handler(conv_handler)

    updater.dispatcher.add_handler(CommandHandler("start", start))
    updater.dispatcher.add_handler(CommandHandler("stop", stop))

    updater.dispatcher.add_handler(MessageHandler(
        filters=Filters.text,
        callback=get_crypto)
    )

    updater.dispatcher.add_handler(MessageHandler(
        filters=Filters.text,
        callback=get_price)
    )

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
