import asyncio
from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.types import ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from create_bot import admins, tg_db
from keyboards.reply_keyboard import main_kb
from keyboards.inline_keyboard import inline_kb_store
from db_hadlers.db_class import DatabaseBot




user_router = Router()


@user_router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    
    async with DatabaseBot(tg_db) as database:
        user_exists = await database.check_user(message.from_user.id)
        
        if not user_exists:
            await message.answer('Привіт👋\nВ цьому боті ти можеш відслідковувати ціни на свої товари в різних онлайн магазинах🤑 \
                                \nКоли вони будуть падати або підніматися бот тебе про це повідомить👌', reply_markup=ReplyKeyboardRemove())
            await database.add_user(message.from_user.id, message.from_user.username)
    
    await message.answer(f'Ось головне меню!', reply_markup=main_kb(message.from_user.id))
    
    
@user_router.message(F.text == '🛍 Додати новий товар')
async def cmd_add_new_product(message:Message):
    msg = await message.answer('Виберіть онлайн магази🛒', reply_markup=ReplyKeyboardRemove())
    asyncio.sleep(0.1)
    await msg.delete()

    await message.answer(f'Виберіть онлайн магази🛒', reply_markup=inline_kb_store())
    

@user_router.message(F.text == '❓ Про нас')
async def cmd_about_us(message: Message):
    await message.answer(f'Бот створений для спостереженям за цінами в різних онлайн магазинах')
    await message.answer(f'Бот поки що знаходиться в стадії розробки, якщо ви знайшли якись баг повідомте мене про це будь ласка'
                         , reply_markup=main_kb(message.from_user.id))
    

@user_router.callback_query(F.data == 'back_home')
async def cmd_on_main(data: CallbackQuery, state: FSMContext):
    await state.clear()
    await data.answer()
    await data.message.delete()
    await data.message.answer(f'Ось головне меню!', reply_markup=main_kb(data.from_user.id))
    
