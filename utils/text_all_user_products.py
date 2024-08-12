

async def get_text_for_all_products(products: list) -> str:
    '''Функція для створення тексту про всі товари користувача'''
    
    str = '<b>Ось вся інформація про ваші товари</b>🧐:\n'
    
    # [(id, tg_id, URL, name, store_name, price, min_price, max_price, state, currency)] 
    for tupl in products:
        
        temp_str = f'''\n🛒<b>Магазин:</b> {tupl[4]}\n📝<b>Назва товара:</b> {tupl[3]}\n💸<b>Ціна зараз:</b> {tupl[5]}{tupl[-1]}\n'''
        
        if tupl[5] != tupl[6]:
            temp_str+=f'📉<b>Мінімальна ціна:</b> {tupl[6]}{tupl[-1]}\n'
        
        if tupl[5] != tupl[7]:
            temp_str+=f'📈<b>Максимальна ціна:</b> {tupl[7]}{tupl[-1]}\n'
            
        if tupl[-2]:
            temp_str+=f'❔<b>Статус:</b> {tupl[-2]}\n'
        
        temp_str+='\n'
        
        str+=temp_str
        
    return str


async def get_text_for_product(product: list) -> str:
    '''Функція для створення тексту про товар користувача'''
    
    str = '<b>Ось інформація про цей товар</b>🧐:\n'
    
    # [(id, tg_id, URL, name, store_name, price, min_price, max_price, state, currency)] 
    for tupl in product:
        
        temp_str = f'''\n🛒<b>Магазин:</b> {tupl[4]}\n📝<b>Назва товара:</b> {tupl[3]}\n💸<b>Ціна зараз:</b> {tupl[5]}{tupl[-1]}\n'''
        
        if tupl[5] != tupl[6]:
            temp_str+=f'📉<b>Мінімальна ціна:</b> {tupl[6]}{tupl[-1]}\n'
        
        if tupl[5] != tupl[7]:
            temp_str+=f'📈<b>Максимальна ціна:</b> {tupl[7]}{tupl[-1]}\n'
            
        if tupl[-2]:
            temp_str+=f'❔<b>Статус:</b> {tupl[-2]}\n'
        
        temp_str+='\n'
        
        str+=temp_str
        
    return str