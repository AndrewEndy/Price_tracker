from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.types import ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from create_bot import admins, tg_db
from keyboards.reply_keyboard import main_kb
from keyboards.inline_keyboard import inline_kb_store, back_inline_kb
from db_hadlers.db_class import DatabaseBot
from utils.form_fsm import Form_rozetka
from utils.check_url import check_url
from all_stores.rozetka.is_rozetka import is_rozetka


spu_router = Router()


# ------ ROZETKA

@spu_router.callback_query(F.data == 'store_rozetka')
async def add_product_from_rozetka(data: CallbackQuery, state: FSMContext):
    await data.answer()
    await data.message.delete()
    
    await data.message.answer(f'Введіть силку на товар', reply_markup=back_inline_kb())
    await state.set_state(Form_rozetka.url)
    
    
@spu_router.message(F.text, Form_rozetka.url)
async def set_url(message: Message, state: FSMContext):
    
    result = await check_url(message.text)
    
    if not result:
        await message.answer(f'Ви ввели некоректну силку!', reply_markup=back_inline_kb())
        await state.set_state(Form_rozetka.url)
    else:
        if not is_rozetka:
            await message.answer(f'Ви ввели некоректну силку!', reply_markup=back_inline_kb())
            await state.set_state(Form_rozetka.url)
        else:
            await message.answer(f'Товар додано!', reply_markup=main_kb(message.from_user.id))
            await state.clear()
            # ПРОДОВЖИТИ


@spu_router.message(Form_rozetka.url)
async def foo(message: Message, state: FSMContext):
    await message.answer(f'Ви ввели некоректну силку!')
    await state.set_state(Form_rozetka.url)


# ------ PROM

@spu_router.callback_query(F.data == 'store_prom')
async def add_product_from_prome(data: CallbackQuery):
    await data.answer()
    await data.message.delete()
    await data.message.answer(f'Ви вибрали магазин Prome', reply_markup=back_inline_kb())
    

# ------ OLX
    
@spu_router.callback_query(F.data == 'store_olx')
async def add_product_from_olx(data: CallbackQuery):
    await data.answer()
    await data.message.delete()
    await data.message.answer(f'Ви вибрали магазин OLX', reply_markup=back_inline_kb())


# ------ ALLO
    
@spu_router.callback_query(F.data == 'store_allo')
async def add_product_from_allo(data: CallbackQuery):
    await data.answer()
    await data.message.delete()
    await data.message.answer(f'Ви вибрали магазин АЛЛО', reply_markup=back_inline_kb())
    