from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.types.reply_keyboard_remove import ReplyKeyboardRemove
from aiogram.enums import ParseMode
from aiogram.utils.formatting import as_list, as_marked_section, Bold, Text

import bot.menu as menu
import bot.texts as texts
import bot.filters as filters
import bot.states as states
from bot.callbacks import QACallback

from db.volunteer_table import VolunteerModel
from db.accommodation_table import AccommodationModel
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
    await message.answer("Введіть назву міста для пошуку житла:")
    # await message.answer("Оберіть область для житла", reply_markup=menu.get_region_markup(AccommodationRegionCallback))


@router.message(states.Form.accommodation)
async def accommodation_city_search_handler(message: Message, state: FSMContext) -> None:
    accommodation_list = AccommodationModel.find_by_location(message.text)
    index = 0
    if len(accommodation_list) == 0:
        await message.answer("Житла не знайдено")
    else:
        for accommodation in accommodation_list:
            index += 1
            content = as_list(
                as_marked_section(
                    Text(Bold(f"{index}"), ". ", Bold(accommodation.name), ":"),
                    Text(Bold("Локація"), f": {accommodation.region}"),
                    Text(Bold("Дата"), f": {accommodation.date}"),
                    Text(Bold("Кого приймають"), f": {accommodation.accepted}"),
                    Text(Bold("На який термін"), f": {accommodation.term}"),
                    Text(Bold("Тип розміщення"), f": {accommodation.accommodation_type}\n"
                                                 f"\nПовна інформація за посиланням -> {accommodation.url}"),
                    marker="   🔸 ",
                ),
            )
            await message.answer(**content.as_kwargs())
    await state.clear()


@router.message(filters.VolunteerFilter())
async def volunteer_handler(message: Message, state: FSMContext) -> None:
    await state.set_state(states.Form.volunteer)
    await message.answer("Введіть назву міста для пошуку волонтерської активності:")
    # await message.answer("Оберіть область для волонтерства", reply_markup=menu.get_region_markup(VolunteerRegionCallback))


@router.message(states.Form.volunteer)
async def volunteer_city_search_handler(message: Message, state: FSMContext) -> None:
    volunteer_list = VolunteerModel.find_by_location(message.text)
    index = 0
    if len(volunteer_list) == 0:
        await message.answer("Подій не знайдено")
    else:
        for volunteer in volunteer_list:
            index += 1
            content = as_list(
                as_marked_section(
                    Text(Bold(f"{index}"), ". ", Bold(volunteer.name), ":"),
                    Text(Bold("Локація"), f": {volunteer.region}"),
                    Text(Bold("Дата"), f": {volunteer.date}"),
                    Text(Bold("Організатор"), f": {volunteer.organizer}\n"
                                              f"\nПовна інформація за посиланням -> {volunteer.url}"),
                    marker="   🔸 ",
                ),
            )
            await message.answer(**content.as_kwargs())
    await state.clear()


@router.message(filters.QaFilter())
async def qa_handler(message: Message, state: FSMContext) -> None:
    await state.set_state(states.Form.qa)
    await message.answer("Оберіть одне з питань:", reply_markup=menu.get_qa_markup())


@router.callback_query(VolunteerRegionCallback.filter())
async def volunteer_region_handler(callback: types.CallbackQuery, callback_data: VolunteerRegionCallback) -> None:
    await callback.message.edit_text(f"Знадено наступні волонтерські діяльності за область {callback_data.region}:")
    volunteer_events = VolunteerModel.get_all()
    for event in volunteer_events:
        if event.region == callback_data.region:
            await callback.message.answer(event.description)

    await callback.message.edit_reply_markup(reply_markup=ReplyKeyboardRemove())


@router.callback_query(AccommodationRegionCallback.filter())
async def volunteer_region_handler(callback: types.CallbackQuery, callback_data: VolunteerRegionCallback) -> None:
    await callback.message.answer(f"Обрано область {callback_data.region} для житла", reply_markup=menu.main_menu)
    await callback.message.edit_reply_markup(reply_markup=ReplyKeyboardRemove())


@router.callback_query(QACallback.filter())
async def qa_callback_handler(callback: types.CallbackQuery, callback_data: QACallback) -> None:
    q = get_question_by_id(callback_data.id)
    await callback.message.answer(f"<b>{q.question}</b>:\n\n"
                                  f"{q.answer}", parse_mode=ParseMode.HTML)

