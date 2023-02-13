from pathlib import Path
import random
import string
import bot_settings
from UserControl import UserControl
from SpotControl import SpotControl
from mongoDB import connect_database
from logger import logger
from telegram.ext import (
    CallbackContext,
)
from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Update,
)


def start_handler(update: Update, context: CallbackContext):
    chat_id = update.effective_message.chat_id
    database = connect_database()
    user_control = UserControl(database)
    if not user_control.find_user(chat_id):
        user_control.add_user(chat_id)
        logger.info(f"new user with chat_id #{chat_id} created")
        context.bot.send_message(chat_id, bot_settings.WELCOME)
    else:
        context.bot.send_message(chat_id, bot_settings.HELP)
        logger.info(f"chat_id #{chat_id} started")


def help_handler(update: Update, context: CallbackContext):
    chat_id = update.effective_message.chat_id
    context.bot.send_message(chat_id, bot_settings.HELP)


def get_user_spots_handler(update: Update, context: CallbackContext):
    chat_id = update.effective_message.chat_id
    database = connect_database()
    user_control = UserControl(database)
    spots = user_control.get_user_from_db(chat_id)
    keyboard = [
        [
            InlineKeyboardButton(value, callback_data=f"user_spot_{key}")
            for area in bot_settings.BEACHES.values()
            for key, value in area.items()
            if key in spots["spots"]
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.bot.send_message(
        chat_id=chat_id, text="Choose a spot:", reply_markup=reply_markup
    )
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
        text="Choose an area:",
        reply_markup=reply_markup,
    )
    logger.info(f"chat_id #{chat_id} wants to registrate new spot")


def area_handler(update: Update, context: CallbackContext):
    chat_id = update.effective_message.chat_id
    option = update.callback_query.data
    update.callback_query.answer(f"Selected area: {option}")
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
        text="Choose a beach to register:",
        reply_markup=reply_markup,
    )


def spot_handler(update: Update, context: CallbackContext):
    chat_id = update.effective_message.chat_id
    context.user_data["cur_spot"] = update.callback_query.data
    database = connect_database()
    spot_control = SpotControl(database)
    user_control = UserControl(database)
    spot = spot_control.get_spot_by_id(context.user_data["cur_spot"])
    user_control.set_spot(chat_id, update.callback_query.data)
    logger.info(f"chat_id #{chat_id} registered spot #{update.callback_query.data}")
    context.bot.send_message(
        chat_id,
        "Spot successfully registered.\nNow you will receive daily forecast of your spot and you can also share with others your own wave-report of your spot",
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


def report_handler(update: Update, context: CallbackContext):
    chat_id = update.effective_message.chat_id
    context.bot.send_message(
        chat_id, "Send a picture of the spot's waves and share with other"
    )


def get_user_interaction(update: Update, context: CallbackContext):
    chat_id = update.effective_message.chat_id
    key = update.callback_query.data.split("_")
    context.user_data["cur_spot"] = key[2]
    keyboard = [
        [
            InlineKeyboardButton("Get forecast", callback_data="forecast"),
            InlineKeyboardButton("Send your personal report", callback_data="report"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.bot.send_message(
        chat_id=chat_id,
        text="Please choose an action:",
        reply_markup=reply_markup,
    )


def photos_upload_handler(update: Update, context: CallbackContext):
    PHOTOS_PATH = Path(".") / "_photos"
    PHOTOS_PATH.mkdir(exist_ok=True)
    chat_id = update.effective_chat.id
    text = update.message.text
    code = "".join(
        random.choices(string.ascii_lowercase + string.digits, k=16)
    )  # generates a name for photo file
    filename = PHOTOS_PATH / f"photo_{code}.jpeg"
    uploaded_photo = update.message.photo[-1].get_file()
    uploaded_photo.download(str(filename))
    database = connect_database()
    spot_control = SpotControl(database)
    spot_control.add_pic_to_spot(context.user_data["cur_spot"], filename)
    logger.info(f"= Got photo on chat #{chat_id}, saved on {filename}")
    response = f"Thank you for your upload"
    send_updated_pic_to_users(context.user_data["cur_spot"], filename, context)
    context.bot.send_message(chat_id=update.message.chat_id, text=response)


def send_updated_pic_to_users(spot_id, pic, context: CallbackContext):
    database = connect_database()
    users = UserControl(database)
    for user in users.users.find({"spots": {"$in": [spot_id]}}):
        print()
        context.bot.send_photo(user["chat_id"], open(pic, "rb"))


def send_daily_forecast(context: CallbackContext):
    logger.info(f"Bot sending automatic daily forecast")
    database = connect_database()
    user_control = UserControl(database)
    spot_control = SpotControl(database)
    for user in user_control.users.find():
        for spot in user["spots"]:
            spot_control.set_spot_forecast(spot)
            context.bot.send_photo(
                user["chat_id"], spot_control.get_spot_forecast(spot)
            )
