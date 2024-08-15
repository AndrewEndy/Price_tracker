import asyncio
from aiogram.types import BotCommand, BotCommandScopeDefault
from create_bot import bot, dp, scheduler

from handlers.user_handler import user_router
from handlers.set_url_product import spu_router
from handlers.rozetka_handler import rozetka_router
from handlers.view_products_handler import view_router

from create_bot import admins, tg_db
from db_hadlers.db_class import DatabaseBot
#from work_time.send_message import send_message_time
from datetime import datetime, timedelta


async def set_commands():
    commands = [BotCommand(command='start', description='Запустити/перезапустити бота'),
                BotCommand(command='info', description='Інформація про бот'),]
    await bot.set_my_commands(commands, BotCommandScopeDefault())



async def start_bot():
    await set_commands()
    
    async with DatabaseBot(tg_db) as database:
        await database.on_start_up()
        
    #count_users = await get_all_users(count=True)
    try:
        for admin_id in admins:
            await bot.send_message(admin_id, f'Я запущений🥳')
    except:
        pass


# Функция, которая выполнится когда бот завершит свою работу
async def stop_bot():
    try:
        for admin_id in admins:
            await bot.send_message(admin_id, 'Бот виключений😔')
    except:
        pass



async def main():
    # scheduler.add_job(send_message_time, 'interval', seconds=7200, next_run_time=datetime.now(), args=(bot,))
    # scheduler.start()
    
    dp.include_router(rozetka_router)
    dp.include_router(spu_router)
    dp.include_router(user_router)
    dp.include_router(view_router)
    
    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)

    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await bot.session.close()



if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print(f'\033[32mБот завершив роботу\033[0m')

