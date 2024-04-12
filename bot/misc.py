import asyncio
import logging
import sys
from os import getenv
from configparser import ConfigParser
from aiogram.methods.delete_webhook import DeleteWebhook

from aiogram import Bot, Dispatcher, Router, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.markdown import hbold

from bot.handlers import router

config = ConfigParser()
config.read("config.ini")

TOKEN = config["BOT"]["Token"]

dp = Dispatcher()
dp.include_router(router)


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Hello, {hbold(message.from_user.full_name)}!\n"
                         f"commands: /test_command, /inline_menu_command, /reply_menu_command")


async def main() -> None:
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    await bot(DeleteWebhook(drop_pending_updates=True))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())