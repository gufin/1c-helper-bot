import logging

from telegram import ReplyKeyboardRemove
from telegram.ext import ConversationHandler

from const import *
from utils import get_api_answer, get_menu_keyboard

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


class BotEngine:

    def start(self, update, _):
        user = update.message.from_user
        markup_key = get_menu_keyboard(self, user, 'main')
        update.message.reply_text(
            'Привет я ваш виртуальный помошник Борис. '
            'Команда /cancel, чтобы прекратить разговор.\n\n'
            'Вот что я могу',
            reply_markup=markup_key, )

        return MAIN_MENU

    def main_menu(self, update, _):
        user = update.message.from_user
        logger.info("Action %s: %s", user.first_name, update.message.text)
        if update.message.text == 'Get_stock':
            update.message.reply_text(
                'Введите артикул или название номенклатуры.',
                reply_markup=ReplyKeyboardRemove(),
            )
            return GET_STOCK

        if update.message.text == 'Admin':
            markup_key = get_menu_keyboard(self, user, 'admin')
            update.message.reply_text(
                'Что хотите сделать?',
                reply_markup=markup_key, )
            return ADMIN

        if update.message.text == 'Vacation':
            markup_key = get_menu_keyboard(self, user, 'main')
            response = get_api_answer('vacation', user)
            if response is None:
                text_message = 'Не удалось получить информацию ' \
                               'по данному запросу'
            else:
                vacation_data = response['vacation']
                vacation_str = ', '.join(d['Приод'] for d in vacation_data)
                text_message = f'Вот что мне удалось найти: {vacation_str}'
            update.message.reply_text(
                text_message,
                reply_markup=markup_key, )

            return MAIN_MENU

    def get_stock(self, update, _):
        user = update.message.from_user
        logger.info("Action %s: %s", user.first_name, update.message.text)
        markup_key = get_menu_keyboard(self, user, 'main')
        response = get_api_answer('get_stock', user)

        if response is None:
            text_message = 'Не удалось получить информацию по данному запросу'
        else:
            stocks = response['stocks']
            stocks_string = str(stocks)
            text_message = f'Вот что мне удалось найти: {stocks_string}'

        update.message.reply_text(
            text_message,
            reply_markup=markup_key,
        )
        return MAIN_MENU

    def cancel(self, update, _):
        user = update.message.from_user
        logger.info("Пользователь %s отменил разговор.", user.first_name)
        update.message.reply_text(
            'Мое дело предложить - Ваше отказаться'
            ' Будет скучно - пиши.',
            reply_markup=ReplyKeyboardRemove()
        )

        return ConversationHandler.END

    def admin_menu(self, update, _):
        user = update.message.from_user
        logger.info("Пользователь %s запросил действие %s", user.first_name,
                    update.message.text)

        markup_key = get_menu_keyboard(self, user, 'main')
        text_message = ''
        if update.message.text == 'crate_update_file':
            text_message = 'Запущено создание файла поставки erp',

        elif update.message.text == 'run_cost_calculation':
            text_message = 'Запущен расчет себестоймости',

        elif update.message.text == 'update_erp':
            text_message = 'Запущено обновление erp',

        response = get_api_answer(update.message.text, user)
        if response is None:
            text_message = 'Не удалось получить информацию по данному запросу'

        update.message.reply_text(
            text_message,
            reply_markup=markup_key, )

        return MAIN_MENU

    def vacation(self, update, _):
        user = update.message.from_user
        logger.info("Action %s: %s", user.first_name, update.message.text)
        markup_key = get_menu_keyboard(self, user, 'main')
        response = get_api_answer('vacation', user)

        if response is None:
            text_message = 'Не удалось получить информацию по данному запросу'
        else:
            vacation_data = response['vacation']
            vacation_str = ', '.join(d['Приод'] for d in vacation_data)
            text_message = f'Вот что мне удалось найти: {vacation_str}'

        update.message.reply_text(
            text_message,
            reply_markup=markup_key,
        )
        return MAIN_MENU

    def user_is_admin(self, user):
        response = get_api_answer('check_admin', user)
        check_admin_lst = response['check_admin']
        return check_admin_lst[0]['status']
