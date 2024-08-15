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


def show_all_my_products(products: list) -> InlineKeyboardBuilder:
    '''Inline клавіатура з усіма товарами користувача'''
    
    builder = InlineKeyboardBuilder()
    
    for tupl in products:
        builder.row(
            InlineKeyboardButton(
                text=tupl[3],
                callback_data=f'product_{tupl[0]}'
            )
        )
        
    # Додаєм кнопку "Переглянути всі" 
    builder.row(
        InlineKeyboardButton(
            text='Переглянути всі',
            callback_data='show_all_products'
        )
    )
        
    # Додаєм кнопку "На головну"
    builder.row(
        InlineKeyboardButton(
            text='Назад',
            callback_data='back_home'
        )
    )
    # Настраиваем размер клавиатуры
    builder.adjust(1)
    return builder.as_markup()


def button_displaying_product(product_id: int) -> InlineKeyboardMarkup:
    '''Inline клавіатура для кнопок при показі товара'''
    return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Оновити дані', callback_data=f'update_status_{product_id}')],
                                                  [InlineKeyboardButton(text='Змінити назву', callback_data=f'change_name_{product_id}')],
                                                  [InlineKeyboardButton(text='На головну', callback_data='back_home')],
                                                  [InlineKeyboardButton(text='Назад', callback_data='show_my_products')]
                                                  ])


def back_buttons() -> InlineKeyboardMarkup:
    '''Inline клавіатура з кнопками на головну і назад'''
    return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='На головну', callback_data='back_home')],
                                                  [InlineKeyboardButton(text='Назад', callback_data='show_my_products')]
                                                  ])