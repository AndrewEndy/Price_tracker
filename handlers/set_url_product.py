from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.types import ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from create_bot import admins, tg_db, bot
from keyboards.reply_keyboard import main_kb
from keyboards.inline_keyboard import inline_kb_store, back_inline_kb, check_name_product
from db_hadlers.db_class import DatabaseBot




spu_router = Router()

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
    