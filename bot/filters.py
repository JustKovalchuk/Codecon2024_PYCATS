from aiogram.filters import Filter
from aiogram.types import Message

import bot.texts as texts


class AccommodationFilter(Filter):
    async def __call__(self, message: Message):
        return message.text.lower() == texts.ACCOMMODATION.lower()


class VolunteerFilter(Filter):
    async def __call__(self, message: Message):
        return message.text.lower() == texts.VOLUNTEER.lower()


class QaFilter(Filter):
    async def __call__(self, message: Message):
        return message.text.lower() == texts.QA.lower()
