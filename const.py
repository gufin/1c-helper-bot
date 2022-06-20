import os

from dotenv import load_dotenv

load_dotenv()

API_1C_API_TOKEN = os.getenv('ONE_C_API_TOKEN')
API_1C_URL = os.getenv('ONE_C_URL')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

MAIN_MENU, GET_STOCK, ADMIN = range(3)

DEBUG = True

ADMIN_KEYBOARD = ['Get_stock', 'Admin', 'Vacation']
USER_KEYBOARD = ['Get_stock', 'Vacation']
ADMIN_ACTIONS_KEYBOARD = ['run_cost_calculation',
                          'crate_update_file',
                          'update_erp']
