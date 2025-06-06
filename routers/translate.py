from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram import F
from services.api_client import ExplanationClient
from aiogram.utils.keyboard import InlineKeyboardBuilder
from datetime import datetime

router = Router()
mal_client = ExplanationClient()


# Использование: /word <word>
@router.message(Command("word"))
async def cmd_choose_city(message: Message):
    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        return await message.reply("You need to write a word /word buy")

    word = parts[1].strip()
    response = await mal_client.get_explanation(word)
    try:
        response = response[0]
        return await message.reply(f"Word {response['word']}\ndefinition: {response['meanings'][0]['definitions'][0]['definition']}")   
    except:
        return await message.reply(f"Wrong!\n Code: {response['title']}\n Message: {response['message']}")

       
    
