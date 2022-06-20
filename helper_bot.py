from telegram.ext import CommandHandler, ConversationHandler, Filters, \
    MessageHandler, Updater

from bot_engine import BotEngine
from const import ADMIN, GET_STOCK, MAIN_MENU, TELEGRAM_TOKEN
from utils import check_const


def main():
    if not check_const():
        return
    bot_engine = BotEngine()
    updater = Updater(TELEGRAM_TOKEN)
    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', bot_engine.start)],

        states={
            MAIN_MENU: [
                MessageHandler(Filters.regex('^(Get_stock|Admin|Vacation)$'),
                               bot_engine.main_menu)],
            GET_STOCK: [MessageHandler(Filters.text, bot_engine.get_stock)],
            ADMIN: [MessageHandler(Filters.regex(
                '^(run_cost_calculation|crate_update_file|update_erp)$'),
                bot_engine.admin_menu)],
        },

        fallbacks=[CommandHandler('cancel', bot_engine.cancel)],
    )

    dispatcher.add_handler(conv_handler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
