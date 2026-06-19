from aiogram.fsm.state import State, StatesGroup


class LeadForm(StatesGroup):
    name = State()
    phone = State()
    service = State()
    comment = State()