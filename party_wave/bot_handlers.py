import bot_settings
from UserControl import UserControl
from SpotControl import SpotControl
from WaveForecast import WaveForecast
from mongoDB import connect_database
from logger import logger
from telegram.ext import (
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    Filters,
    Updater,
    CallbackContext,
)
from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Update,
)


def app_help(update: Update, context: CallbackContext):
    pass


def start_handler(update: Update, context: CallbackContext):
    chat_id = update.effective_message.chat_id
    database = connect_database()
    user_control = UserControl(database)
    if not user_control.find_user(chat_id):
        user_control.add_user(chat_id)
        logger.info(f"new user with chat_id #{chat_id} created")
        context.bot.send_message(chat_id, "Welcome ...")
    else:
        context.bot.send_message(
            chat_id,
            "/register to register a new spot\n/list to se yours spots\n/help for more information",
        )
        logger.info(f"chat_id #{chat_id} started")


def get_spots_handler(update: Update, context: CallbackContext):
    chat_id = update.effective_message.chat_id
    database = connect_database()
    user_control = UserControl(database)
    spots = user_control.get_user_spots(chat_id)
    context.bot.send_message(chat_id, spots)
    logger.info(f"chat_id #{chat_id} asked for spots list")


def registration_handler(update: Update, context: CallbackContext):
    chat_id = update.effective_message.chat_id
    keyboard = [
        [
            InlineKeyboardButton("North", callback_data="north"),
            InlineKeyboardButton("Central", callback_data="central"),
            InlineKeyboardButton("South", callback_data="south"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.bot.send_message(
        chat_id=chat_id,
        text="Please choose an area:",
        reply_markup=reply_markup,
    )
    logger.info(f"chat_id #{chat_id} wants to registrate new spot")


def area_handler(update: Update, context: CallbackContext):
    chat_id = update.effective_message.chat_id
    option = update.callback_query.data
    update.callback_query.answer(f"You selected area {option}")
    if option == "north":
        keyboard = [
            [
                InlineKeyboardButton(place, callback_data=key)
                for key, place in bot_settings.BEACHES["north"].items()
            ]
        ]

    elif option == "central":
        keyboard = [
            [
                InlineKeyboardButton(place, callback_data=key)
                for key, place in bot_settings.BEACHES["central"].items()
            ]
        ]
    elif option == "south":
        keyboard = [
            [
                InlineKeyboardButton(place, callback_data=key)
                for key, place in bot_settings.BEACHES["south"].items()
            ]
        ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    context.bot.send_message(
        chat_id=chat_id,
        text="Please choose a beach:",
        reply_markup=reply_markup,
    )
    logger.info(f"chat_id #{chat_id} chosed area #{option}")


def spot_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    chat_id = update.effective_message.chat_id
    option = query.data
    context.user_data["cur_spot"] = option
    database = connect_database()
    user_control = UserControl(database)
    spot_control = SpotControl(database)
    user_control.set_spot(chat_id, option)
    spot_control.add_user_to_spot(option, chat_id)
    logger.info(f"chat_id #{chat_id} registered spot #{option}")
    context.bot.send_message(
        chat_id,
        "Spot successfully registered.\nNow you will receive daily forecast of your spot and you can also share with others your own wave-report of your spot",
    )
    keyboard = [
        [
            InlineKeyboardButton("Get forecast", callback_data="forecast"),
            InlineKeyboardButton("Send your personal report", callback_data="user"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    logger.info(f"chat_id #{chat_id} chosed spot #{option}")
    context.bot.send_message(
        chat_id=chat_id,
        text="Please choose an action:",
        reply_markup=reply_markup,
    )


def get_forecast(update: Update, context: CallbackContext):
    chat_id = update.effective_message.chat_id
    spot_id = context.user_data["cur_spot"]
    database = connect_database()
    spot_control = SpotControl(database)
    spot_control.set_spot_forecast(spot_id)
    forecast = spot_control.get_spot_forecast(spot_id)
    logger.info(f"chat_id #{chat_id} asked for forecast")
    context.bot.send_message(chat_id, forecast)


def get_user_interaction(update: Update, context: CallbackContext):
    chat_id = update.effective_message.chat_id
    logger.info(f"chat_id #{chat_id} wants to send a ")
    context.bot.send_message(
        chat_id, "Send a picture or a message about the waves situation"
    )
