import math
from enum import Enum


from aiogram.enums import ParseMode
from aiogram.types import Message

import bot.menu as menu


active_listviews = dict()


class ListType(Enum):
    ACCOMMODATION = "ACCOMMODATION"
    VOLUNTEER = "VOLUNTEER"


class ListView:
    def __init__(self, data: list, page_size: int = 10, current_page: int = 0,
                 start_text="Список даних:\n", end_text="",
                 empty_data_text="Даних по вашому запиту не знайдено!"):
        self.page_size = page_size
        self.max_page = math.ceil(float(len(data)) / self.page_size)
        self.data = data
        self.current_page = current_page

        self.start_text = start_text
        self.end_text = end_text
        self.empty_data_text = empty_data_text

    def has_more_than_one_page(self):
        return self.max_page > 1

    def slice_data(self):
        start_index = self.current_page * self.page_size
        end_index = (self.current_page + 1) * self.page_size

        if end_index > len(self.data):
            end_index = len(self.data)

        return self.data[start_index:end_index], range(start_index + 1, end_index + 1)

    def next(self):
        if self.max_page > 0:
            self.current_page = (self.current_page + 1) % self.max_page
        return self.slice_data()

    def previous(self):
        if self.max_page > 0:
            self.current_page = (self.current_page - 1) % self.max_page
        return self.slice_data()


async def print_list(message: Message, lv: ListView, lt: ListType):
    text = ''
    data, index = lv.slice_data()

    for i, v in enumerate(index):
        text += data[i].lv_string(v) + "\n"

    save_listview(message.from_user.id, lv)

    markup = menu.get_inline_keyboard_markup_for_lists(message.from_user.id, lv, lt)
    await message.answer(lv.start_text + text + lv.end_text, reply_markup=markup, parse_mode=ParseMode.HTML)


def save_listview(tg_id, listview: ListView):
    active_listviews.update({tg_id: listview})


def get_listview(tg_id):
    return active_listviews.get(tg_id)


def clear_listview(tg_id):
    active_listviews.pop(tg_id)
