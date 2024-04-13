from aiogram.utils.keyboard import (KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup,
                                    InlineKeyboardBuilder)

import bot.texts as texts
from bot.callbacks import QACallback

from questions import questions_list
from regions import regions_list


main_menu = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text=texts.ACCOMMODATION),
         KeyboardButton(text=texts.VOLUNTEER)],
        [KeyboardButton(text=texts.QA)],
    ])


def get_region_markup(callback):
    buttons = [InlineKeyboardButton(text=region, callback_data=callback(region=region).pack()) for region in regions_list]

    builder = InlineKeyboardBuilder()
    builder.add(*buttons)
    builder.adjust(2, 2)

    return builder.as_markup(resize_keyboard=True)


def get_qa_markup():
    buttons = [InlineKeyboardButton(text=v.question, callback_data=QACallback(id=i).pack()) for i, v in
               questions_list.items()]

    builder = InlineKeyboardBuilder()
    builder.add(*buttons)
    builder.adjust(2, 2)

    return builder.as_markup(resize_keyboard=True)


reply_markup = ReplyKeyboardMarkup(keyboard=[])

