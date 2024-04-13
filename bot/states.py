from aiogram.fsm.state import State, StatesGroup


class VerificationStatesGroup(StatesGroup):
    login = State()
    password = State()


class Form(StatesGroup):
    accommodation = State()
    volunteer = State()
    qa = State()

