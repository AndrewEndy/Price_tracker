

async def get_text_for_all_products(products: list) -> str:
    '''Функція для створення тексту про всі товари користувача'''
    
    text = '<b>Ось вся інформація про ваші товари</b>🧐:\n'
    
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
        
        text+=temp_str
        
    return text


async def get_text_for_product(product: list) -> str:
    '''Функція для створення тексту про товар користувача'''
    
    text = '<b>Ось інформація про цей товар</b>🧐:\n'
    
    # [(id, tg_id, URL, name, store_name, price, min_price, max_price, state, currency)] 
    for tupl in product:
        
        temp_str = f'''\n🛒<b>Магазин:</b> {tupl[4]}\n📝<b>Назва товара:</b> {tupl[3]}\n💸<b>Ціна зараз:</b> {tupl[5]}{tupl[-1]}\n'''
        
        if tupl[5] != tupl[6]:
            temp_str+=f'📉<b>Мінімальна ціна:</b> {tupl[6]}{tupl[-1]}\n'
        
        if tupl[5] != tupl[7]:
            temp_str+=f'📈<b>Максимальна ціна:</b> {tupl[7]}{tupl[-1]}\n'
            
        if tupl[-2]:
            temp_str+=f'❔<b>Статус:</b> {tupl[-2]}\n'
            
        temp_str += f'🔗<b>Посилання: </b> {tupl[2]}\n'
        
        temp_str+='\n'
        
        text+=temp_str
        
    return text


async def get_update_data_text(product: list, new_data) -> str:
    '''Функція для створення тексту з оновленими даними'''
    
    new_data = new_data[0]
    # [(id, tg_id, URL, name, store_name, price, min_price, max_price, state, currency)] 
     
    text = '<b>Ось Оновлені дані товару</b>🙌:\n'
    
    text += f'\n🛒<b>Магазин:</b> {product[4]}\n📝<b>Назва товара:</b> {product[3]}\n' #💸<b>Ціна зараз:</b> {tupl[5]}{tupl[-1]}\n
        
    if product[5] != new_data[5]:
        text += f'💸<b>Ціна зараз:</b> <s>{product[5]}{product[-1]}</s> ➡️ {new_data[5]}{new_data[-1]}\n'
    else:
        text += f'💸<b>Ціна зараз:</b> {new_data[5]}{new_data[-1]}\n'
    
    if product[6] != new_data[6]:
        text += f'📉<b>Мінімальна ціна:</b> <s>{product[6]}{product[-1]}</s> ➡️ {new_data[6]}{new_data[-1]}\n'
    else:
        text += f'📉<b>Мінімальна ціна:</b> {new_data[6]}{new_data[-1]}\n'
    
    if product[7] != new_data[7]:
        text += f'📈<b>Максимальна ціна:</b> <s>{product[7]}{product[-1]}</s> ➡️ {new_data[7]}{new_data[-1]}\n'
    else:
        text += f'📈<b>Максимальна ціна:</b> {new_data[7]}{new_data[-1]}\n'
        
    if product[-2] != new_data[-2]:
        text += f'❔<b>Статус:</b> <s>{product[-2]}</s> ➡️ {new_data[-2]}\n'
    else:
        text += f'❔<b>Статус:</b> {new_data[-2]}\n'
    
    if product[-1] != new_data[-1]:
        text += f'💵<b>Валюта:</b> <s>{product[-1]}</s> ➡️ {new_data[-1]}\n'
    
    text += f'🔗<b>Посилання: </b> {new_data[2]}\n'
        
    text+='\n'
    
    return text