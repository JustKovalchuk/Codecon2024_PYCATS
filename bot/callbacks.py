from aiogram.filters.callback_data import CallbackData


class QACallback(CallbackData, prefix="qa_answer"):
    id: int
