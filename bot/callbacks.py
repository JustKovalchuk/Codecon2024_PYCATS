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
