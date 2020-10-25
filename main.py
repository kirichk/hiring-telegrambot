import logging
import os
from telegram import Bot
from telegram.ext import (CallbackQueryHandler, Updater, MessageHandler,
                            CommandHandler, ConversationHandler, Filters)
from telegram.utils.request import Request
from handlers import (start_buttons_handler, name_handler, phone_handler,
                        niche_handler, vertical_handler, geo_handler,
                        spend_handler, cases_handler, case_details_handler,
                        finish_handler)
from tools.additional_handlers import cancel_handler, echo_handler


logger = logging.getLogger(__name__)

MODE = os.getenv("MODE")
TOKEN = os.getenv('TOKEN')
HEROKU_APP_NAME = os.getenv('HEROKU_APP_NAME')
PORT = int(os.environ.get("PORT", "8443"))

(NAME, PHONE, NICHE, VERTICAL, GEO, SPEND, CASES,
CASE_DETAILS, FINISH) = range(9)


def main():
    '''Setting up all needed to launch bot'''
    logger.info('Started')

    req = Request(
        connect_timeout=30.0,
        read_timeout=1.0,
        con_pool_size=8,
    )
    bot = Bot(
        token=TOKEN,
        request=req,
    )
    updater = Updater(
        bot=bot,
        use_context=True,
    )

    # Проверить что бот корректно подключился к Telegram API
    info = bot.get_me()
    logger.info('Bot info: %s', info)

    # Навесить обработчики команд
    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler('start', start_buttons_handler),
        ],
        states={
            NAME: [CallbackQueryHandler(name_handler,
                                    pass_user_data=True),],
            PHONE: [MessageHandler(Filters.all, phone_handler,
                                    pass_user_data=True),],
            NICHE : [MessageHandler(Filters.all, niche_handler,
                                    pass_user_data=True),],
            VERTICAL: [CallbackQueryHandler(vertical_handler,
                                    pass_user_data=True),],
            GEO: [CallbackQueryHandler(geo_handler,
                                    pass_user_data=True),],
            SPEND: [CallbackQueryHandler(spend_handler,
                                    pass_user_data=True),],
            CASES: [CallbackQueryHandler(cases_handler,
                                    pass_user_data=True),],
            CASE_DETAILS: [CallbackQueryHandler(case_details_handler,
                                    pass_user_data=True),],
            FINISH: [CallbackQueryHandler(
                                    finish_handler,
                                    pass_user_data=True),
                                MessageHandler(Filters.all,
                                    finish_handler,
                                    pass_user_data=True),]
        },
        fallbacks=[
            CommandHandler('cancel', cancel_handler),
        ],
    )
    updater.dispatcher.add_handler(conv_handler)
    updater.dispatcher.add_handler(MessageHandler(Filters.all, echo_handler))

    if MODE == "dev":
        updater.start_polling()
        updater.idle()
        logger.info('Stopped')
    elif MODE == "prod":
        updater.start_webhook(listen="0.0.0.0",
                              port=PORT,
                              url_path=TOKEN)
        updater.bot.set_webhook("https://{}.herokuapp.com/{}".format(
                                        HEROKU_APP_NAME, TOKEN))


if __name__ == '__main__':
    main()
