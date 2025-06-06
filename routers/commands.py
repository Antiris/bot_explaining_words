from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
import logging
from keyboards.builders import keyboard


router = Router()

@router.message(Command("start"))
async def start_command(message: Message):
    await message.answer("Hi! I'm a bot explaining words\n"
                         "Enter /help to display a list of available commands.",
                         reply_markup=keyboard)

    logging.info(f"User {message.from_user.id} called /start")

@router.message(Command("help"))
async def help_command(message: Message):
    await message.answer(
        "Команды:\n"
        "/start - Greetings\n"
        "/word <word> - explaining word\n"
        "/favs - words in favorites\n"
        "/add_fav <word> - add a word to favorites\n"
        "/del_fav <word> - delete a city to favorites\n"
        "/help - list of commands\n"
        "/support - send a message to support"
    )
