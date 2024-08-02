from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder


def inline_kb_store():
    '''Inline клавіатура з вибором різних інтернет магазинів'''
    inline_kb_list = [
        [InlineKeyboardButton(text='Rozetka', callback_data='store_rozetka'), InlineKeyboardButton(text='Prom', callback_data='store_prom')],
        [InlineKeyboardButton(text='OLX', callback_data='store_olx'), InlineKeyboardButton(text='АЛЛО', callback_data='store_allo')],
        [InlineKeyboardButton(text='«Назад', callback_data='back_home')]
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)

def back_inline_kb():
    '''Inline клавіатура з кнопкою яка переносить в головне меню'''
    return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='«На головну', callback_data='back_home')]])

def check_name_product():
    '''Inline клавіатура для перевірки чи підходить назва товара'''
    return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='OK', callback_data='good')
                                                  ,InlineKeyboardButton(text='Змінити назву', callback_data='change_name')]])
