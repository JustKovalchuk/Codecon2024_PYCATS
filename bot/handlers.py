from aiogram import Router, types, Bot
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.types.reply_keyboard_remove import ReplyKeyboardRemove
from aiogram.enums import ParseMode
from aiogram.utils.formatting import as_list, as_marked_section, Bold, Text
from aiogram.utils.keyboard import InlineKeyboardButton, InlineKeyboardMarkup
import bot.menu as menu
import bot.texts as texts
import bot.filters as filters
import bot.states as states
from bot.utils import ListView, print_list, ListType, get_listview, save_listview
from bot.callbacks import QACallback, FullListPrint, ListMovementCallbackData

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
    await message.answer("Введіть назву міста для пошуку житла 🔍:")
    # await message.answer("Оберіть область для житла", reply_markup=menu.get_region_markup(AccommodationRegionCallback))


@router.message(states.Form.accommodation)
async def accommodation_city_search_handler(message: Message, state: FSMContext) -> None:
    accommodation_list = AccommodationModel.find_by_location(message.text)
    lv = ListView(accommodation_list, start_text="Список житла за вашим запитом:\n", empty_data_text="На жаль, житла не знайдено🤷‍♀️")
    await print_list(message, lv, ListType.ACCOMMODATION)
    await state.clear()


@router.message(filters.VolunteerFilter())
async def volunteer_handler(message: Message, state: FSMContext) -> None:
    await state.set_state(states.Form.volunteer)
    await message.answer("Введіть назву міста для пошуку волонтерської активності 🔍:")
    # await message.answer("Оберіть область для волонтерства", reply_markup=menu.get_region_markup(VolunteerRegionCallback))


@router.message(states.Form.volunteer)
async def volunteer_city_search_handler(message: Message, state: FSMContext) -> None:
    volunteer_list = VolunteerModel.find_by_location(message.text)
    lv = ListView(volunteer_list, start_text="Список волонтерських діяльностей за вашим запитом:\n",
                  empty_data_text="Волонтерських діяльностей не знайдено🤷‍♀️")
    await print_list(message, lv, ListType.ACCOMMODATION)
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
    await callback.answer()


@router.callback_query(AccommodationRegionCallback.filter())
async def volunteer_region_handler(callback: types.CallbackQuery, callback_data: VolunteerRegionCallback) -> None:
    await callback.message.answer(f"Обрано область {callback_data.region} для житла", reply_markup=menu.main_menu)
    await callback.message.edit_reply_markup(reply_markup=ReplyKeyboardRemove())
    await callback.answer()


@router.callback_query(QACallback.filter())
async def qa_callback_handler(callback: types.CallbackQuery, callback_data: QACallback, bot: Bot) -> None:
    q = get_question_by_id(callback_data.id)
    txt = f"<b>{q.question}</b>:\n\n{q.answer}"
    if q.link:
        markup = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Посилання', url=q.link)]])
        await callback.message.answer(text=txt, parse_mode=ParseMode.HTML, reply_markup=markup)
    else:
        await callback.message.answer(txt, parse_mode=ParseMode.HTML)
    await callback.answer()


@router.callback_query(ListMovementCallbackData.filter())
async def list_movement_handler(callback: types.CallbackQuery, callback_data: ListMovementCallbackData) -> None:
    lv = get_listview(callback_data.tg_user_id)

    if callback_data.next:
        lv.next()
    else:
        lv.previous()

    save_listview(callback.message.from_user.id, lv)
    await print_list(callback.message, lv, callback_data.list_type, edit=True)
    await callback.answer()


@router.callback_query(FullListPrint.filter())
async def list_movement_handler(callback: types.CallbackQuery, callback_data: FullListPrint) -> None:
    id = callback_data.id
    lv: ListView = get_listview(callback.from_user.id)
    data, indexes = lv.slice_data()
    await callback.message.answer(data[id].full_string(indexes[id]), parse_mode=ParseMode.HTML)
    await callback.answer()