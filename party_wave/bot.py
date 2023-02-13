import bot_settings
from logger import logger
from bot_handlers import (
    start_handler,
    app_help,
    get_spots_handler,
    registration_handler,
    area_handler,
    spot_handler,
    get_forecast,
    get_user_interaction,
    photos_upload_handler
)
from telegram.ext import (
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    Filters,
    Updater,
    CallbackContext,
)


def bot():

    updater = Updater(token=bot_settings.BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start_handler))
    dispatcher.add_handler(CommandHandler("help", app_help))
    dispatcher.add_handler(CommandHandler("list", get_spots_handler))
    dispatcher.add_handler(CommandHandler("register", registration_handler))
    dispatcher.add_handler(MessageHandler(Filters.photo, photos_upload_handler))
    dispatcher.add_handler(
        CallbackQueryHandler(area_handler, pattern="^(north|central|south)$")
    )
    dispatcher.add_handler(
        CallbackQueryHandler(
            spot_handler,
            pattern=f"^({'|'.join(key for area in bot_settings.BEACHES.values() for key in area.keys())})",
        )
    )
    dispatcher.add_handler(CallbackQueryHandler(get_forecast, pattern="forecast"))
    dispatcher.add_handler(CallbackQueryHandler(get_user_interaction, pattern="user"))

    logger.info("** Start polling **")
    updater.start_polling()
    updater.idle()
    logger.info("** Server turning off! **")


bot()
