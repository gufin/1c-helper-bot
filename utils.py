import logging
from http import HTTPStatus

import requests
from telegram import ReplyKeyboardMarkup

from const import ADMIN_ACTIONS_KEYBOARD, ADMIN_KEYBOARD, API_1C_API_TOKEN, \
    API_1C_URL, DEBUG, TELEGRAM_TOKEN, USER_KEYBOARD
from exceptions import EndPointUnAvailable

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


def get_api_answer(method, user):
    """Gets data from 1c api"""
    if DEBUG:
        response = None
        if method == 'get_stock':
            stocks = [{'Номенклатура': 'Мороженое Даша',
                       'Серия': '001',
                       'Склад': '12',
                       'Количество': 1000},
                      {'Номенклатура': 'Мороженое Митя',
                       'Серия': '001',
                       'Склад': '12',
                       'Количество': 177},
                      {'Номенклатура': 'Мороженое белые ночи',
                       'Серия': '001',
                       'Склад': '12',
                       'Количество': 90}
                      ]
            response = {'stocks': stocks}
        elif method == 'vacation':
            vacation = [{'Приод': '01.01.2022 по 14.01.2022'},
                        {'Приод': '01.03.2022 по 14.03.2022'}]
            response = {'vacation': vacation}

        if method in ADMIN_ACTIONS_KEYBOARD:
            admin_answer = [{'status': True}]
            response = {method: admin_answer}

        if method == 'check_admin':
            check_admin = [{'status': True}]
            response = {'check_admin': check_admin}

        return response

    else:
        params = {'method': method,
                  'user': user.id}
        headers = {'Authorization': f'OAuth {API_1C_API_TOKEN}'}
        try:
            response = requests.post(API_1C_URL, headers=headers, params=params)
            if response.status_code != HTTPStatus.OK:
                logger.error(f'Ошибка {response.status_code}!')
                raise Exception(f'Ошибка {response.status_code}!')
            else:
                response = response.json()
        except EndPointUnAvailable:
            error_text = f'Сбой в работе программы: {API_1C_URL} недоступен.'
            logger.exception(error_text)
            response = None

    return response


def check_const() -> bool:
    """Checks that environment variables are set."""
    response = True
    if API_1C_API_TOKEN is None:
        response = False
        logger.critical('Отсутствует обязательная переменная окружения '
                        'API_1C_API_TOKEN')
    if TELEGRAM_TOKEN is None:
        response = False
        logger.critical('Отсутствует обязательная переменная окружения '
                        'TELEGRAM_TOKEN')

    if API_1C_URL is None:
        response = False
        logger.critical('Отсутствует обязательная переменная окружения '
                        'API_1C_URL')

    return response


def get_menu_keyboard(bot_obj, user, menu_type):
    """Returns the keyboard of the desired menu type."""
    reply_keyboard = None
    if menu_type == 'main':
        if bot_obj.user_is_admin(user):
            reply_keyboard = [ADMIN_KEYBOARD]
        else:
            reply_keyboard = [USER_KEYBOARD]

    if menu_type == 'admin':
        reply_keyboard = [ADMIN_ACTIONS_KEYBOARD]

    return ReplyKeyboardMarkup(reply_keyboard,
                               one_time_keyboard=True,
                               resize_keyboard=True)
