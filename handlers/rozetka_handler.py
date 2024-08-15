from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.types import ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.utils.chat_action import ChatActionSender
from create_bot import admins, tg_db, bot
from keyboards.reply_keyboard import main_kb
from keyboards.inline_keyboard import inline_kb_store, back_inline_kb, check_name_product
from db_hadlers.db_class import DatabaseBot
from utils.form_fsm import Form_rozetka
from utils.check_url import check_url
from all_stores.rozetka.is_rozetka import is_rozetka, is_product_rozetka
from all_stores.rozetka.get_data_from_rozetka import get_product_data_from_rozetka
from utils.set_product_data import set_product_data_rozetka


rozetka_router = Router()


temp_name = ''

@rozetka_router.callback_query(F.data == 'store_rozetka')
async def add_product_from_rozetka(data: CallbackQuery, state: FSMContext):
    '''Хендлер просить ввести силку і ставить FSM стан'''
    await data.answer()
    await data.message.delete()
    
    await data.message.answer(f'Введіть силку на товар', reply_markup=back_inline_kb())
    await state.set_state(Form_rozetka.url)
    
    
@rozetka_router.message(F.text, Form_rozetka.url)
async def set_url(message: Message, state: FSMContext):
    '''Хендлер перевіряє силку і додає дані в БД'''
    async with ChatActionSender.typing(bot=bot, chat_id=message.from_user.id):
        
        result = await check_url(message.text) # Перевіряє чи можна підлючитись до сайту по силці
        
        if not result: # Якщо ні, то просить ввести силку ще раз
            await message.answer(f'Ця силка некоректна!\nВведіть іншу силку', reply_markup=back_inline_kb())
            await state.set_state(Form_rozetka.url)
        else:
            flag = await is_rozetka(message.text) # Перевіряє чи це сайт Rozetka
            
            if not flag: # Якщо ні, то просить ввести силку ще раз
                await message.answer(f'Ця силка некоректна!\nВведіть іншу силку', reply_markup=back_inline_kb())
                await state.set_state(Form_rozetka.url)
            else:
                flag = await is_product_rozetka(message.text) # Перевіряє чи це силка саме на сторінку з товаром
                
                if flag:
                    async with DatabaseBot(tg_db) as database:
                        flag = await database.check_similar_url(message.from_user.id, message.text) # Перевіряє чи немає вже такої силки в цього користувача
                        
                        if flag: # Якщо є, то виводить це і перекидає в головне меню
                            await message.answer(f'Цей товар уже доданий!', reply_markup=main_kb(message.from_user.id))
                            await state.clear()
                            
                        else: # Якщо немає, то отримує дані з сайту і вносить їх в БД
                            name, price, max_price, currency, state_product = await get_product_data_from_rozetka(message.text)
                            await set_product_data_rozetka(message.from_user.id, message.text, name, 'Rozetka', price, max_price, currency, state_product)
                            
                            # Виводить повідомлення з inlineKeyboard і ставить стан FSM (Form_rozetka.check), щоб або змінити назву в БД або завершити
                            await message.answer(f'<b>Навза товару</b>: {name}', reply_markup=check_name_product())
                            await state.set_state(Form_rozetka.check)
                            
                            global temp_name
                            temp_name = name
                            
                else: # Якщо ні, то просить ввести силку ще раз 
                    await message.answer(f'Ця силка некоректна!\nВведіть іншу силку', reply_markup=back_inline_kb())
                    await state.set_state(Form_rozetka.url) 


@rozetka_router.message(Form_rozetka.url)
async def foo(message: Message, state: FSMContext):
    '''Хендлер який спрацьовує якщо ввели щось не те'''
    await message.answer(f'Ви ввели некоректну силку!')
    await state.set_state(Form_rozetka.url)


@rozetka_router.callback_query(F.data == 'good', Form_rozetka.check)
async def foo(data: CallbackQuery, state: FSMContext):
    '''Хендлер який спрацьовує якщо назва товару влаштовує користувача'''
    await data.answer()
    await data.message.delete()
    await data.message.answer(f'Товар додано!', reply_markup=main_kb(data.from_user.id))
    await state.clear()


@rozetka_router.callback_query(F.data == 'change_name', Form_rozetka.check)
async def change_name(data: CallbackQuery, state: FSMContext):
    '''Хендлер який спрацьовує якщо назва товару не влаштовує користувача'''
    await data.answer()
    await data.message.delete()
    
    await data.message.answer(f'Введіть назву товара')
    await state.set_state(Form_rozetka.set_name)


@rozetka_router.message(Form_rozetka.check)
async def foo(message: Message, state: FSMContext):
    '''Хендлер спрацьовує якщо користувач не вибрав якийсь з варіантів'''
    await message.answer(f'Виберіть щось з запропонованих варіантів!')
    await state.set_state(Form_rozetka.check)


@rozetka_router.message(F.text, Form_rozetka.set_name)
async def set_new_name(message: Message, state: FSMContext):
    '''Хендлер який змінює назву товару в БД'''
    
    async with DatabaseBot(tg_db) as database:
        flag = await database.check_similar_name(message.from_user.id, message.text)
    
    if len(message.text) > 40: # Якщо назва занадто довга, просить ввести коротшу назву 
        await message.answer(f'Назва завелика!\nБудь ласка введіть іншу')
        await state.set_state(Form_rozetka.set_name)
    
    if flag:
        await message.answer(f'Така навзва уже є!', reply_markup=back_inline_kb())
        await state.set_state(Form_rozetka.set_name)
        
    else: # Інкаше змінює назву в БД і перекидає в головне меню
        async with DatabaseBot(tg_db) as database:
            await database.update_product_name_by_old_name(message.from_user.id ,temp_name, message.text)
        #print(temp_name)
        await state.clear()
        await message.answer(f'Товар додано!', reply_markup=main_kb(message.from_user.id))


@rozetka_router.message(Form_rozetka.set_name)
async def foo(message: Message, state: FSMContext):
    '''Хендлер спрацьовує якщо користувач ввів щось не те'''
    await message.answer(f'Введіть назву товару!')
    await state.set_state(Form_rozetka.set_name)

