from aiogram.fsm.state import State, StatesGroup

# Класи для FSM стану різних магазинів, щоб коректно опрацювати URL кожного магазина

class Form_rozetka(StatesGroup):
    url = State()

class Form_prom(StatesGroup):
    url = State()

class Form_olx(StatesGroup):
    url = State()

class Form_allo(StatesGroup):
    url = State()