import logging
import os
from http import HTTPStatus

import requests
from dotenv import load_dotenv

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
)

from exceptions import EndPointUnAvailable

load_dotenv()

ONE_C_API_TOKEN = os.getenv('ONE_C_API_TOKEN')
ONE_C_URL = os.getenv('ONE_C_URL')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

MAIN_MENU, GET_STOCK, ADMIN, VACATION = range(4)


def start(update, _):
    user = update.message.from_user
    if user_is_admin(user):
        reply_keyboard = [['Get_stock', 'Admin', 'Vacation']]
    else:
        reply_keyboard = [['Get_stock', 'Vacation']]
    markup_key = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    update.message.reply_text(
        'Привет я ваш виртуальный помошник Борис. '
        'Команда /cancel, чтобы прекратить разговор.\n\n'
        'Вот что я могу',
        reply_markup=markup_key, )

    return MAIN_MENU


def main_menu(update, _):
    user = update.message.from_user
    logger.info("Action %s: %s", user.first_name, update.message.text)

    if update.message.text == 'Get_stock':
        update.message.reply_text(
            'Введите артикул или название номенклатуры.',
            reply_markup=ReplyKeyboardRemove(),
        )
        return GET_STOCK

    if update.message.text == 'Admin':
        reply_keyboard = [['run_cost_calculation', 'crate_update_file', 'update_erp']]
        markup_key = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
        update.message.reply_text(
            'Привет я ваш виртуальный помошник Борис Н. '
            'Команда /cancel, чтобы прекратить разговор.\n\n'
            'Вот что я могу',
            reply_markup=markup_key, )
        return ADMIN

    if update.message.text == 'Vacation':
        return VACATION


def get_stock(update, _):
    user = update.message.from_user
    logger.info("Action %s: %s", user.first_name, update.message.text)

    response = get_api_answer('get_stock', user)

    if response is None:
        text_message = 'К сожалению, ответ от api пуст.'
    else:
        stocks = response['stocks']
        text_message = f'Вот что мне удалось найти: {stocks}'

    update.message.reply_text(
        text_message,
        reply_markup=ReplyKeyboardRemove(),
    )
    return ConversationHandler.END


def cancel(update, _):
    user = update.message.from_user
    logger.info("Пользователь %s отменил разговор.", user.first_name)
    update.message.reply_text(
        'Мое дело предложить - Ваше отказаться'
        ' Будет скучно - пиши.',
        reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END


def admin_menu(update, _):
    user = update.message.from_user
    logger.info("Пользователь %s запросил действие %s", user.first_name, update.message.text)

    reply_keyboard = [['Get_stock', 'Admin', 'Vacation']]
    markup_key = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    success_message = ''
    if update.message.text == 'run_cost_calculation':
        success_message = 'Запущен расчет себестоймости',

    if update.message.text == 'crate_update_file':
        success_message = 'Запущено создание файла поставки erp',

    if update.message.text == 'update_erp':
        success_message = 'Запущено обновление erp',

    response = get_api_answer(update.message.text, user)
    if response is None:
        text_message = 'К сожалению, ответ от api пуст.'
    else:
        text_message = success_message

    update.message.reply_text(
        text_message,
        reply_markup=markup_key, )

    return MAIN_MENU


def vacation(update, _):
    user = update.message.from_user
    logger.info("Action %s: %s", user.first_name, update.message.text)

    response = get_api_answer('vacation', user)

    if response is None:
        text_message = 'К сожалению, ответ от api пуст.'
    else:
        vacation_data = response['vacation']
        text_message = f'Вот что мне удалось найти: {vacation_data}'

    update.message.reply_text(
        text_message,
        reply_markup=ReplyKeyboardRemove(),
    )
    return ConversationHandler.END


def check_const() -> bool:
    """Checks that environment variables are set."""
    response = True
    if ONE_C_API_TOKEN is None:
        response = False
        logger.critical('Отсутствует обязательная переменная окружения '
                        'ONE_C_API_TOKEN')
    if TELEGRAM_TOKEN is None:
        response = False
        logger.critical('Отсутствует обязательная переменная окружения '
                        'TELEGRAM_TOKEN')

    if ONE_C_URL is None:
        response = False
        logger.critical('Отсутствует обязательная переменная окружения '
                        'ONE_C_URL')

    return response


def get_api_answer(method, user):
    """Gets data from 1c api"""
    '''
    params = {'method': method,
              'user': user.id}
    headers = {'Authorization': f'OAuth {ONE_C_API_TOKEN}'}
    try:
        response = requests.post(ONE_C_URL, headers=headers, params=params)
        if response.status_code != HTTPStatus.OK:
            logger.error(f'Ошибка {response.status_code}!')
            raise Exception(f'Ошибка {response.status_code}!')
        else:
            response = response.json()
    except EndPointUnAvailable:
        error_text = f'Сбой в работе программы: {ONE_C_URL} недоступен.'
        logger.exception(error_text)
        response = None
    return response
    '''
    return None


def user_is_admin(user):
    response = get_api_answer('check_admin', user)
    '''
    if response is None:
        return False
    else:
        return True
    '''
    return True


def main():
    if not check_const():
        return

    updater = Updater(TELEGRAM_TOKEN)
    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            MAIN_MENU: [MessageHandler(Filters.regex('^(Get_stock|Admin|Vacation)$'), main_menu)],
            GET_STOCK: [MessageHandler(Filters.text, get_stock)],
            ADMIN: [MessageHandler(Filters.regex('^(run_cost_calculation|crate_update_file|update_erp)$'), admin_menu)],
            VACATION: [MessageHandler(Filters.text, vacation)]
        },

        fallbacks=[CommandHandler('cancel', cancel)],
    )

    dispatcher.add_handler(conv_handler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
