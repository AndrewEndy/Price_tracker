from db_hadlers.db_class import DatabaseBot
from create_bot import tg_db

async def set_product_data_rozetka(telegram_id: int, url: str, name: str | None, store_name: str, price: float | None
                                   , max_price: float | None, currency: str | None, state: str | None):
    '''Функція вносить всі дані про товар в БД'''
    
    if not name: name = 'None'
    if not price: price = 0
    if not max_price: 
        if price: max_price = price
        else: max_price = 0
    if not currency: currency = None
    if not state: state = None
    
    
    async with DatabaseBot(tg_db) as database:
        await database.set_product(telegram_id, url, name, store_name, price, max_price, currency, state)