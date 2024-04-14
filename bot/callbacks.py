from aiogram.filters.callback_data import CallbackData
from bot.utils import ListType


class QACallback(CallbackData, prefix="qa_answer"):
    id: int


class FullListPrint(CallbackData, prefix="full_list"):
    id: int
    list_type: ListType


class ListMovementCallbackData(CallbackData, prefix='list_movement'):
    next: bool
    tg_user_id: int
    list_type: ListType


class DonateGroupCallback(CallbackData, prefix='donate_group'):
    group: str


class DonateInGroupNamesCallback(CallbackData, prefix='donate_in_group'):
    name: str


class PrintDonateCallback(CallbackData, prefix='print_donate'):
    id: int
