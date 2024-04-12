from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton, ReplyKeyboardBuilder, KeyboardButton
from aiogram.types.reply_keyboard_remove import ReplyKeyboardRemove

import bot.menu as menu
import bot.texts as texts


router = Router()


# як додати обробник власної команди
@router.message(Command("test_command"))
async def my_command_handler(message: Message) -> None:
    await message.answer("/test_command executed!")


# приклад створення inline menu
@router.message(Command("inline_menu_command"))
async def inline_menu_command_handler(message: Message) -> None:
    buttons = [
        [InlineKeyboardButton(text="Inline 1", callback_data=InlineButton1CallbackData(id=1).pack()),
         InlineKeyboardButton(text="Inline 2", callback_data=InlineButton1CallbackData(id=2).pack())],
        [InlineKeyboardButton(text="Inline 3", callback_data=InlineButton1CallbackData(id=3).pack())],
    ]
    builder = InlineKeyboardBuilder(buttons)
    # builder = builder.adjust(1) # якщо хочеш перезадати максимальну кількість кнопок в 1 рядку
    await message.answer("/inline_menu_command executed!", reply_markup=builder.as_markup())


# приклад створення callback-у для inline кнопок
class InlineButton1CallbackData(CallbackData, prefix="inline_button"):
    id: int # параметрів можна й не додавати. Тоді замість цього рядка пишуть pass


# приклад обробки натискання inline кнопок
@router.callback_query(InlineButton1CallbackData.filter())
async def inline_button1_handler(callback: types.CallbackQuery, callback_data: InlineButton1CallbackData) -> None:
    await callback.message.answer(f"Inline button {callback_data.id} pressed!")
    await callback.answer("") # для прибирання затримки в кнопці


@router.message(Command("reply_menu_command"))
async def reply_menu_command_handler(message: Message) -> None:
    buttons = [
        [KeyboardButton(text="Reply 1"),
         KeyboardButton(text="Reply 2")],
        [KeyboardButton(text="Reply 3")],
    ]
    builder = ReplyKeyboardBuilder(buttons)
    # builder = builder.adjust(1) # якщо хочеш перезадати максимальну кількість кнопок в 1 рядку

    # приклад створення reply menu (from markup) (так можна створювати і inline menu)
    # markup = menu.reply_markup
    # приклад створення reply menu (builder)
    markup = builder.as_markup()

    await message.answer("/reply_menu_command executed!", reply_markup=markup)


# приклад опрацювання reply markup
@router.message()
async def main_handler(message: Message) -> None:
    if message.text == texts.REPLY_BUTTON_1_TEXT:
        await message.answer("Answer for reply button 1")
    elif message.text == texts.REPLY_BUTTON_2_TEXT:
        await message.answer("Answer for reply button 2")
    elif message.text == texts.REPLY_BUTTON_3_TEXT:
        # приклад видалення reply markup
        await message.answer("Answer for reply button 3", reply_markup=ReplyKeyboardRemove())
    else:
        await message.answer("Did not understand your command! Try again!")
