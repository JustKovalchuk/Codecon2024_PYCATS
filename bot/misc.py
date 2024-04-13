import asyncio
import logging
import sys
from configparser import ConfigParser
from aiogram.methods.delete_webhook import DeleteWebhook

from aiogram import Bot, Dispatcher, Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from bot.handlers import router
import bot.menu as menu
from aiogram import Bot

config = ConfigParser()
config.read("config.ini")

TOKEN = config["BOT"]["Token"]

dp = Dispatcher()
dp.include_router(router)


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Привіт {message.from_user.full_name}! Це бот створений для ...",
                         reply_markup=menu.main_menu)


async def main() -> None:
    bot = Bot(TOKEN)
    await bot(DeleteWebhook(drop_pending_updates=True))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
