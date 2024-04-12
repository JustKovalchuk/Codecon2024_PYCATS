from aiogram.utils.keyboard import KeyboardButton, ReplyKeyboardMarkup
import bot.texts as texts

reply_markup = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text=texts.REPLY_BUTTON_1_TEXT),
         KeyboardButton(text=texts.REPLY_BUTTON_2_TEXT)],
        [KeyboardButton(text=texts.REPLY_BUTTON_3_TEXT)],
    ])