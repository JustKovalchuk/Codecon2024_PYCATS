from aiogram.utils.keyboard import (KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup,
                                    InlineKeyboardBuilder)

import bot.texts as texts
from bot.utils import get_listview, ListType, ListView
from bot.callbacks import QACallback, ListMovementCallbackData, FullListPrint

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
    builder.adjust(1, 1)

    return builder.as_markup(resize_keyboard=True)


def get_inline_keyboard_markup_for_lists(tg_user_id: int, list_view: ListView, list_type: ListType):
    base_markup = []
    lv = get_listview(tg_user_id)
    if lv.has_more_than_one_page():
        back_button = InlineKeyboardButton(
            text=texts.BACK_BUTTON,
            callback_data=ListMovementCallbackData(next=False,
                                                   tg_user_id=tg_user_id,
                                                   list_type=list_type).pack())
        next_button = InlineKeyboardButton(
            text=texts.NEXT_BUTTON,
            callback_data=ListMovementCallbackData(next=True,
                                                   tg_user_id=tg_user_id,
                                                   list_type=list_type).pack())
        if lv.current_page == 0:
            base_markup = [[next_button]]
        elif lv.current_page == lv.max_page-1:
            base_markup = [[back_button]]
        else:
            base_markup = [[back_button, next_button]]
    builder_main = InlineKeyboardBuilder(base_markup)
    builder = InlineKeyboardBuilder()
    data, index = list_view.slice_data()
    for key, value in enumerate(data):
        builder.add(InlineKeyboardButton(text=str(index[key]),
                                         callback_data=FullListPrint(id=key, list_type=list_type).pack()))
        # if list_type == ListType.VOLUNTEER:
        #     builder.add(InlineKeyboardButton(text=str(index[key]),
        #                                      callback_data=FullListPrint(id=value.id, list_type=list_type).pack()))
        # elif list_type == ListType.ACCOMMODATION:
        #     builder.add(InlineKeyboardButton(text=str(index[key]),
        #                                      callback_data=FullListPrint(id=value.id, list_type=list_type).pack()))
    builder.adjust(5, 5)
    builder_main.attach(builder)

    return builder_main.as_markup()