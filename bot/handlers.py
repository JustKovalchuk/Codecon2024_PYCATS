from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.types.reply_keyboard_remove import ReplyKeyboardRemove
from aiogram.enums import ParseMode

import bot.menu as menu
import bot.texts as texts
import bot.filters as filters
import bot.states as states
from bot.callbacks import QACallback

from questions import questions_list, get_question_by_id

router = Router()


class RegionCallback(CallbackData, prefix="region"):
    region: str


class VolunteerRegionCallback(RegionCallback, prefix="volunteer_region"):
    pass


class AccommodationRegionCallback(RegionCallback, prefix="accommodation_region"):
    pass


@router.message(filters.AccommodationFilter())
async def accommodation_handler(message: Message, state: FSMContext) -> None:
    await state.set_state(states.Form.accommodation)
    await message.answer("Оберіть область для житла", reply_markup=menu.get_region_markup(AccommodationRegionCallback))


@router.message(filters.VolunteerFilter())
async def volunteer_handler(message: Message, state: FSMContext) -> None:
    await state.set_state(states.Form.volunteer)
    await message.answer("Оберіть область для волонтерства", reply_markup=menu.get_region_markup(VolunteerRegionCallback))


@router.message(filters.QaFilter())
async def qa_handler(message: Message, state: FSMContext) -> None:
    await state.set_state(states.Form.qa)
    await message.answer("Оберіть одне з питань:", reply_markup=menu.get_qa_markup())


@router.callback_query(VolunteerRegionCallback.filter())
async def volunteer_region_handler(callback: types.CallbackQuery, callback_data: VolunteerRegionCallback) -> None:
    await callback.message.edit_text(f"Знадено наступні волонтерські діяльності за область {callback_data.region}:")
    await callback.message.edit_reply_markup(reply_markup=ReplyKeyboardRemove())


@router.callback_query(AccommodationRegionCallback.filter())
async def volunteer_region_handler(callback: types.CallbackQuery, callback_data: VolunteerRegionCallback) -> None:
    await callback.message.answer(f"Обрано регіон {callback_data.region} для житла", reply_markup=menu.main_menu)
    await callback.message.edit_reply_markup(reply_markup=ReplyKeyboardRemove())


@router.callback_query(QACallback.filter())
async def qa_callback_handler(callback: types.CallbackQuery, callback_data: QACallback) -> None:
    q = get_question_by_id(callback_data.id)
    await callback.message.answer(f"<b>{q.question}</b>:\n\n"
                                  f"{q.answer}", parse_mode=ParseMode.HTML)

