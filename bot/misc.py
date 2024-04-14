import asyncio
import logging
import sys
from configparser import ConfigParser
from aiogram.methods.delete_webhook import DeleteWebhook

from aiogram import Bot, Dispatcher, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.enums import ParseMode

from bot.handlers import router
import bot.menu as menu
from aiogram import Bot

config = ConfigParser()
config.read("config.ini")

TOKEN = config["BOT"]["Token"]

dp = Dispatcher()
final_router = Router()
dp.include_router(router)
dp.include_router(final_router)


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Привіт <b>{message.from_user.full_name}</b>! 👋 \n\n🤖 Цей бот створений для <b>допомоги ВПО та волонтерам</b>, розроблений студентами ЛНУ Івана Франка. Це загальна база даних, яка збирає інформацію про волонтерські події та допомогу ВПО <b>в одному зручному місці</b>.",
                         reply_markup=menu.main_menu, parse_mode=ParseMode.HTML)


@dp.message(Command("help"))
async def command_help_handler(message: Message) -> None:
    await message.answer(f"Список команд бота:\n"
                         f"\t start - Запустити бота✅\n"
                         f"\t help - Список команд📋\n",
                         reply_markup=menu.main_menu)


@final_router.message()
async def echo(message: Message):
    await message.reply("Не зрозумів ваше питання. 🤷‍♀️ \nСпробуйте ще раз або натисніть /start чи /help")


async def main() -> None:
    bot = Bot(TOKEN)
    await bot(DeleteWebhook(drop_pending_updates=True))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
