import asyncio
from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.utils.chat_action import ChatActionSender
from aiogram.types import Message, CallbackQuery
from aiogram.types import ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from create_bot import admins, tg_db, bot
from keyboards.reply_keyboard import main_kb
from keyboards.inline_keyboard import back_buttons, show_all_my_products, button_displaying_product
from db_hadlers.db_class import DatabaseBot
from utils.text_all_user_products import get_text_for_all_products, get_text_for_product, get_update_data_text
from utils.form_fsm import Change_name_form
from all_stores.rozetka.get_data_from_rozetka import get_product_data_from_rozetka


view_router = Router()


# -----Переглянути мої товари-----  

# *** Показати мої товари ***  

@view_router.message(F.text == '👀 Переглянути мої товари')
async def show_my_products(message: Message):
    '''Хендлер для перегляду товарів користувача'''
    async with DatabaseBot(tg_db) as database:
        products = await database.get_products(message.from_user.id) # [(id, tg_id, URL, name, store_name, price, min_price, max_price, state, currency)]
        
    if products:
        msg = await message.answer('Виберіть один з варіантів', reply_markup=ReplyKeyboardRemove())
        asyncio.sleep(0.1)
        await msg.delete()

        await message.answer(f'Виберіть один з варіантів', reply_markup=show_all_my_products(products))
    else:
        await message.answer(f'У вас немає доданих товарів😔', reply_markup=main_kb(message.from_user.id))
    
    
@view_router.callback_query(F.data == 'show_my_products')
async def show_my_products(data: CallbackQuery):
    '''Хендлер для перегляду товарів користувача'''
    
    await data.answer()
    await data.message.delete()
    
    async with DatabaseBot(tg_db) as database:
        products = await database.get_products(data.from_user.id) # [(id, tg_id, URL, name, store_name, price, min_price, max_price, state, currency)]
        
    if products:
        msg = await data.message.answer('Виберіть один з варіантів', reply_markup=ReplyKeyboardRemove())
        asyncio.sleep(0.1)
        await msg.delete()

        await data.message.answer(f'Виберіть один з варіантів', reply_markup=show_all_my_products(products))
    else:
        await data.message.answer(f'У вас немає доданих товарів😔', reply_markup=main_kb(data.from_user.id))


@view_router.callback_query(F.data == 'show_all_products')
async def show_all_products(data: CallbackQuery):
    '''Хендлер який виводить всю інформацію про всі товари користувача'''
    
    await data.answer()
    await data.message.delete()
    
    async with DatabaseBot(tg_db) as database:
        products = await database.get_products(data.from_user.id)
        
    text = await get_text_for_all_products(products)
    
    await data.message.answer(text=text, reply_markup=main_kb(data.from_user.id))
    

@view_router.callback_query(F.data.startswith('product_'))
async def show_user_product(data: CallbackQuery):
    '''Хендлер для виведення інформації про конкретний товар користувача'''
    await data.answer()
    await data.message.delete()
    
    product_id = int(data.data.replace('product_', ''))
    
    async with DatabaseBot(tg_db) as database:
        # [(id, tg_id, URL, name, store_name, price, min_price, max_price, state, currency)]
        product = await database.get_product_by_product_id(product_id, data.from_user.id)
        
    text = await get_text_for_product(product)
    
    await data.message.answer(text=text, reply_markup=button_displaying_product(product_id))


# *** Змінити назву товара ***  

@view_router.callback_query(F.data.startswith('change_name_'))
async def change_name(data: CallbackQuery, state: FSMContext):
    '''Хендлер для змінни назви товару'''
    await data.answer()
    await data.message.delete()
    
    product_id = int(data.data.replace('change_name_', ''))
    
    await data.message.answer(f'Введіть назву товара')
    
    await state.set_state(Change_name_form.change_name)
    await state.update_data(change_name = product_id)
    

@view_router.message(F.text, Change_name_form.change_name)
async def set_new_name(message: Message, state: FSMContext):
    '''Хендлер який змінює назву товару в БД'''
    
    if len(message.text) > 40: # Якщо назва занадто довга, просить ввести коротшу назву 
        await message.answer(f'Назва завелика!\nБудь ласка введіть іншу')
        await state.set_state(Change_name_form.change_name)
        
    else: # Інкаше змінює назву в БД і перекидає в головне меню
        product_id = await state.get_data()
        
        async with DatabaseBot(tg_db) as database:
            await database.update_product_name_by_product_id(int(product_id.get('change_name')), message.text)
            
        await state.clear()
        await message.answer(f'Назву змінено!', reply_markup=main_kb(message.from_user.id))


@view_router.message(Change_name_form.change_name)
async def foo(message: Message, state: FSMContext):
    '''Хендлер спрацьовує якщо користувач ввів щось не те'''
    await message.answer(f'Введіть назву товару!')
    await state.set_state(Change_name_form.change_name)
        
    
# *** Оновити дані про товар ***

@view_router.callback_query(F.data.startswith('update_status_'))
async def update_product_data(data: CallbackQuery):
    '''Метод який буде оновлювати дані товара'''
    
    async with ChatActionSender.typing(bot=bot, chat_id=data.from_user.id):
        
        asyncio.sleep(1)
        
        await data.answer()
        await data.message.delete()

        product_id = int(data.data.replace('update_status_', ''))

        async with DatabaseBot(tg_db) as database:
            product = await database.get_product_by_product_id(product_id, data.from_user.id)
            # [(id, tg_id, URL, name, store_name, price, min_price, max_price, state, currency)]
        product = product[0]

        
        if product[4] == 'Rozetka':
            new_data = await get_product_data_from_rozetka(product[2])
            if new_data:
                
                print(product) #product (3, 701084602, 'URL', 'RTX 3060', 'Rozetka', 13249.0, 13200.0, 13509.0, 'Є в наявності', '₴')
                print(new_data) #new_data ('name', 13249.0, 13509.0, '₴', 'Є в наявності')
                
                if  (product[5] == new_data[1]) and (not new_data[2] or product[7] == new_data[2]) \
                and (not new_data[-1] or product[8] == new_data[-1]) and (not new_data[3] or product[-1] == new_data[3]):
                    await data.message.answer(f'Ніякі дані товару не змінились🙌', reply_markup=main_kb(data.from_user.id))
                    
                else:
                    await data.message.answer(f'Виявлено нові дані🧐') 
                    asyncio.sleep(2)
                    
                    async with DatabaseBot(tg_db) as database:
                        await database.update_price_state_currency_by_product_id(new_data[1], new_data[-1], new_data[3], product_id)
                        
                        if product[6] > new_data[1]:
                            await database.update_min_price_by_product_id(new_data[1], product_id)
                        
                        if product[7] < new_data[1]:
                            await database.update_max_price_by_product_id(new_data[1], product_id)
                            
                        elif new_data[2] and product[7] < new_data[2]:
                            await database.update_max_price_by_product_id(new_data[2], product_id)
                        
                        new_data = await database.get_product_by_product_id(product_id, data.from_user.id)
                        
                    text = await get_update_data_text(product, new_data)
                    
                    await data.message.answer(text, reply_markup=back_buttons())
            else:
                data.message.answer(f'Даний товар більше не доступний😢', reply_markup=main_kb(data.from_user.id))