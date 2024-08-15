from aiogram.fsm.state import State, StatesGroup

# Класи для FSM стану 

class Change_name_form(StatesGroup):
    change_name = State()


class Form_rozetka(StatesGroup):
    url = State()
    check = State()
    set_name = State()

class Form_prom(StatesGroup):
    url = State()

class Form_olx(StatesGroup):
    url = State()

class Form_allo(StatesGroup):
    url = State()