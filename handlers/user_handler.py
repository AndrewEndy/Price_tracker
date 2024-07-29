from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.types import ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from create_bot import admins, tg_db
from keyboards.reply_keyboard import main_kb
from db_hadlers.db_class import DatabaseBot
#from keyboards.inline_keyboards import base_link_kb

user_router = Router()


@user_router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    state.clear()
    
    async with DatabaseBot(tg_db) as database:
        user_exists = await database.check_user(message.from_user.id)
        
        if not user_exists:
            await message.answer('Привіт👋\nВ цьому боті ти можеш відслідковувати ціни на свої товари в різних онлайн магазинах🤑 \
                                \nКоли вони будуть падати або підніматися бот тебе про це повідомить👌', reply_markup=ReplyKeyboardRemove())
            await database.add_user(message.from_user.id, message.from_user.username)
    
    await message.answer(f'Ось головне меню!', reply_markup=main_kb(message.from_user.id))
    

@user_router.message(F.text == '❓ Про нас')
async def cmd_about_us(message: Message):
    await message.answer(f'Бот створений для спостереженям за цінами в різних онлайн магазинах')
    await message.answer(f'Бот поки що знаходиться в стадії розробки, якщо ви знайшли якись баг повідомте мене про це будь ласка'
                         , reply_markup=main_kb(message.from_user.id))
